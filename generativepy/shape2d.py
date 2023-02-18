# Author:  Martin McBride
# Created: 2023-02-17
# Copyright (C) 2023, Martin McBride
# License: MIT
from generativepy.math import Matrix, Vector


class Points:

    def __init__(self, points):
        self.points = tuple(Vector(p) for p in points)

    def transform(self, m):
        return m*self

    def scale(self, scale_x, scale_y=0):
        return Matrix.scale(scale_x, scale_y)*self

    def translate(self, x, y):
        return Matrix.translate(x, y)*self

    def rotate(self, angle):
        return Matrix.rotate(angle)*self

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all([a == b for a, b in zip(self, other)])

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return tuple(Vector.matrix_premultiply(other, p) for p in self.points)
        return NotImplemented

    def __repr__(self):
        return "Points(" + ", ".join((str(p) for p in self.points)) + ")"

    def __str__(self):
        return repr(self)

