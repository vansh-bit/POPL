# hierarchy.py: Multi-axis ExTetromino classification hierarchy
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from .base import ExTetromino


class BoundingBoxShape(ExTetromino):
    """Base class for ExTetrominoes classified by (height, width) bounding box."""

    expected_bbox = None

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if self.expected_bbox is not None and self.bounding_box() != self.expected_bbox:
            raise ValueError(
                f"{self.__class__.__name__} requires bounding box {self.expected_bbox}, "
                f"got {self.bounding_box()}"
            )


class Box1x4Shape(BoundingBoxShape):
    expected_bbox = (1, 4)


class Box4x1Shape(BoundingBoxShape):
    expected_bbox = (4, 1)


class Box2x2Shape(BoundingBoxShape):
    expected_bbox = (2, 2)


class Box2x3Shape(BoundingBoxShape):
    expected_bbox = (2, 3)


class Box3x2Shape(BoundingBoxShape):
    expected_bbox = (3, 2)


class Box2x4Shape(BoundingBoxShape):
    expected_bbox = (2, 4)


class Box4x2Shape(BoundingBoxShape):
    expected_bbox = (4, 2)


class Box3x3Shape(BoundingBoxShape):
    expected_bbox = (3, 3)


class Box3x4Shape(BoundingBoxShape):
    expected_bbox = (3, 4)


class Box4x3Shape(BoundingBoxShape):
    expected_bbox = (4, 3)


class Box4x4Shape(BoundingBoxShape):
    expected_bbox = (4, 4)


BOUNDING_BOX_CLASSES = {
    (1, 4): Box1x4Shape,
    (4, 1): Box4x1Shape,
    (2, 2): Box2x2Shape,
    (2, 3): Box2x3Shape,
    (3, 2): Box3x2Shape,
    (2, 4): Box2x4Shape,
    (4, 2): Box4x2Shape,
    (3, 3): Box3x3Shape,
    (3, 4): Box3x4Shape,
    (4, 3): Box4x3Shape,
    (4, 4): Box4x4Shape,
}


class MorphologyShape(ExTetromino):
    """Base class for topological connectivity classification."""


class OrthogonalTetromino(MorphologyShape):
    """Edge-connected (4-neighborhood) tetromino."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if not self.is_orthogonal():
            raise ValueError(f"{self.__class__.__name__} requires 4-connected cells.")


class DiagonalPolyplet(MorphologyShape):
    """Corner-connected (8-neighborhood, non-4-connected) extended polyplet."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if not self.is_diagonal():
            raise ValueError(f"{self.__class__.__name__} requires at least one corner-only link.")


class LandingCavityShape(ExTetromino):
    """Base class classifying shapes by trapped holes produced while landing."""


class FlatLandingShape(LandingCavityShape):
    """Produces 0 landing holes in its current orientation."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if self.landing_holes() != 0:
            raise ValueError(f"FlatLandingShape requires 0 landing holes, got {self.landing_holes()}.")


class SingleCavityShape(LandingCavityShape):
    """Produces exactly 1 landing hole in its current orientation."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if self.landing_holes() != 1:
            raise ValueError(f"SingleCavityShape requires 1 landing hole, got {self.landing_holes()}.")


class MultiCavityShape(LandingCavityShape):
    """Produces 2 or more landing holes in its current orientation."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if self.landing_holes() < 2:
            raise ValueError(f"MultiCavityShape requires >=2 landing holes, got {self.landing_holes()}.")


_COMPOSITE_CLASS_CACHE = {}


def _clone_reclassified(self):
    return classify_extetromino(self.coords, piece_id=self.piece_id, name=self.name)


def get_composite_class(box_cls, morph_cls, cavity_cls):
    key = (box_cls, morph_cls, cavity_cls)
    if key not in _COMPOSITE_CLASS_CACHE:
        cls_name = f"{box_cls.__name__}_{morph_cls.__name__}_{cavity_cls.__name__}"
        composite_cls = type(
            cls_name,
            (box_cls, morph_cls, cavity_cls),
            {"clone": _clone_reclassified, "reclassify": _clone_reclassified},
        )
        _COMPOSITE_CLASS_CACHE[key] = composite_cls
    return _COMPOSITE_CLASS_CACHE[key]


def classify_extetromino(coords, piece_id=None, name=None):
    """Instantiate an ExTetromino as the exact composite (Box, Morphology, Cavity) subclass."""
    probe = ExTetromino(coords=coords, piece_id=piece_id, name=name)
    bbox = probe.bounding_box()
    if bbox not in BOUNDING_BOX_CLASSES:
        raise ValueError(f"Unsupported bounding box {bbox} for 4-polyplet classification.")
    box_cls = BOUNDING_BOX_CLASSES[bbox]
    morph_cls = OrthogonalTetromino if probe.is_orthogonal() else DiagonalPolyplet
    holes = probe.landing_holes()
    if holes == 0:
        cavity_cls = FlatLandingShape
    elif holes == 1:
        cavity_cls = SingleCavityShape
    else:
        cavity_cls = MultiCavityShape

    composite_cls = get_composite_class(box_cls, morph_cls, cavity_cls)
    return composite_cls(coords=probe.coords, piece_id=piece_id, name=name)
