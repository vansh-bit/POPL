# allextetrominoes.py: Piece registry for Attempt 1 Naive OOP
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
from shape import ClassicTetromino, ExtendedTetromino

# Deduplicated matrix catalog (71 unique oriented matrices from the original 73;
# duplicate I-piece entries #10 and #11 from Appendix D are removed).
_CLASSIC_SPECS = [
    (1, "I", [[True, True, True, True]]),
    (2, "O", [[True, True], [True, True]]),
    (3, "L", [[True, True, True], [True, False, False]]),
    (4, "T", [[True, True, True], [False, True, False]]),
    (5, "Gamma", [[True, True, True], [False, False, True]]),
    (6, "S", [[False, True, True], [True, True, False]]),
    (7, "Z", [[True, True, False], [False, True, True]]),
]

_EXTENDED_SPECS = [
    (8, "Ext8", [[True, False, True], [False, True, True]]),
    (9, "Ext9", [[True, True, False], [True, False, True]]),
    (10, "Ext10", [[True, True, True, False], [False, False, False, True]]),
    (11, "Ext11", [[True, True, False, True], [False, False, True, False]]),
    (12, "Ext12", [[True, True, False, False], [False, False, True, True]]),
    (13, "Ext13", [[True, False, True, True], [False, True, False, False]]),
    (14, "Ext14", [[True, False, True, False], [False, True, False, True]]),
    (15, "Ext15", [[True, False, False, True], [False, True, True, False]]),
    (16, "Ext16", [[True, False, False, False], [False, True, True, True]]),
    (17, "Ext17", [[False, True, True, False], [True, False, False, True]]),
    (18, "Ext18", [[False, True, False, False], [True, False, True, True]]),
    (19, "Ext19", [[False, False, True, False], [True, True, False, True]]),
    (20, "Ext20", [[True, True], [True, False], [False, True]]),
    (21, "Ext21", [[True, False], [True, True], [False, True]]),
    (22, "Ext22", [[True, False], [False, True], [True, True]]),
    (23, "Ext23", [[True, True, False], [False, True, False], [False, False, True]]),
    (24, "Ext24", [[True, True, False], [False, False, True], [False, True, False]]),
    (25, "Ext25", [[True, True, False], [False, False, True], [False, False, True]]),
    (26, "Ext26", [[True, False, True], [False, True, False], [True, False, False]]),
    (27, "Ext27", [[True, False, True], [False, True, False], [False, True, False]]),
    (28, "Ext28", [[True, False, True], [False, True, False], [False, False, True]]),
    (29, "Ext29", [[True, False, False], [True, True, False], [False, False, True]]),
    (30, "Ext30", [[True, False, False], [True, False, True], [False, True, False]]),
    (31, "Ext31", [[True, False, False], [True, False, False], [False, True, True]]),
    (32, "Ext32", [[True, False, False], [False, True, True], [True, False, False]]),
    (33, "Ext33", [[True, False, False], [False, True, True], [False, True, False]]),
    (34, "Ext34", [[True, False, False], [False, True, True], [False, False, True]]),
    (35, "Ext35", [[True, False, False], [False, True, False], [True, False, True]]),
    (36, "Ext36", [[True, False, False], [False, True, False], [False, True, True]]),
    (37, "Ext37", [[False, True, True], [True, False, False], [True, False, False]]),
    (38, "Ext38", [[False, True, True], [True, False, False], [False, True, False]]),
    (39, "Ext39", [[False, True, True], [False, True, False], [True, False, False]]),
    (40, "Ext40", [[False, True, False], [True, True, False], [False, False, True]]),
    (41, "Ext41", [[False, True, False], [True, False, True], [True, False, False]]),
    (42, "Ext42", [[False, True, False], [True, False, True], [False, True, False]]),
    (43, "Ext43", [[False, True, False], [True, False, True], [False, False, True]]),
    (44, "Ext44", [[False, True, False], [True, False, False], [False, True, True]]),
    (45, "Ext45", [[False, True, False], [False, True, True], [True, False, False]]),
    (46, "Ext46", [[False, True, False], [False, True, False], [True, False, True]]),
    (47, "Ext47", [[False, True, False], [False, False, True], [True, True, False]]),
    (48, "Ext48", [[False, False, True], [True, True, False], [True, False, False]]),
    (49, "Ext49", [[False, False, True], [True, True, False], [False, True, False]]),
    (50, "Ext50", [[False, False, True], [True, True, False], [False, False, True]]),
    (51, "Ext51", [[False, False, True], [True, False, True], [False, True, False]]),
    (52, "Ext52", [[False, False, True], [False, True, True], [True, False, False]]),
    (53, "Ext53", [[False, False, True], [False, True, False], [True, True, False]]),
    (54, "Ext54", [[False, False, True], [False, True, False], [True, False, True]]),
    (55, "Ext55", [[False, False, True], [False, False, True], [True, True, False]]),
    (56, "Ext56", [[True, True, False, False], [False, False, True, False], [False, False, False, True]]),
    (57, "Ext57", [[True, False, False, False], [False, True, True, False], [False, False, False, True]]),
    (58, "Ext58", [[True, False, False, False], [False, True, False, True], [False, False, True, False]]),
    (59, "Ext59", [[True, False, False, False], [False, True, False, False], [False, False, True, True]]),
    (60, "Ext60", [[False, True, False, False], [True, False, True, False], [False, False, False, True]]),
    (61, "Ext61", [[True, False], [True, False], [True, False], [False, True]]),
    (62, "Ext62", [[True, False], [True, False], [False, True], [False, True]]),
    (63, "Ext63", [[True, False], [False, True], [True, False], [False, True]]),
    (64, "Ext64", [[True, False], [False, True], [False, True], [False, True]]),
    (65, "Ext65", [[True, False, False], [True, False, False], [False, True, False], [False, False, True]]),
    (66, "Ext66", [[True, False, False], [False, True, False], [False, True, False], [False, False, True]]),
    (67, "Ext67", [[True, False, False], [False, True, False], [False, False, True], [False, True, False]]),
    (68, "Ext68", [[True, False, False], [False, True, False], [False, False, True], [False, False, True]]),
    (69, "Ext69", [[False, True, False], [True, False, False], [False, True, False], [False, False, True]]),
    (70, "Ext70", [[True, False, False, False], [False, True, False, False], [False, False, True, False], [False, False, False, True]]),
    (71, "Ext71", [[False, False, False, True], [False, False, True, False], [False, True, False, False], [True, False, False, False]]),
]


