import unittest

from extetris.board import Board
from extetris.shapes import Box1x4Shape, ExTetrominoFactory


class TestBoard(unittest.TestCase):
    def test_negative_indices_and_boundaries(self):
        b = Board(width=10, height=20)
        i_horiz = next(p for p in ExTetrominoFactory().classic_fixed() if isinstance(p, Box1x4Shape))
        self.assertTrue(b.collision(i_horiz, (0, -1)))
        self.assertTrue(b.collision(i_horiz, (-1, 0)))
        self.assertTrue(b.collision(i_horiz, (0, 7)))
        self.assertTrue(b.collision(i_horiz, (20, 0)))
        self.assertFalse(b.collision(i_horiz, (0, 6)))

    def test_collisions_and_insert_remove(self):
        b = Board(width=10, height=20)
        i_horiz = next(p for p in ExTetrominoFactory().classic_fixed() if isinstance(p, Box1x4Shape))
        b.insertShape(i_horiz, 19, 2)
        self.assertTrue(b.collision(i_horiz, (19, 0)))
        self.assertFalse(b.collision(i_horiz, (19, 6)))
        b.removeShape(i_horiz, 19, 2)
        self.assertFalse(b.area.any())

    def test_line_clearing_and_metrics(self):
        b = Board(width=6, height=10)
        b.area[7, 0] = True
        b.area[8, 1] = True
        b.area[9, 1] = True
        b.area[9, 2] = True
        self.assertEqual(b.column_heights(), [3, 2, 1, 0, 0, 0])
        self.assertEqual(b.get_max_height(), 3)
        self.assertEqual(b.count_holes(), 2)
        self.assertEqual(b.get_bumpiness(), 3)

        b.area[7, :] = True
        b.area[9, :] = True
        cleared = b.clear_full_lines()
        self.assertEqual(cleared, 2)
        self.assertTrue(b.area[9, 1])
        self.assertFalse(b.area[9, 2])
