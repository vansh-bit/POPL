import unittest

from extetris.shapes import (
    BOUNDING_BOX_CLASSES,
    Box1x4Shape,
    Box3x4Shape,
    Box4x1Shape,
    DiagonalPolyplet,
    ExTetromino,
    ExTetrominoFactory,
    FlatLandingShape,
    MultiCavityShape,
    OrthogonalTetromino,
    SingleCavityShape,
    is_connected,
    normalize_coords,
)


class TestShapeGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.pieces = cls.factory.all_fixed()

    def test_110_unique_shapes_and_groupings(self):
        self.assertEqual(len(self.pieces), 110)
        self.assertEqual(len(self.factory.all_one_sided()), 34)
        self.assertEqual(len(self.factory.all_free()), 22)
        self.assertEqual(len(self.factory.classic_one_sided()), 7)
        self.assertEqual(len(self.factory.classic_fixed()), 19)
        self.assertEqual(len(self.factory.extended_one_sided()), 27)
        self.assertEqual(len(self.factory.extended_fixed()), 91)

    def test_connectivity_normalization_and_no_duplicate_ids(self):
        ids = [p.piece_id for p in self.pieces]
        coords = [p.coords for p in self.pieces]
        self.assertEqual(ids, list(range(1, 111)))
        self.assertEqual(len(set(coords)), 110)
        for p in self.pieces:
            self.assertEqual(len(p.coords), 4)
            self.assertEqual(min(r for r, _ in p.coords), 0)
            self.assertEqual(min(c for _, c in p.coords), 0)
            self.assertTrue(is_connected(p.coords, diagonal=True))

        norm = normalize_coords([(-4, 9), (-4, 10), (-3, 10), (-2, 11)])
        self.assertEqual(norm, ((0, 0), (0, 1), (1, 1), (2, 2)))


class TestShapeHierarchy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = ExTetrominoFactory()
        cls.pieces = cls.factory.all_fixed()

    def test_all_11_bounding_boxes_morphology_and_cavities(self):
        bbox_counts = {}
        for p in self.pieces:
            bbox = p.bounding_box()
            bbox_counts[bbox] = bbox_counts.get(bbox, 0) + 1
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

        self.assertEqual(len(bbox_counts), 11)
        self.assertEqual(bbox_counts[(3, 4)], 10)
        self.assertEqual(bbox_counts[(4, 3)], 10)
        self.assertEqual(bbox_counts[(1, 4)], 1)
        self.assertEqual(bbox_counts[(4, 1)], 1)

    def test_landing_hole_profiles_and_invalid_invariants(self):
        i_piece = next(p for p in self.pieces if isinstance(p, Box1x4Shape))
        self.assertEqual(i_piece.landing_hole_profile(), (0, 0, 0, 0))
        t_piece = ExTetromino(((0, 0), (0, 1), (0, 2), (1, 1)))
        self.assertEqual(t_piece.landing_hole_profile(), (2, 1, 0, 1))

        with self.assertRaises(ValueError):
            ExTetromino(((0, 0), (0, 2), (0, 3), (0, 4)))
        with self.assertRaises(ValueError):
            Box3x4Shape(((0, 0), (0, 1), (1, 0), (1, 1)))
        with self.assertRaises(ValueError):
            Box4x1Shape(((0, 0), (0, 1), (0, 2), (0, 3)))
