# factory.py: Algorithmic 4-polyplet generator and grouping API (Attempt 2)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from itertools import combinations
import time
from shape import is_connected, normalize_coords
from hierarchy import classify_extetromino


class ExTetrominoFactory(object):
    """
    Algorithmically synthesizes all unique 4-polyplets fitting on a 4x4 grid
    without any hard-coded boolean matrices, and exposes canonical groupings:
      - 110 fixed (oriented, normalized) 4-polyplets
      - 34 one-sided 4-polyplets (modulo 90-degree rotations)
      - 22 free 4-polyplets (modulo rotations and reflections)
      - 7 classic one-sided tetrominoes / 19 classic fixed orientations
      - 27 diagonal one-sided polyplets / 91 diagonal fixed orientations
    """

    def __init__(self, grid_size=4):
        if grid_size < 4:
            raise ValueError("grid_size must be at least 4 to generate all 4-polyplets.")
        self.grid_size = grid_size
        t0 = time.perf_counter()
        self._fixed_catalog = self._generate_catalog()
        self.generation_time_sec = time.perf_counter() - t0
        self._by_id = {p.piece_id: p for p in self._fixed_catalog}

    def _instantiate_piece(self, coords, piece_id, name):
        """Instantiate each generated piece as its exact multi-axis subclass."""
        return classify_extetromino(coords=coords, piece_id=piece_id, name=name)

    def _generate_catalog(self):
        grid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        unique_coords = set()
        for comb in combinations(grid_cells, 4):
            if is_connected(comb, diagonal=True):
                unique_coords.add(normalize_coords(comb))

        # Order orthogonal (classic) pieces first, then diagonal, sorted canonically
        def sort_key(coords):
            ortho = is_connected(coords, diagonal=False)
            h = max(r for r, _ in coords) + 1
            w = max(c for _, c in coords) + 1
            return (0 if ortho else 1, h, w, coords)

        ordered = sorted(unique_coords, key=sort_key)
        catalog = []
        for idx, coords in enumerate(ordered, start=1):
            prefix = "Classic" if is_connected(coords, diagonal=False) else "Diag"
            piece = self._instantiate_piece(coords, piece_id=idx, name=f"{prefix}-{idx}")
            catalog.append(piece)
        return catalog

    def by_id(self, piece_id):
        if piece_id not in self._by_id:
            raise ValueError(f"Unknown ExTetromino ID: {piece_id} (expected 1..{len(self._fixed_catalog)})")
        return self._by_id[piece_id].clone()

    def all_fixed(self):
        """Return all 110 unique oriented normalized 4-polyplets."""
        return [p.clone() for p in self._fixed_catalog]

    def all_one_sided(self):
        """Return 1 representative per 90-degree rotation class (34 shapes)."""
        seen = set()
        result = []
        for p in self._fixed_catalog:
            sig = p.canonical_one_sided()
            if sig not in seen:
                seen.add(sig)
                result.append(p.clone())
        return result

    def all_free(self):
        """Return 1 representative per rotation+reflection class (22 shapes)."""
        seen = set()
        result = []
        for p in self._fixed_catalog:
            sig = p.canonical_free()
            if sig not in seen:
                seen.add(sig)
                result.append(p.clone())
        return result

    def classic_fixed(self):
        """Return all 19 fixed orientations of the 7 classic edge-connected tetrominoes."""
        return [p.clone() for p in self._fixed_catalog if p.is_orthogonal()]

    def classic_one_sided(self):
        """Return the 7 classic one-sided tetrominoes (modulo 90-degree rotations)."""
        seen = set()
        result = []
        for p in self._fixed_catalog:
            if p.is_orthogonal():
                sig = p.canonical_one_sided()
                if sig not in seen:
                    seen.add(sig)
                    result.append(p.clone())
        return result

    def extended_fixed(self):
        """Return all 91 fixed orientations that require at least one diagonal connection."""
        return [p.clone() for p in self._fixed_catalog if p.is_diagonal()]

    def extended_one_sided(self):
        """Return the 27 diagonal one-sided 4-polyplets (modulo 90-degree rotations)."""
        seen = set()
        result = []
        for p in self._fixed_catalog:
            if p.is_diagonal():
                sig = p.canonical_one_sided()
                if sig not in seen:
                    seen.add(sig)
                    result.append(p.clone())
        return result

    def filter(self, predicate):
        """Filter the 110 fixed 4-polyplets by a custom predicate."""
        return [p.clone() for p in self._fixed_catalog if predicate(p)]

    def summary(self):
        return {
            "fixed_total": len(self._fixed_catalog),
            "one_sided_total": len(self.all_one_sided()),
            "free_total": len(self.all_free()),
            "classic_one_sided": len(self.classic_one_sided()),
            "classic_fixed": len(self.classic_fixed()),
            "diagonal_one_sided": len(self.extended_one_sided()),
            "diagonal_fixed": len(self.extended_fixed()),
            "generation_time_sec": round(self.generation_time_sec, 6),
        }


if __name__ == "__main__":
    factory = ExTetrominoFactory()
    print("ExTetrominoFactory summary:", factory.summary())