class PieceRegistry(object):
    """Registry mapping piece IDs to (name, Shape subclass, matrix)."""

    def __init__(self):
        self._entries = {}
        for piece_id, name, grid in _CLASSIC_SPECS:
            self._entries[piece_id] = (name, ClassicTetromino, numpy.array(grid, dtype=bool))
        for piece_id, name, grid in _EXTENDED_SPECS:
            self._entries[piece_id] = (name, ExtendedTetromino, numpy.array(grid, dtype=bool))

    def __len__(self):
        return len(self._entries)

    def ids(self):
        return list(self._entries.keys())

    def create(self, index):
        if index not in self._entries:
            raise ValueError(f"Extetromino index out of range: {index} (expected 1..{len(self._entries)})")
        name, cls, mat = self._entries[index]
        return cls(mat, piece_id=index, name=name)

    def matrix_at(self, index):
        if index not in self._entries:
            raise ValueError(f"Extetromino index out of range: {index} (expected 1..{len(self._entries)})")
        return self._entries[index][2].copy()


PIECE_REGISTRY = PieceRegistry()


def total_pieces():
    return len(PIECE_REGISTRY)


def create_piece(index):
    return PIECE_REGISTRY.create(index)


def get_extetromino_at(index):  # gives a sequential extetromino matrix.
    return PIECE_REGISTRY.matrix_at(index)


def get_any_piece(distribution=range(1, 72)):
    chosen_index = distribution[numpy.random.randint(len(distribution))]
    return PIECE_REGISTRY.create(chosen_index)


def get_any_extetromino(distribution=range(1, 72)):
    '''
    Returns a randomly selected extetromino matrix from the registry,
    according to the distribution.
    '''
    chosen_index = distribution[numpy.random.randint(len(distribution))]
    return PIECE_REGISTRY.matrix_at(chosen_index)
