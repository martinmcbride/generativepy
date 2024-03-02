# Author:  Martin McBride
# Created: 2023-02-06
# Copyright (C) 2023, Martin McBride
# License: MIT
import math
"""
The math module provides basic implementation of 2D vectors and matrices.

There are other Python matrix libraries, but this library is geared towards vector graphics, and provides features such
as polar vectors and vector lerp (linear interpolation) that are useful for maths visualisation and animation.
"""

def isclose(a, b, rel_tol=1e-09, abs_tol=1e-12):
    """
    Check if two values a and b are equal to within a given tolerance

    Args:
        a: number - First value
        b: number - Second value
        rel_tol: number - Tolerance as a fraction of the absolute value of a or b (whichever is largest)
        abs_tol: number - Tolerance as an absolute value

    Returns:
        True if the numbers are close, false otherwise.
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Matrix():
    """
    Class to represent a 2D transform matrix:

    ```
    | xx xy xt |
    | yx yy yt |
    ```
    """

    @staticmethod
    def unit():
        """
        Create a unit matrix

        Returns:
            The unit matrix.
        """
        return Matrix(1, 0, 0, 0, 1, 0)

    @staticmethod
    def scale(scale_x, scale_y=None):
        """
        Create a scaling matrix

        Args:
            scale_x: Scale factor in x direction
            scale_y: Scale factor in y direction, defaults to scale_x

        Returns:
            New matrix
        """
        if scale_y is None:
            scale_y = scale_x
        return Matrix(scale_x, 0, 0, 0, scale_y, 0)

    @staticmethod
    def translate(x, y):
        """
        Create a translation matrix

        Args:
            x: Translation in x direction
            y: Translation in y direction

        Returns:
            New matrix
        """
        return Matrix(1, 0, x, 0, 1, y)

    @staticmethod
    def rotate(angle):
        """
        Create a rotation matrix

        Args:
            angle: Angle in radians, measured counterclockwise from positive x direction

        Returns:
            New matrix
        """
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix(c, -s, 0, s, c, 0)

    @staticmethod
    def multiply(p, q):
        """
        Multiply two matrices

        Args:
            a: First matrix
            b: Second matrix

        Returns:
            New matrix
        """
        a = p[0] * q[0] + p[1] * q[3]
        b = p[0] * q[1] + p[1] * q[4]
        c = p[0] * q[2] + p[1] * q[5] + p[2]
        d = p[3] * q[0] + p[4] * q[3]
        e = p[3] * q[1] + p[4] * q[4]
        f = p[3] * q[2] + p[4] * q[5] + p[5]
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
            return Matrix(*[other * a for a in self])
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
    The main changes are to make the object immutable, and measuring angles in radians rather than degrees
    """

    @staticmethod
    def polar(length, angle):
        """
        Create a vector based on a length and angle

        Args:
            length: Length of vector
            angle: Angle in radians, measured counterclockwise from positive x direction

        Returns:
            New vector
        """
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        return Vector(x, y)

    @staticmethod
    def matrix_premultiply(m, v):
        """
        Multiply a matrix (first) and a vector (second)

        Args:
            m: matrix
            v: vector

        Returns:
            New vector
        """
        a = m[0] * v[0] + m[1] * v[1] + m[2]
        b = m[3] * v[0] + m[4] * v[1] + m[5]
        return Vector(a, b)

    def __init__(self, *args):
        """
        Can either accept 2 number, or a tuple containing 2 numerical elements.

        Args:
            args: various - see above

        Returns:
            Self
        """
        if len(args) == 1 and hasattr(args[0], "__iter__") and len(args[0]) == 2:
            self.coords = tuple(args[0])
        elif len(args) == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
            self.coords = tuple(args)
        else:
            raise ValueError("Vector requires a sequence of length 2, or 2 numbers")

    def transform(self, m):
        """
        Transform this vector by a matrix. The vector is pre-multiplied by the matrix

        Args:
            m: matrix

        Returns:
            New transformed vector
        """
        return m * self

    def scale(self, scale_x, scale_y=None):
        """
        Scale this vector by a factor.

        Args:
            scale_x: scale factor in x direction.
            scale_y: scale factor in y direction. If this is None, scale by scale_x in both directions.

        Returns:
            New scaled vector
        """
        return Matrix.scale(scale_x, scale_y) * self

    def translate(self, x, y):
        """
        Translate this vector by (x, y),

        Args:
            x: translation amount in x direction.
            y: translation amount in y direction.

        Returns:
            New translated vector
        """
        return Matrix.translate(x, y) * self

    def rotate(self, angle):
        """
        Rotate this vector by (x, y),

        Args:
            x: rotation amount in x direction.
            y: rotation amount in y direction.

        Returns:
            New rotated vector
        """
        return Matrix.rotate(angle) * self

    def lerp(self, other, factor):
        """
        Interpolate between this vector and other.

        The `factor` parameter works like this:

        * 0 - result is self
        * 1 - result is other
        * 0 to 1 - result between self and other
        * > 1 - result extensds beyond other
        * < 0 - result extends backwards before other

        Args:
            other: Vector - the other vector
            factor: number - The interpolation amount.

        Returns:
            New rotated vector
        """

        return Vector((1 - factor) * self.x + factor * other.x, (1 - factor) * self.y + factor * other.y)

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
        """
        Read-only property returns x component of vector.
        """
        return self.coords[0]

    @property
    def y(self):
        """
        Read-only property returns y component of vector.
        """
        return self.coords[1]

    @property
    def length(self):
        """
        Read-only property returns length of vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        """
        Read-only property returns angle of vector.
        """
        angle = math.atan2(self.y, self.x)
        return angle

    @property
    def unit(self):
        """
        Read-only property returns a unit vector with the same angle as this vector
        """
        return self / self.length

    # String representation
    def __repr__(self):
        return "Vector({0}, {1})".format(self.x, self.y)

    def __str__(self):
        return repr(self)

class Vector3:
    """
    Class to represent a 3-vector including most of its common operations
    """

    def __init__(self, *args):
        """
        Can either accept 3 numbers, or a tuple containing 3 numerical elements.

        Args:
            args: various - see above

        Returns:
            Self
        """
        if len(args) == 1 and hasattr(args[0], "__iter__") and len(args[0]) == 3:
            self.coords = tuple(args[0])
        elif (
            len(args) == 3
            and isinstance(args[0], (int, float))
            and isinstance(args[1], (int, float))
            and isinstance(args[2], (int, float))
        ):
            self.coords = tuple(args)
        else:
            raise ValueError("Vector3 requires a sequence of length 3, or 3 numbers")

    def lerp(self, other, factor):
        """
        Interpolate between this vector and other.

        The `factor` parameter works like this:

        * 0 - result is self
        * 1 - result is other
        * 0 to 1 - result between self and other
        * > 1 - result extensds beyond other
        * < 0 - result extends backwards before other

        Args:
            other: Vector3 - the other vector
            factor: number - The interpolation amount.

        Returns:
            New rotated vector
        """

        return Vector3(
            (1 - factor) * self.x + factor * other.x,
            (1 - factor) * self.y + factor * other.y,
            (1 - factor) * self.z + factor * other.z,
        )

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
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        # add the negative of `other`
        return self + (-other)

    def __mul__(self, other):

        # vector * scalar
        if isinstance(other, (int, float)):
            return Vector3(other * self.x, other * self.y, other * self.z)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        return NotImplemented

    def __truediv__(self, other):

        # vector / scalar
        if isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            return NotImplemented

    def __floordiv__(self, other):

        # vector / scalar
        if isinstance(other, (int, float)):
            return Vector3(self.x // other, self.y // other, self.z // other)
        else:
            return NotImplemented

    @property
    def x(self):
        """
        Read-only property returns x component of vector.
        """
        return self.coords[0]

    @property
    def y(self):
        """
        Read-only property returns y component of vector.
        """
        return self.coords[1]

    @property
    def z(self):
        """
        Read-only property returns z component of vector.
        """
        return self.coords[2]

    # String representation
    def __repr__(self):
        return "Vector3({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __str__(self):
        return repr(self)


