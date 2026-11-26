"""Seeded tests for Board heuristic metrics and Functional-OO ShapeDistributions."""

import unittest
from collections import Counter

from board import Board
from factory import ExTetrominoFactory
from hierarchy import Box1x4Shape, FlatLandingShape, MultiCavityShape, OrthogonalTetromino, DiagonalPolyplet
from distributions import (
    UniformDistribution,
    WeightedDistribution,
    BagDistribution,
    AdaptiveDifficultyDistribution,
    MarkovDistribution,
)


class TestBoardMetrics(unittest.TestCase):
    def test_heights_holes_bumpiness_and_ghost(self):
        b = Board(width=6, height=10)
        self.assertEqual(b.get_max_height(), 0)
        self.assertEqual(b.count_holes(), 0)
        self.assertEqual(b.get_bumpiness(), 0)

        # Build explicit column profile:
        # col 0: block at row 7 (height 3) -> holes below at rows 8, 9 (2 holes)
        # col 1: blocks at rows 8, 9 (height 2) -> 0 holes
        # col 2: block at row 9 (height 1) -> 0 holes
        # cols 3..5: empty (height 0)
        b.area[7, 0] = True
        b.area[8, 1] = True
        b.area[9, 1] = True
        b.area[9, 2] = True

        self.assertEqual(b.column_heights(), [3, 2, 1, 0, 0, 0])
        self.assertEqual(b.get_max_height(), 3)
        self.assertEqual(b.count_holes(), 2)
        # |3-2| + |2-1| + |1-0| + |0-0| + |0-0| = 3
        self.assertEqual(b.get_bumpiness(), 3)

        # Ghost row for 1x4 horizontal I-piece at col 2: blocked by (9, 2) -> lands at row 8!
        factory = ExTetrominoFactory()
        i_horiz = next(p for p in factory.classic_fixed() if isinstance(p, Box1x4Shape))
        self.assertTrue(b.is_valid_position(i_horiz, (0, 2)))
        self.assertEqual(b.get_ghost_row(i_horiz, (0, 2)), 8)
        # At col 1, blocked by (8, 1) -> lands at row 7
        self.assertEqual(b.get_ghost_row(i_horiz, (0, 1)), 7)

        b_clone = b.clone()
        b_clone.area[0, 0] = True
        self.assertFalse(b.area[0, 0])


