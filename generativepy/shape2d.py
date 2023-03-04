# Author:  Martin McBride
# Created: 2023-02-17
# Copyright (C) 2023, Martin McBride
# License: MIT
from generativepy.math import Matrix, Vector
import math


class Points:

    @staticmethod
    def regular_polygon(sides, centre=(0, 0), radius=1, flat_base=True):
        """
        Create the points for a regular polygon.
        @param sides: Number of sides of the polygon
        @param centre: Position of polygon centre
        @param radius: Radius (distance from centre to any vertex)
        @param flat_base: If true, the polygon will have a flat base. Otherwise, vertex 0 will be on +ve x-axis.
        @return:
        """
        centre_angle = math.pi * 2 / sides
        angle = math.pi / 2 - centre_angle / 2 if flat_base else 0
        angles = [angle + centre_angle * i for i in range(sides)]

        return Points(((radius * math.cos(a) + centre[0], radius * math.sin(a) + centre[1]) for a in angles))

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
            return Points(Vector.matrix_premultiply(other, p) for p in self.points)
        return NotImplemented

    def __repr__(self):
        return "Points(" + ", ".join((str(p) for p in self.points)) + ")"

    def __str__(self):
        return repr(self)

