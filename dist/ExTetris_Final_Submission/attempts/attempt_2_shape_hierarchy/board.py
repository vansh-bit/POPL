# board.py: Bounds-safe coordinate-aware game board (Attempt 2)
# Based on starter code Copyright (C) 2024 Ramprasad S. Joshi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy
from shape import Shape


class Board(object):
    """2D block grid supporting coordinate-based Shape collision, placement, and line clearing."""

    def __init__(self, width=10, height=20):
        self.width = int(width)
        self.height = int(height)
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Board dimensions must be positive.")
        self.area = numpy.zeros((self.height, self.width), dtype=bool)

    def clone(self):
        copy_board = Board(width=self.width, height=self.height)
        copy_board.area = self.area.copy()
        return copy_board

    @staticmethod
    def _extract_coords(shape):
        if isinstance(shape, Shape):
            return shape.coords
        if hasattr(shape, "coords"):
            return shape.coords
        # Fallback for raw 2D boolean sequences
        coords = []
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    coords.append((r, c))
        return tuple(coords)

    def __str__(self):
        lines = []
        for row in range(self.height):
            row_chars = []
            for col in range(self.width):
                if self.area[row, col]:
                    row_chars.append('\N{BLACK LARGE SQUARE}|')
                else:
                    row_chars.append('  |')
            lines.append(''.join(row_chars))
        return '\n'.join(lines) + '\n'

    def insertShape(self, shape, rowIndex=0, columnIndex=0):
        for dr, dc in self._extract_coords(shape):
            r = rowIndex + dr
            c = columnIndex + dc
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                raise IndexError(f"Cannot insert cell out of bounds at ({r}, {c})")
            self.area[r, c] = True

    def removeShape(self, shape, rowIndex=0, columnIndex=0):
        for dr, dc in self._extract_coords(shape):
            r = rowIndex + dr
            c = columnIndex + dc
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                raise IndexError(f"Cannot remove cell out of bounds at ({r}, {c})")
            self.area[r, c] = False

    def collision(self, shape, offset):
        off_y, off_x = offset
        for dr, dc in self._extract_coords(shape):
            r = off_y + dr
            c = off_x + dc
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                return True
            if self.area[r, c]:
                return True
        return False

    def clear_full_lines(self):
        """Remove all completely filled rows, shift upper rows down, and return cleared count."""
        kept_rows = [self.area[r] for r in range(self.height) if not self.area[r].all()]
        cleared = self.height - len(kept_rows)
        if cleared > 0:
            empty_top = numpy.zeros((cleared, self.width), dtype=bool)
            if kept_rows:
                self.area = numpy.vstack([empty_top, numpy.array(kept_rows, dtype=bool)])
            else:
                self.area = empty_top
        return cleared
