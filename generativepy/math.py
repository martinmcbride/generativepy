# Author:  Martin McBride
# Created: 2023-02-06
# Copyright (C) 2023, Martin McBride
# License: MIT
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=1e-12):
    """
    Check if two values a and b are equal to within a given tolerance
    :param a:
    :param b:
    :param rel_tol: Tolerance as a fraction of the absolute value of a or b (whichever is largest)
    :param abs_tol: Tolerance as an absolute value
    :return:
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class Matrix():
    """
    Class to represent a 2D transform matrix:
    | xx xy xt |
    | yx yy yt |
    """

    @staticmethod
    def scale(scale_x, scale_y=None):
        """
        Create a scaling matrix
        :param scale_x: Scale factor in x direction
        :param scale_y: Scale factor in y direction, defaults to scale_x
        :return: New matrix
        """
        if scale_y is None:
            scale_y = scale_x
        return Matrix(scale_x, 0, 0, 0, scale_y, 0)

    @staticmethod
    def translate(x, y):
        """
        Create a translation matrix
        :param x: Translation in x direction
        :param y: Translation in y direction
        :return: New matrix
        """
        return Matrix(1, 0, x, 0, 1, y)

    @staticmethod
    def rotate(angle):
        """
        Create a rotation matrix
        :param angle: Angle in radians, measured counterclockwise from positive x direction
        :return: New matrix
        """
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix(c, -s, 0, s, c, 0)

    @staticmethod
    def multiply(p, q):
        """
        Multiply two matrices
        :param a: First matrix
        :param b: Second matrix
        :return: New matrix
        """
        a = p[0]*q[0] + p[1]*q[3]
        b = p[0]*q[1] + p[1]*q[4]
        c = p[0]*q[2] + p[1]*q[5] + p[2]
        d = p[3]*q[0] + p[4]*q[3]
        e = p[3]*q[1] + p[4]*q[4]
        f = p[3]*q[2] + p[4]*q[5] + p[5]
        return Matrix(a, b, c, d, e, f)


    def __init__(self, xx, xy, xt, yx, yy, yt):
        self.matrix = (xx, xy, xt, yx, yy, yt)

    def __iter__(self):
        return iter(self.matrix)

    def __len__(self):
        return len(self.matrix)

    def __getitem__(self, index):
        return self.matrix[index]

    def __eq__(self, other):
        return all([isclose(a, b) for a, b in zip(self, other)])

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        return Matrix(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        # add the negative of `other`
        return self + (-other)

    def __mul__(self, other):
        # matrix * scalar
        if isinstance(other, (int, float)):
            return Matrix(*[other*a for a in self])
        if isinstance(other, Matrix):
            return Matrix.multiply(self, other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        # matrix / scalar
        if isinstance(other, (int, float)):
            return Matrix(*[a / other for a in self])
        else:
            return NotImplemented

    def __floordiv__(self, other):

        # matrix // scalar
        if isinstance(other, (int, float)):
            return Matrix(*[a // other for a in self])
        else:
            return NotImplemented

    def __repr__(self):
        return "Matrix({0}, {1}, {2}, {3}, {4}, {5})".format(*self.matrix)

    def __str__(self):
        return repr(self)



class Vector():
    """
    Class to represent a 2-vector including most of its common operations
    This is based on easy_vector https://github.com/DariusMontez/easy_vector
    The main changes are to make the object immutable, and measuring angle sin radians rather than degrees
    """

    @staticmethod
    def polar(length, angle):
        """
        Create a vector based on a length and angle
        :param length: Length of vector
        :param angle: Angle in radians, measured counterclockwise from positive x direction
        :return: New vector
        """
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        return Vector(x, y)

    @staticmethod
    def matrix_premultiply(m, v):
        """
        Multiply a matrix (first) and a vector (second)
        :param m: matrix
        :param v: vector
        :return: New vector
        """
        a = m[0]*v[0] + m[1]*v[1] + m[2]
        b = m[3]*v[0] + m[4]*v[1] + m[5]
        return Vector(a, b)

    def __init__(self, *args):
        # first arg may be an iterable (list, tuple, etc...)
        if len(args) == 1 and hasattr(args[0], "__iter__") and len(args[0]) == 2:
            self.coords = tuple(args[0])
        elif len(args) == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
            self.coords = tuple(args)
        else:
            raise ValueError("Vector requires a sequence of length 2, or 2 numbers")

    def transform(self, m):
        return m*self

    def scale(self, scale_x, scale_y=0):
        return Matrix.scale(scale_x, scale_y)*self

    def translate(self, x, y):
        return Matrix.translate(x, y)*self

    def rotate(self, angle):
        return Matrix.rotate(angle)*self

    def lerp(self, other, factor):
        """
        Interpolate between this vecto and other.
        Interplations factor:
            0 - result is self
            1 - result is other
            0 to 1 - result between self and other
            > 1 - result extensds beyond other
            < 0 - result extends backwards before other
        @param other: Other vector
        @param factor: Interpolation factor
        @return:
        """

        return Vector((1 - factor)*self.x + factor*other.x, (1 - factor)*self.y + factor*other.y)
    def __iter__(self):
        return iter(self.coords)

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, index):
        return self.coords[index]

    def __eq__(self, other):
        return isclose(self.x, other.x) and isclose(self.y, other.y)

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # add the negative of `other`
        return self + (-other)

    def __mul__(self, other):

        # vector * scalar
        if isinstance(other, (int, float)):
            return Vector(other * self.x, other * self.y)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        if isinstance(other, Matrix):
            return Vector.matrix_premultiply(other, self)
        return NotImplemented


    def __truediv__(self, other):

        # vector / scalar
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __floordiv__(self, other):

        # vector / scalar
        if isinstance(other, (int, float)):
            return Vector(self.x // other, self.y // other)
        else:
            return NotImplemented


    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def angle(self):
        angle = math.atan2(self.y, self.x)
        return angle

    @property
    def unit(self):
        return self / self.length

    # String representation
    def __repr__(self):
        return "Vector({0}, {1})".format(self.x, self.y)

    def __str__(self):
        return repr(self)

