# board.py: Coordinate-aware game board with heuristic metrics
# Based on starter code Copyright (C) 2024 Ramprasad S. Joshi
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import numpy
from extetris.shapes import Shape


class Board(object):
    """2D block grid supporting collision checks, ghost projection, line clearing, and board metrics."""

    def __init__(self, width=10, height=20):
        self.width = int(width)
        self.height = int(height)
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Board dimensions must be positive.")
        self.area = numpy.zeros((self.height, self.width), dtype=bool)

    @property
    def grid(self):
        return self.area

    def clone(self):
        copy_board = Board(width=self.width, height=self.height)
        copy_board.area = self.area.copy()
        return copy_board

    @staticmethod
    def _extract_coords(shape):
        if isinstance(shape, Shape) or hasattr(shape, "coords"):
            return shape.coords
        coords = []
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    coords.append((r, c))
        return tuple(coords)

    def __str__(self):
        lines = []
        for row in range(self.height):
            row_chars = [
                "\N{BLACK LARGE SQUARE}|" if self.area[row, col] else "  |"
                for col in range(self.width)
            ]
            lines.append("".join(row_chars))
        return "\n".join(lines) + "\n"

    def is_valid_position(self, shape, offset):
        """Return True iff every occupied cell of shape placed at offset is in bounds and free."""
        off_y, off_x = offset
        for dr, dc in self._extract_coords(shape):
            r = off_y + dr
            c = off_x + dc
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                return False
            if self.area[r, c]:
                return False
        return True

    def collision(self, shape, offset):
        return not self.is_valid_position(shape, offset)

    def get_ghost_row(self, shape, cursor):
        """Return the lowest valid row index where shape would land straight below cursor."""
        row, col = cursor
        if not self.is_valid_position(shape, (row, col)):
            return row
        while self.is_valid_position(shape, (row + 1, col)):
            row += 1
        return row

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

    def column_heights(self):
        heights = []
        for col in range(self.width):
            occupied = numpy.where(self.area[:, col])[0]
            heights.append(0 if len(occupied) == 0 else int(self.height - occupied[0]))
        return heights

    def get_max_height(self):
        heights = self.column_heights()
        return max(heights) if heights else 0

    def count_holes(self):
        holes = 0
        for col in range(self.width):
            seen_block = False
            for row in range(self.height):
                if self.area[row, col]:
                    seen_block = True
                elif seen_block:
                    holes += 1
        return holes

    def get_bumpiness(self):
        heights = self.column_heights()
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))
