# base.py: Coordinate-based Shape and ExTetromino base classes
# Based on starter design Copyright (C) 2024 Ramprasad S. Joshi
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from collections import deque
import numpy


def normalize_coords(coords):
    """Translate (r, c) coordinates so min_r == 0 and min_c == 0, sorted canonically."""
    pts = [(int(r), int(c)) for r, c in coords]
    if not pts:
        raise ValueError("Shape must contain at least one coordinate.")
    if len(set(pts)) != len(pts):
        raise ValueError("Shape coordinates must not contain duplicates.")
    min_r = min(r for r, _ in pts)
    min_c = min(c for _, c in pts)
    return tuple(sorted((r - min_r, c - min_c) for r, c in pts))


def is_connected(coords, diagonal=True):
    """Return True if all coordinates form a single connected component (8- or 4-connected)."""
    pts = set(coords)
    if not pts:
        return False
    start = next(iter(pts))
    visited = {start}
    queue = deque([start])
    neighbors = (
        [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if diagonal
        else [(-1, 0), (1, 0), (0, -1), (0, 1)]
    )
    while queue:
        r, c = queue.popleft()
        for dr, dc in neighbors:
            nxt = (r + dr, c + dc)
            if nxt in pts and nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return len(visited) == len(pts)


class Shape(object):
    """Coordinate-based geometric polyomino/polyplet anchored at (0, 0)."""

    def __init__(self, coords=None, piece_id=None, name=None):
        if coords is None:
            coords = ((0, 0), (0, 1), (0, 2), (0, 3))
        self.coords = normalize_coords(coords)
        self._coord_set = frozenset(self.coords)
        self.piece_id = piece_id
        self.name = name or self.__class__.__name__

    def clone(self):
        return self.__class__(self.coords, piece_id=self.piece_id, name=self.name)

    def bounding_box(self):
        height = max(r for r, _ in self.coords) + 1
        width = max(c for _, c in self.coords) + 1
        return (height, width)

    @property
    def height(self):
        return self.bounding_box()[0]

    @property
    def width(self):
        return self.bounding_box()[1]

    def _set_coords(self, new_coords):
        self.coords = normalize_coords(new_coords)
        self._coord_set = frozenset(self.coords)

    def rotateCW(self):
        """Rotate 90 degrees clockwise in (row, col) screen coordinates and re-normalize."""
        self._set_coords((c, -r) for r, c in self.coords)
        return self

    def rotateAntiCW(self):
        """Rotate 90 degrees counter-clockwise in (row, col) screen coordinates and re-normalize."""
        self._set_coords((-c, r) for r, c in self.coords)
        return self

    def fliplr(self):
        """Reflect horizontally across columns and re-normalize."""
        self._set_coords((r, -c) for r, c in self.coords)
        return self

    def flipud(self):
        """Reflect vertically across rows and re-normalize."""
        self._set_coords((-r, c) for r, c in self.coords)
        return self

    def to_matrix(self):
        """Materialize a 2D boolean numpy array on demand from coordinates."""
        h, w = self.bounding_box()
        mat = numpy.zeros((h, w), dtype=bool)
        for r, c in self.coords:
            mat[r, c] = True
        return mat

    @property
    def matrix(self):
        """Read-only computed view for compatibility with matrix consumers."""
        return self.to_matrix()

    def landing_holes(self):
        """
        Count empty cells within the bounding box lying strictly below
        at least one occupied cell in the same column.
        """
        h, w = self.bounding_box()
        holes = 0
        for col in range(w):
            col_rows = [r for r, c in self.coords if c == col]
            if not col_rows:
                continue
            top_r = min(col_rows)
            for row in range(top_r + 1, h):
                if (row, col) not in self._coord_set:
                    holes += 1
        return holes

    def landing_hole_profile(self):
        """Return (h0, h90, h180, h270) landing hole counts across all 4 CW rotations."""
        probe = Shape(self.coords)
        profile = []
        for _ in range(4):
            profile.append(probe.landing_holes())
            probe.rotateCW()
        return tuple(profile)

    def min_landing_holes(self):
        return min(self.landing_hole_profile())

    def max_landing_holes(self):
        return max(self.landing_hole_profile())

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        h, w = self.bounding_box()
        lines = []
        for r in range(h):
            row_str = "".join("\u25A1 " if (r, c) in self._coord_set else "  " for c in range(w))
            lines.append(row_str)
        return "\n".join(lines) + "\n"


class ExTetromino(Shape):
    """A 4-cell 8-connected (edge or corner connected) polyplet."""

    def __init__(self, coords=None, piece_id=None, name=None):
        super().__init__(coords=coords, piece_id=piece_id, name=name)
        if len(self.coords) != 4:
            raise ValueError(f"ExTetromino must have exactly 4 cells, got {len(self.coords)}.")
        if not is_connected(self.coords, diagonal=True):
            raise ValueError(f"ExTetromino cells must be 8-connected, got {self.coords}.")

    def is_orthogonal(self):
        """True if all 4 cells are edge-connected (4-neighborhood)."""
        return is_connected(self.coords, diagonal=False)

    def is_diagonal(self):
        """True if the piece relies on at least one diagonal (corner) connection."""
        return not self.is_orthogonal()

    def canonical_one_sided(self):
        """Canonical signature invariant under 90-degree rotations."""
        probe = Shape(self.coords)
        forms = []
        for _ in range(4):
            forms.append(probe.coords)
            probe.rotateCW()
        return min(forms)

    def canonical_free(self):
        """Canonical signature invariant under rotations and reflections."""
        forms = []
        for base in (Shape(self.coords), Shape(self.coords).fliplr()):
            for _ in range(4):
                forms.append(base.coords)
                base.rotateCW()
        return min(forms)
