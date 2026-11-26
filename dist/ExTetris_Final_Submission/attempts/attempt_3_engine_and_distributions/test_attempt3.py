"""Comprehensive unittest suite for Attempt 3 (Engine FSM, Distributions, Board Metrics, Renderers)."""

import contextlib
import io
import sys
import unittest
from collections import Counter

from board import Board
from distributions import (
    AdaptiveDifficultyDistribution,
    BagDistribution,
    MarkovDistribution,
    UniformDistribution,
    WeightedDistribution,
)
from engine import ExTetrisEngine, GameState
from factory import ExTetrominoFactory
from hierarchy import Box1x4Shape, Box4x1Shape, DiagonalPolyplet, FlatLandingShape
import play
from renderers import CLIRenderer, HeadlessRenderer, TkinterRenderer, create_renderer


class TestBoardMetricsAndBounds(unittest.TestCase):
    def test_bounds_metrics_ghost_and_multiline_clear(self):
        b = Board(width=8, height=12)
        factory = ExTetrominoFactory()
        i_horiz = next(p for p in factory.classic_fixed() if isinstance(p, Box1x4Shape))

        self.assertFalse(b.is_valid_position(i_horiz, (0, -1)))
        self.assertFalse(b.is_valid_position(i_horiz, (-1, 0)))
        self.assertFalse(b.is_valid_position(i_horiz, (0, 5)))
        self.assertTrue(b.is_valid_position(i_horiz, (0, 4)))

        b.area[9, 0] = True   # col 0 height=3, 2 holes (rows 10, 11)
        b.area[10, 1] = True  # col 1 height=2, 1 hole (row 11)
        b.area[11, 2] = True  # col 2 height=1, 0 holes
        self.assertEqual(b.column_heights(), [3, 2, 1, 0, 0, 0, 0, 0])
        self.assertEqual(b.get_max_height(), 3)
        self.assertEqual(b.count_holes(), 3)
        self.assertEqual(b.get_bumpiness(), 3)
        self.assertEqual(b.get_ghost_row(i_horiz, (0, 1)), 9)

        # Multi-line clear
        b.area[9, :] = True
        b.area[11, :] = True
        self.assertEqual(b.clear_full_lines(), 2)
        self.assertTrue(b.area[11, 1])  # old row 10 shifted to row 11


class TestDistributionsAndCombinators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.classic = cls.factory.classic_one_sided()
        cls.all_fixed = cls.factory.all_fixed()

    def test_seeded_reproducibility_and_bag_filtered(self):
        d1 = (
            BagDistribution(self.all_fixed, seed=101)
            .filter(lambda p: isinstance(p, FlatLandingShape), seed=101)
            >> (lambda p: p.clone().rotateCW().reclassify())
        )
        d2 = (
            BagDistribution(self.all_fixed, seed=101)
            .filter(lambda p: isinstance(p, FlatLandingShape), seed=101)
            >> (lambda p: p.clone().rotateCW().reclassify())
        )
        seq1 = [p.piece_id for p in d1.sample_many(30)]
        seq2 = [p.piece_id for p in d2.sample_many(30)]
        self.assertEqual(seq1, seq2)

    def test_weighted_bag_markov_adaptive_and_combinators(self):
        # Weighted
        w = WeightedDistribution(self.classic[:3], [8, 1, 1], seed=12)
        c = Counter(p.piece_id for p in w.sample_many(1500))
        self.assertGreater(c[self.classic[0].piece_id], 1050)

        # 7-bag
        bag = BagDistribution(self.classic, seed=3)
        batch = bag.sample_many(14)
        self.assertEqual(len({p.piece_id for p in batch[:7]}), 7)
        self.assertEqual(len({p.piece_id for p in batch[7:]}), 7)

        # Markov anti-repeat
        m = MarkovDistribution(self.classic, repeat_penalty=0.0, seed=4)
        m_seq = [p.piece_id for p in m.sample_many(150)]
        self.assertTrue(all(m_seq[i] != m_seq[i + 1] for i in range(len(m_seq) - 1)))

        # Adaptive distress
        flat = next(p for p in self.all_fixed if isinstance(p, FlatLandingShape))
        hard = next(p for p in self.all_fixed if p.landing_holes() >= 4)
        adapt = AdaptiveDifficultyDistribution([flat, hard], seed=8)
        empty = Board(10, 20)
        distressed = Board(10, 20)
        for col in range(0, 10, 2):
            distressed.area[2, col] = True
        self.assertGreater(adapt.weights_for_board(empty)[1], adapt.weights_for_board(empty)[0])
        self.assertGreater(adapt.weights_for_board(distressed)[0], adapt.weights_for_board(distressed)[1])

        # Blend, +, conditional
        ortho_d = UniformDistribution(self.factory.classic_fixed(), seed=1)
        diag_d = UniformDistribution(self.factory.extended_fixed(), seed=2)
        blended = ortho_d.blend(diag_d, weight=0.75, seed=55)
        diag_frac = sum(1 for p in blended.sample_many(800) if isinstance(p, DiagonalPolyplet)) / 800.0
        self.assertGreater(diag_frac, 0.67)
        self.assertLess(diag_frac, 0.83)

        added = UniformDistribution(self.factory.classic_fixed(), seed=3) + UniformDistribution(
            self.factory.extended_fixed(), seed=4
        )
        added_frac = sum(1 for p in added.sample_many(800) if isinstance(p, DiagonalPolyplet)) / 800.0
        self.assertGreater(added_frac, 0.40)
        self.assertLess(added_frac, 0.60)

        cond = diag_d.conditional(lambda b, _h: b.get_max_height() >= 5, ortho_d, diag_d)
        low_b = Board(10, 20)
        high_b = Board(10, 20)
        high_b.area[10, 0] = True
        self.assertTrue(all(isinstance(p, DiagonalPolyplet) for p in cond.sample_many(15, board=low_b)))
        self.assertTrue(all(not isinstance(p, DiagonalPolyplet) for p in cond.sample_many(15, board=high_b)))


