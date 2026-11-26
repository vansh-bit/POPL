from collections import Counter
import unittest

from extetris.board import Board
from extetris.distributions import (
    AdaptiveDifficultyDistribution,
    BagDistribution,
    MarkovDistribution,
    UniformDistribution,
    WeightedDistribution,
)
from extetris.shapes import DiagonalPolyplet, ExTetrominoFactory, FlatLandingShape


class TestDistributions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.classic = cls.factory.classic_one_sided()
        cls.all_fixed = cls.factory.all_fixed()

    def test_uniform_and_weighted_with_seeds(self):
        u1 = UniformDistribution(self.classic, seed=42)
        u2 = UniformDistribution(self.classic, seed=42)
        self.assertEqual([p.piece_id for p in u1.sample_many(50)], [p.piece_id for p in u2.sample_many(50)])

        w = WeightedDistribution(self.classic[:3], [10, 1, 1], seed=7)
        counts = Counter(p.piece_id for p in w.sample_many(1200))
        self.assertGreater(counts[self.classic[0].piece_id], 900)

    def test_bag_markov_and_adaptive(self):
        bag = BagDistribution(self.classic, seed=10)
        draws = bag.sample_many(14)
        self.assertEqual(len({p.piece_id for p in draws[:7]}), 7)
        self.assertEqual(len({p.piece_id for p in draws[7:]}), 7)

        markov = MarkovDistribution(self.classic, repeat_penalty=0.0, seed=11)
        seq = [p.piece_id for p in markov.sample_many(150)]
        self.assertTrue(all(seq[i] != seq[i + 1] for i in range(len(seq) - 1)))

        flat = next(p for p in self.all_fixed if isinstance(p, FlatLandingShape))
        hard = next(p for p in self.all_fixed if p.landing_holes() >= 4)
        adapt = AdaptiveDifficultyDistribution([flat, hard], seed=12)
        empty = Board(10, 20)
        bad = Board(10, 20)
        for c in range(0, 10, 2):
            bad.area[2, c] = True
        self.assertGreater(adapt.weights_for_board(empty)[1], adapt.weights_for_board(empty)[0])
        self.assertGreater(adapt.weights_for_board(bad)[0], adapt.weights_for_board(bad)[1])

    def test_combinators_reproducibility(self):
        d1 = (
            BagDistribution(self.all_fixed, seed=55).filter(lambda p: isinstance(p, FlatLandingShape), seed=55)
            >> (lambda p: p.clone().rotateCW().reclassify())
        )
        d2 = (
            BagDistribution(self.all_fixed, seed=55).filter(lambda p: isinstance(p, FlatLandingShape), seed=55)
            >> (lambda p: p.clone().rotateCW().reclassify())
        )
        self.assertEqual([p.piece_id for p in d1.sample_many(25)], [p.piece_id for p in d2.sample_many(25)])

        ortho = UniformDistribution(self.factory.classic_fixed(), seed=1)
        diag = UniformDistribution(self.factory.extended_fixed(), seed=2)
        blended = ortho.blend(diag, weight=0.8, seed=3)
        frac = sum(1 for p in blended.sample_many(600) if isinstance(p, DiagonalPolyplet)) / 600.0
        self.assertGreater(frac, 0.70)

        added = UniformDistribution(self.factory.classic_fixed(), seed=4) + UniformDistribution(
            self.factory.extended_fixed(), seed=5
        )
        self.assertGreater(sum(1 for p in added.sample_many(400) if isinstance(p, DiagonalPolyplet)) / 400.0, 0.35)

        cond = diag.conditional(lambda b, _h: b.get_max_height() >= 8, ortho, diag)
        high = Board(10, 20)
        high.area[10, 0] = True
        self.assertTrue(all(not isinstance(p, DiagonalPolyplet) for p in cond.sample_many(15, board=high)))
