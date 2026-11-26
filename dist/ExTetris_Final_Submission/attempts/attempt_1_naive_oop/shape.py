# shape.py: Handling tetromino-like shapes or larger (Attempt 1 Naive OOP).
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


class Shape(object):
    is_classic = False

    def __init__(self, mat=None, piece_id=None, name=None):
        if mat is None:
            self.matrix = numpy.array([[True, True, True, True]], dtype=bool)
        elif isinstance(mat, numpy.ndarray):
            self.matrix = mat.copy()
        else:
            raise Exception('Expected matrix, found ' + str(mat) + ' a ' + str(type(mat)))
        self.piece_id = piece_id
        self.name = name or self.__class__.__name__

    def clone(self):
        return self.__class__(self.matrix.copy(), piece_id=self.piece_id, name=self.name)

    def bounding_box(self):
        return self.matrix.shape

    def fliplr(self):
        for row in range(self.matrix.shape[0]):
            self.matrix[row] = [self.matrix[row][i] for i in range(self.matrix.shape[1] - 1, -1, -1)]

    def flipud(self):
        firstrow = 0
        exchangerow = self.matrix.shape[0] - 1
        while firstrow < exchangerow:
            temp = self.matrix[firstrow].copy()
            self.matrix[firstrow] = self.matrix[exchangerow].copy()
            self.matrix[exchangerow] = temp.copy()
            firstrow += 1
            exchangerow -= 1

    def transpose(self):
        self.matrix = self.matrix.transpose().copy()

    def rotateCW(self):
        self.flipud()
        self.transpose()

    def rotateAntiCW(self):
        self.transpose()
        self.flipud()

    def __str__(self):
        string = ''
        for row in range(self.matrix.shape[0]):
            for col in range(self.matrix.shape[1]):
                if self.matrix[row][col]:
                    string = string + '\u25A1 '
                else:
                    string = string + '  '
            string = string + '\n'
        return string


class ClassicTetromino(Shape):
    """Represents one of the 7 classic edge-connected tetrominoes."""
    is_classic = True


class ExtendedTetromino(Shape):
    """Represents an extended (edge/corner-connected) tetromino from the starter catalog."""
    is_classic = False


if __name__ == "__main__":
    from allextetrominoes import create_piece, total_pieces

    shape0 = Shape()
    for i in range(1, total_pieces() + 1):
        shape1 = create_piece(i)
        print(f"#{i} ({shape1.__class__.__name__}: {shape1.name})")
        print(str(shape1))
        shape1.rotateCW()
        print(str(shape1))
        shape1.rotateAntiCW()
        shape1.rotateAntiCW()
        print(str(shape1))