class TestSeededDistributions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.classic = cls.factory.classic_one_sided()
        cls.all_fixed = cls.factory.all_fixed()

    def test_uniform_and_seed_reproducibility(self):
        d1 = UniformDistribution(self.classic, seed=2026)
        d2 = UniformDistribution(self.classic, seed=2026)
        s1 = [p.piece_id for p in d1.sample_many(100)]
        s2 = [p.piece_id for p in d2.sample_many(100)]
        self.assertEqual(s1, s2)
        self.assertEqual(len(set(s1)), 7)

    def test_weighted_statistical_proportions(self):
        shapes = self.classic[:3]
        d = WeightedDistribution(shapes, weights=[10.0, 1.0, 1.0], seed=99)
        counts = Counter(p.piece_id for p in d.sample_many(2400))
        # Expected: ~2000 for shapes[0], ~200 each for shapes[1], shapes[2]
        self.assertGreater(counts[shapes[0].piece_id], 1850)
        self.assertLess(counts[shapes[1].piece_id], 300)
        self.assertLess(counts[shapes[2].piece_id], 300)

        with self.assertRaises(ValueError):
            WeightedDistribution(shapes, weights=[0.0, 0.0, 0.0])

    def test_bag_distribution_guarantees(self):
        bag1 = BagDistribution(self.classic, bag_multiplier=1, seed=7)
        draws = bag1.sample_many(21)  # 3 full 7-bags
        for chunk_idx in range(3):
            chunk_ids = [p.piece_id for p in draws[chunk_idx * 7:(chunk_idx + 1) * 7]]
            self.assertEqual(len(set(chunk_ids)), 7)

        bag2 = BagDistribution(self.classic, bag_multiplier=2, seed=7)
        draws2 = bag2.sample_many(14)
        counts2 = Counter(p.piece_id for p in draws2)
        self.assertTrue(all(v == 2 for v in counts2.values()))

    def test_adaptive_difficulty_distress_response(self):
        flat = next(p for p in self.all_fixed if isinstance(p, FlatLandingShape))
        multi = next(p for p in self.all_fixed if p.landing_holes() >= 4)
        adapt_a = AdaptiveDifficultyDistribution([flat, multi], seed=123)
        adapt_b = AdaptiveDifficultyDistribution([flat, multi], seed=123)

        empty_board = Board(10, 20)
        self.assertAlmostEqual(adapt_a.compute_distress(empty_board), 0.0)
        low_weights = adapt_a.weights_for_board(empty_board)
        self.assertGreater(low_weights[1], low_weights[0])  # multi-cavity favored when safe

        # High distress board: tall stack + many holes + high bumpiness
        bad_board = Board(10, 20)
        for col in range(0, 10, 2):
            bad_board.area[2, col] = True  # height 18, 17 holes per even col, high bumpiness
        distress = adapt_a.compute_distress(bad_board)
        self.assertGreater(distress, 0.85)
        high_weights = adapt_a.weights_for_board(bad_board)
        self.assertGreater(high_weights[0], high_weights[1])  # flat shape strongly favored

        # Reproducibility on distressed board
        seq_a = [p.piece_id for p in adapt_a.sample_many(40, board=bad_board)]
        seq_b = [p.piece_id for p in adapt_b.sample_many(40, board=bad_board)]
        self.assertEqual(seq_a, seq_b)
        self.assertGreater(seq_a.count(flat.piece_id), seq_a.count(multi.piece_id))

    def test_markov_transitions_and_anti_repeat(self):
        a, b = self.classic[0], self.classic[1]
        # Deterministic flip-flop transition matrix
        m = MarkovDistribution([a, b], transition_matrix=[[0.0, 1.0], [1.0, 0.0]], seed=5)
        seq = [p.piece_id for p in m.sample_many(10)]
        for i in range(len(seq) - 1):
            self.assertNotEqual(seq[i], seq[i + 1])

        # Default anti-repeat with repeat_penalty=0.0 forbids consecutive duplicates
        m2 = MarkovDistribution(self.classic, repeat_penalty=0.0, seed=11)
        seq2 = [p.piece_id for p in m2.sample_many(200)]
        for i in range(len(seq2) - 1):
            self.assertNotEqual(seq2[i], seq2[i + 1])

    def test_combinators_filter_map_blend_add_rshift_conditional(self):
        # 1. filter()
        flat_only = UniformDistribution(self.all_fixed, seed=42).filter(
            lambda p: isinstance(p, FlatLandingShape)
        )
        sampled_flat = flat_only.sample_many(60)
        self.assertTrue(all(isinstance(p, FlatLandingShape) for p in sampled_flat))

        with self.assertRaises(ValueError):
            UniformDistribution(self.classic, seed=1).filter(lambda p: isinstance(p, DiagonalPolyplet))

        # 2. >> / map()
        rotated_i = UniformDistribution([self.classic[0]], seed=10) >> (
            lambda p: p.clone().rotateCW().reclassify()
        )
        for p in rotated_i.sample_many(5):
            self.assertEqual(p.bounding_box(), (4, 1))

        # 3. blend() and + (and seed reproducibility of composed pipelines)
        ortho_dist = UniformDistribution(self.factory.classic_fixed(), seed=100)
        diag_dist = UniformDistribution(self.factory.extended_fixed(), seed=200)
        blended_1 = ortho_dist.blend(diag_dist, weight=0.8, seed=777)
        blended_2 = UniformDistribution(self.factory.classic_fixed(), seed=100).blend(
            UniformDistribution(self.factory.extended_fixed(), seed=200),
            weight=0.8,
            seed=777,
        )
        seq_1 = [p.piece_id for p in blended_1.sample_many(100)]
        seq_2 = [p.piece_id for p in blended_2.sample_many(100)]
        self.assertEqual(seq_1, seq_2)

        diag_ratio = sum(1 for p in blended_1.sample_many(1000) if isinstance(p, DiagonalPolyplet)) / 1000.0
        self.assertGreater(diag_ratio, 0.72)
        self.assertLess(diag_ratio, 0.88)

        added = UniformDistribution(self.factory.classic_fixed(), seed=300) + UniformDistribution(
            self.factory.extended_fixed(), seed=400
        )
        added_diag_ratio = sum(1 for p in added.sample_many(1000) if isinstance(p, DiagonalPolyplet)) / 1000.0
        self.assertGreater(added_diag_ratio, 0.42)
        self.assertLess(added_diag_ratio, 0.58)

        # 4. conditional() dynamic switching
        safe_dist = UniformDistribution([p for p in self.all_fixed if isinstance(p, FlatLandingShape)], seed=1)
        hard_dist = UniformDistribution([p for p in self.all_fixed if isinstance(p, DiagonalPolyplet)], seed=2)
        cond = hard_dist.conditional(lambda board, _hist: board.get_max_height() >= 10, safe_dist, hard_dist)

        low_board = Board(10, 20)
        high_board = Board(10, 20)
        high_board.area[5, 0] = True  # height = 15 >= 10

        self.assertTrue(all(isinstance(p, DiagonalPolyplet) for p in cond.sample_many(20, board=low_board)))
        self.assertTrue(all(isinstance(p, FlatLandingShape) for p in cond.sample_many(20, board=high_board)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
