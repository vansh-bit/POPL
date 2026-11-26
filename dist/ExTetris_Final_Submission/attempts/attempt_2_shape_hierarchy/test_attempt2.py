"""Verification suite for Attempt 2 (Coordinate Shape Hierarchy & 110-Shape Generator)."""

import unittest
import numpy as np

from shape import Shape, ExTetromino, is_connected, normalize_coords
from hierarchy import (
    BOUNDING_BOX_CLASSES,
    Box1x4Shape,
    Box4x1Shape,
    Box3x4Shape,
    Box4x3Shape,
    OrthogonalTetromino,
    DiagonalPolyplet,
    FlatLandingShape,
    SingleCavityShape,
    MultiCavityShape,
    classify_extetromino,
)
from factory import ExTetrominoFactory
from board import Board
from engine import TetrisEngine


class TestAttempt2ShapeFactoryAndHierarchy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.all_pieces = cls.factory.all_fixed()

    def test_110_unique_connected_normalized_shapes(self):
        self.assertEqual(len(self.all_pieces), 110)
        self.assertEqual(len(self.factory.all_one_sided()), 34)
        self.assertEqual(len(self.factory.all_free()), 22)
        self.assertEqual(len(self.factory.classic_one_sided()), 7)
        self.assertEqual(len(self.factory.classic_fixed()), 19)
        self.assertEqual(len(self.factory.extended_one_sided()), 27)
        self.assertEqual(len(self.factory.extended_fixed()), 91)

        ids = [p.piece_id for p in self.all_pieces]
        coords = [p.coords for p in self.all_pieces]
        self.assertEqual(ids, list(range(1, 111)))
        self.assertEqual(len(set(coords)), 110)
        for p in self.all_pieces:
            self.assertEqual(len(p.coords), 4)
            self.assertEqual(min(r for r, _ in p.coords), 0)
            self.assertEqual(min(c for _, c in p.coords), 0)
            self.assertTrue(is_connected(p.coords, diagonal=True))

    def test_bounding_box_morphology_and_cavity_classification(self):
        bboxes = {}
        for p in self.all_pieces:
            bbox = p.bounding_box()
            bboxes[bbox] = bboxes.get(bbox, 0) + 1
            self.assertIsInstance(p, BOUNDING_BOX_CLASSES[bbox])
            if p.is_orthogonal():
                self.assertIsInstance(p, OrthogonalTetromino)
                self.assertNotIsInstance(p, DiagonalPolyplet)
            else:
                self.assertIsInstance(p, DiagonalPolyplet)
                self.assertNotIsInstance(p, OrthogonalTetromino)
            holes = p.landing_holes()
            if holes == 0:
                self.assertIsInstance(p, FlatLandingShape)
            elif holes == 1:
                self.assertIsInstance(p, SingleCavityShape)
            else:
                self.assertIsInstance(p, MultiCavityShape)

        # Ensure 3x4 and 4x3 and 4x1 are genuinely populated
        self.assertEqual(bboxes[(3, 4)], 10)
        self.assertEqual(bboxes[(4, 3)], 10)
        self.assertEqual(bboxes[(1, 4)], 1)
        self.assertEqual(bboxes[(4, 1)], 1)

    def test_rotations_and_reclassification(self):
        for p in self.all_pieces:
            orig = p.coords
            rot = p.clone()
            rot.rotateCW()
            rot.rotateAntiCW()
            self.assertEqual(rot.coords, orig)
            for _ in range(4):
                rot.rotateCW()
            self.assertEqual(rot.coords, orig)

        i_horiz = next(p for p in self.all_pieces if isinstance(p, Box1x4Shape))
        i_vert = i_horiz.clone().rotateCW().reclassify()
        self.assertIsInstance(i_vert, Box4x1Shape)
        self.assertIsInstance(i_vert, FlatLandingShape)

    def test_invalid_subclass_and_extetromino_rejected(self):
        with self.assertRaises(ValueError):
            ExTetromino(((0, 0), (0, 2), (0, 3), (0, 4)))
        with self.assertRaises(ValueError):
            Box3x4Shape(((0, 0), (0, 1), (1, 0), (1, 1)))


class TestAttempt2BoardAndEngine(unittest.TestCase):
    def test_board_boundaries_and_collisions(self):
        board = Board(width=10, height=20)
        i_horiz = classify_extetromino(((0, 0), (0, 1), (0, 2), (0, 3)))
        self.assertTrue(board.collision(i_horiz, (0, -1)))
        self.assertTrue(board.collision(i_horiz, (-1, 0)))
        self.assertTrue(board.collision(i_horiz, (0, 7)))
        self.assertTrue(board.collision(i_horiz, (20, 0)))
        self.assertFalse(board.collision(i_horiz, (0, 6)))

        board.insertShape(i_horiz, 19, 0)
        self.assertTrue(board.collision(i_horiz, (19, 2)))
        self.assertFalse(board.collision(i_horiz, (19, 4)))

    def test_multiline_clear_non_adjacent(self):
        board = Board(width=10, height=20)
        board.area[16, 0] = True
        board.area[17, :] = True
        board.area[18, 1] = True
        board.area[19, :] = True
        cleared = board.clear_full_lines()
        self.assertEqual(cleared, 2)
        self.assertTrue(board.area[18, 0])
        self.assertTrue(board.area[19, 1])

    def test_engine_headless_gameplay_and_gameover(self):
        factory = ExTetrominoFactory()
        eng = TetrisEngine(piece_pool=factory.all_fixed(), factory=factory, headless=True, seed=42)
        i_horiz = next(p for p in factory.all_fixed() if isinstance(p, Box1x4Shape))
        eng.new_piece(i_horiz.clone())
        self.assertTrue(eng.move_left())
        self.assertTrue(eng.move_right())
        self.assertTrue(eng.rotate_CW())
        self.assertIsInstance(eng.piece, Box4x1Shape)
        self.assertTrue(eng.rotate_AntiCW())
        self.assertIsInstance(eng.piece, Box1x4Shape)

        # Line clear via drop + lock step
        eng.new_game()
        eng.board.area[19, :6] = True
        eng.new_piece(i_horiz.clone())
        eng.cursor = (0, 6)
        eng.drop_piece()
        eng.move_down_step(accelerated=True)
        self.assertEqual(eng.deleted_lines, 1)

        # Game over when spawn columns are stacked (without pre-filling entire rows)
        eng.new_game()
        eng.board.area[1:4, 3:8] = True
        eng.new_piece(i_horiz.clone())
        eng.move_down_step(accelerated=True)
        self.assertTrue(eng.game_over_status)
        eng.new_game()
        self.assertFalse(eng.game_over_status)

    def test_tkinter_gui_smoke(self):
        factory = ExTetrominoFactory()
        eng = TetrisEngine(piece_pool=factory.classic_one_sided(), factory=factory, headless=False, seed=1)
        eng.window.update_idletasks()
        eng.window.destroy()


if __name__ == "__main__":
    unittest.main(verbosity=2)
