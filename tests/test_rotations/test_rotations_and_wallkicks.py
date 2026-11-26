import unittest
import numpy as np

from extetris.distributions import UniformDistribution
from extetris.engine import ExTetrisEngine
from extetris.shapes import Box1x4Shape, Box4x1Shape, ExTetrominoFactory


class TestRotationsAndWallKicks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.pieces = cls.factory.all_fixed()
        cls.i_horiz = next(p for p in cls.pieces if isinstance(p, Box1x4Shape))
        cls.i_vert = cls.i_horiz.clone().rotateCW().reclassify()

    def test_all_four_rotations_across_110_shapes(self):
        for p in self.pieces:
            orig = p.coords
            m0 = p.to_matrix()
            cur = p.clone()
            for k in range(1, 5):
                cur.rotateCW()
                self.assertTrue(np.array_equal(cur.to_matrix(), np.rot90(m0, k=-k)))
            self.assertEqual(cur.coords, orig)
            cur.rotateCW()
            cur.rotateAntiCW()
            self.assertEqual(cur.coords, orig)

    def test_wall_kicks_and_invalid_rotations(self):
        eng = ExTetrisEngine(distribution=UniformDistribution([self.i_vert], seed=1), enable_wall_kicks=True)
        eng.start()
        eng.current_piece = self.i_vert.clone()
        eng.cursor = (2, 8)
        self.assertTrue(eng.rotate_cw())
        self.assertIsInstance(eng.current_piece, Box1x4Shape)
        self.assertEqual(eng.cursor, (2, 6))

        eng.current_piece = self.i_vert.clone()
        eng.cursor = (5, 8)
        self.assertTrue(eng.rotate_ccw())
        self.assertEqual(eng.cursor, (5, 6))

        eng.board.area[8, :] = True
        eng.board.area[8, 5] = False
        eng.current_piece = self.i_vert.clone()
        eng.cursor = (8, 5)
        self.assertFalse(eng.rotate_cw())
        self.assertIsInstance(eng.current_piece, Box4x1Shape)

        eng_off = ExTetrisEngine(distribution=UniformDistribution([self.i_vert], seed=1), enable_wall_kicks=False)
        eng_off.start()
        eng_off.current_piece = self.i_vert.clone()
        eng_off.cursor = (2, 8)
        self.assertFalse(eng_off.rotate_cw())