class TestEngineFSMWallKicksAndObservers(unittest.TestCase):
    def setUp(self):
        self.factory = ExTetrominoFactory()
        self.i_horiz = next(p for p in self.factory.classic_fixed() if isinstance(p, Box1x4Shape))
        self.i_vert = self.i_horiz.clone().rotateCW().reclassify()

    def test_fsm_lifecycle_and_observers(self):
        eng = ExTetrisEngine(distribution=UniformDistribution([self.i_horiz], seed=1), initial_speed_ms=1000)
        event_log = []
        eng.register_callback(lambda payload: event_log.append(payload["event"]))

        self.assertEqual(eng.state, GameState.READY)
        self.assertFalse(eng.move_left())
        self.assertTrue(eng.start())
        self.assertEqual(eng.state, GameState.RUNNING)
        self.assertTrue(eng.toggle_pause())
        self.assertEqual(eng.state, GameState.PAUSED)
        self.assertFalse(eng.rotate_cw())
        self.assertTrue(eng.toggle_pause())
        self.assertEqual(eng.state, GameState.RUNNING)

        # Trigger Game Over
        eng.board.area[1:4, 2:7] = True
        eng.current_piece = self.i_horiz.clone()
        eng.cursor = (0, 3)
        eng.hard_drop()
        self.assertEqual(eng.state, GameState.GAME_OVER)
        self.assertFalse(eng.pause())
        self.assertIn("game_over", event_log)
        self.assertIn("state_changed", event_log)

        eng.new_game()
        self.assertEqual(eng.state, GameState.RUNNING)

    def test_wall_kicks_left_right_and_disabled(self):
        # Right wall kick (0, -2)
        eng = ExTetrisEngine(distribution=UniformDistribution([self.i_vert], seed=2), enable_wall_kicks=True)
        eng.start()
        kicks = []
        eng.register_callback("piece_rotated", lambda p: kicks.append(p["kick_offset"]))
        eng.current_piece = self.i_vert.clone()
        eng.cursor = (2, 8)
        self.assertTrue(eng.rotate_cw())
        self.assertEqual(kicks[-1], (0, -2))
        self.assertEqual(eng.cursor, (2, 6))

        # Obstacle on left pushes kick (+1)
        eng.current_piece = self.i_vert.clone()
        eng.cursor = (4, 1)
        eng.board.area[4, 0] = True
        # Wait: 4x1 at col 1 rotated to 1x4 at col 1 fits in cols 1..4 without needing kick!
        # Put obstacle at col 4 -> cols 1..4 blocked -> kick (0, -1) puts at 0..3 -> blocked by (4,0)!
        # Put obstacle ONLY at (4, 4) and leave (4, 0) free -> (0,0) blocked at col 4, kick (0,-1) fits cols 0..3!
        eng.board.area[4, 0] = False
        eng.board.area[4, 4] = True
        self.assertTrue(eng.rotate_cw())
        self.assertEqual(kicks[-1], (0, -1))

        # With wall kicks disabled, right-wall rotation is rejected
        eng_no_kick = ExTetrisEngine(distribution=UniformDistribution([self.i_vert], seed=2), enable_wall_kicks=False)
        eng_no_kick.start()
        eng_no_kick.current_piece = self.i_vert.clone()
        eng_no_kick.cursor = (2, 8)
        self.assertFalse(eng_no_kick.rotate_cw())

    def test_scoring_and_level_speed_floor(self):
        eng = ExTetrisEngine(
            distribution=UniformDistribution([self.i_vert], seed=5),
            initial_speed_ms=200,
            speed_factor=0.92,
        )
        eng.start()
        self.assertTrue(eng.soft_drop())
        self.assertEqual(eng.score, 1)
        dist = eng.hard_drop()
        self.assertEqual(dist, 15)

        eng.new_game()
        for _ in range(3):
            eng.board.area[16:20, :9] = True
            eng.current_piece = self.i_vert.clone()
            eng.cursor = (0, 9)
            eng.hard_drop()
        self.assertEqual(eng.lines_cleared, 12)
        self.assertEqual(eng.level, 2)
        self.assertEqual(eng.drop_speed_ms, int(200 * 0.92))

        # Floor at 100ms even at high lines
        eng.lines_cleared = 200
        eng._recompute_level_and_speed()
        self.assertEqual(eng.drop_speed_ms, 100)


