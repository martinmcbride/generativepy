# Author:  Martin McBride
# Created: 2023-02-17
# Copyright (C) 2023, Martin McBride
# License: MIT
from generativepy.math import Matrix, Vector
import math


class Points:
    """
    Points array stores a list of `Vector` objects.

    It provides various ways to transform all the points in the list, and static methods to create new sets of points.

    It also implements pre-multiplication by a matrix. To transform all the points in list `p` by matrix `m`, use:

    `p1 = m * p`
    """

    @staticmethod
    def regular_polygon(sides, centre=(0, 0), radius=1, flat_base=True):
        """
        Create the points for a regular polygon.

        Args:
            sides: int - number of sides of the polygon.
            centre: tuple - position of polygon centre.
            radius: number - Outer radius (distance from centre to any vertex).
            flat_base: bool - ff true, the polygon will have a flat base. Otherwise, vertex 0 will be on +ve x-axis.

        Returns:
            A new `Points` item containing the vertices.
        """
        centre_angle = math.pi * 2 / sides
        angle = math.pi / 2 - centre_angle / 2 if flat_base else 0
        angles = [angle + centre_angle * i for i in range(sides)]

        return Points(((radius * math.cos(a) + centre[0], radius * math.sin(a) + centre[1]) for a in angles))

    def __init__(self, points):
        """
        Initialise a new points object.
        Args:
            points: tuple of tuples - the points to include.
        """
        self.points = tuple(Vector(p) for p in points)

    def transform(self, m):
        """
        Transform every point by the matrix.
        Args:
            m: `Matrix` - transformation matrix.

        Returns:
            New transformed `Points` object.
        """
        return m*self

    def scale(self, scale_x, scale_y=0):
        """
        Apply scale transform to every point.

        Args:
            scale_x: number - x scale factor
            scale_y: number - y scale factor

        Returns:
            New transformed `Points` object.
        """
        return Matrix.scale(scale_x, scale_y)*self

    def translate(self, x, y):
        """
        Apply translation transform to every point.

        Args:
            x: number - x translation
            y: number - y translation

        Returns:
            New transformed `Points` object.
        """

        return Matrix.translate(x, y)*self

    def rotate(self, angle):
        """
        Apply rotation transform to every point.

        Args:
            angle: number - angle to rotate, in radians.

        Returns:
            New transformed `Points` object.
        """

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

