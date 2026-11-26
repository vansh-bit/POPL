import sys
from pathlib import Path
import unittest

ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from distributions import UniformDistribution
from engine import ExTetrisEngine, GameState
from factory import ExTetrominoFactory
from hierarchy import Box1x4Shape


class TestEngineFSM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.i_horiz = next(p for p in cls.factory.classic_fixed() if isinstance(p, Box1x4Shape))
        cls.i_vert = cls.i_horiz.clone().rotateCW().reclassify()

    def test_fsm_transitions_pause_resume_and_gameover(self):
        eng = ExTetrisEngine(distribution=UniformDistribution([self.i_horiz], seed=1))
        events = []
        eng.register_callback(lambda p: events.append(p["event"]))

        self.assertEqual(eng.state, GameState.READY)
        self.assertFalse(eng.move_left())
        self.assertTrue(eng.start())
        self.assertEqual(eng.state, GameState.RUNNING)
        self.assertTrue(eng.pause())
        self.assertTrue(eng.is_paused)
        self.assertFalse(eng.soft_drop())
        self.assertTrue(eng.resume())
        self.assertFalse(eng.is_paused)

        eng.board.area[1:4, 2:7] = True
        eng.current_piece = self.i_horiz.clone()
        eng.cursor = (0, 3)
        eng.hard_drop()
        self.assertEqual(eng.state, GameState.GAME_OVER)
        self.assertTrue(eng.is_game_over)
        self.assertIn("game_over", events)

    def test_level_progression_and_speed_rounding(self):
        eng = ExTetrisEngine(distribution=UniformDistribution([self.i_vert], seed=2), initial_speed_ms=500)
        eng.start()
        eng.speed_up()
        self.assertEqual(eng.drop_speed_ms, 450)
        eng.slow_down()
        self.assertEqual(eng.drop_speed_ms, 495)

        eng.new_game()
        for _ in range(3):
            eng.board.area[16:20, :9] = True
            eng.current_piece = self.i_vert.clone()
            eng.cursor = (0, 9)
            eng.hard_drop()
        self.assertEqual(eng.lines_cleared, 12)
        self.assertEqual(eng.level, 2)
        self.assertEqual(eng.drop_speed_ms, 460)