class TestRenderersAndCLIEntry(unittest.TestCase):
    def test_headless_and_cli_renderers_and_play_cli(self):
        factory = ExTetrominoFactory()
        eng = ExTetrisEngine(distribution=BagDistribution(factory.classic_one_sided(), seed=9))
        hr = create_renderer("headless")
        frames = hr.run(eng, steps=4, action_sequence=["LEFT", "CW", "HARD_DROP", "STEP"])
        self.assertGreaterEqual(len(frames), 4)
        self.assertIn("Score=", frames[-1])

        buf = io.StringIO()
        cli = CLIRenderer(stream=buf, use_ansi=True, tick_sleep=0.005)
        eng2 = ExTetrisEngine(distribution=BagDistribution(factory.classic_one_sided(), seed=9), initial_speed_ms=100)
        cli.run(eng2, max_ticks=2)
        output = buf.getvalue()
        self.assertIn("\033[2J\033[H", output)
        self.assertIn("ExTetris | State: RUNNING", output)
        self.assertTrue(cli.handle_key(eng2, "a"))
        self.assertTrue(cli.handle_key(eng2, "d"))
        self.assertTrue(cli.handle_key(eng2, "w"))
        self.assertTrue(cli.handle_key(eng2, "e"))
        self.assertTrue(cli.handle_key(eng2, "s"))
        self.assertTrue(cli.handle_key(eng2, " "))
        self.assertTrue(cli.handle_key(eng2, "p"))
        self.assertTrue(eng2.is_paused)
        self.assertFalse(cli.handle_key(eng2, "q"))

        # play.main CLI invocation in headless mode
        stdout_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture):
            rc = play.main(["--renderer", "headless", "--variant", "adaptive", "--seed", "7", "--steps", "8"])
        self.assertEqual(rc, 0)
        self.assertIn("Captured 9 headless frames", stdout_capture.getvalue())

    def test_optional_tk_graceful_degradation(self):
        orig_tk = sys.modules.get("tkinter", Ellipsis)
        sys.modules["tkinter"] = None
        try:
            with self.assertRaises(RuntimeError):
                TkinterRenderer()
        finally:
            if orig_tk is Ellipsis:
                sys.modules.pop("tkinter", None)
            else:
                sys.modules["tkinter"] = orig_tk


if __name__ == "__main__":
    unittest.main(verbosity=2)
