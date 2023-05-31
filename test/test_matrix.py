import unittest
import math

from generativepy.math import Matrix

class TestMatrix(unittest.TestCase):

    def test_create_from_numbers(self):
        m = Matrix(2, 3, 4, 5, 6, 7)
        self.assertEqual(m[0], 2)
        self.assertEqual(m[1], 3)
        self.assertEqual(m[2], 4)
        self.assertEqual(m[3], 5)
        self.assertEqual(m[4], 6)
        self.assertEqual(m[5], 7)

    def test_iter(self):
        m = Matrix(2, 3, 4, 5, 6, 7)
        l = list(m)
        self.assertEqual(l, [2, 3, 4, 5, 6, 7])

    def test_len(self):
        m = Matrix(0, 0, 0, 0, 0, 0)
        self.assertEqual(len(m), 6)

    def test_get_item(self):
        m = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(m[0], 20)
        self.assertEqual(m[1], 30)
        self.assertEqual(m[2], 40)
        self.assertEqual(m[3], 50)
        self.assertEqual(m[4], 60)
        self.assertEqual(m[5], 70)
        self.assertEqual(m[-1], 70)
        self.assertEqual(m[-6], 20)
        with self.assertRaises(IndexError):
            m[6]
        with self.assertRaises(IndexError):
            m[-7]

    def test_eq(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = Matrix(2, 3, 4, 5, 6, 7)
        m3 = Matrix(0, 3, 4, 5, 6, 7)
        m4 = Matrix(2, 3, 0, 5, 6, 7)
        m5 = Matrix(2, 3, 4, 5, 6, 0)
        self.assertEqual(m1 == m2, True)
        self.assertEqual(m1 == m3, False)
        self.assertEqual(m1 == m4, False)
        self.assertEqual(m1 == m5, False)

    def test_neg(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = -m1
        self.assertEqual(m2, Matrix(-2, -3, -4, -5, -6, -7))

    def test_add(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(m2+m1, Matrix(22, 33, 44, 55, 66, 77))

    def test_sub(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(m2-m1, Matrix(18, 27, 36, 45, 54, 63))

    def test_mul(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        # mul
        self.assertEqual(m1*5, Matrix(10, 15, 20, 25, 30, 35))
        # rmul
        self.assertEqual(20*m1, Matrix(40, 60, 80, 100, 120, 140))

    def test_mul_matrix(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(m1*m2, Matrix(190, 240, 294, 400, 510, 627))

    def test_div(self):
        m1 = Matrix(20, 30, 40, 50, 60, 70)
        # truediv
        self.assertEqual(m1/20, Matrix(1.0, 1.5, 2.0, 2.5, 3.0, 3.5))
        # floordiv
        self.assertEqual(m1//20, Matrix(1, 1, 2, 2, 3, 3))

    def test_str(self):
        m = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(str(m), "Matrix(20, 30, 40, 50, 60, 70)")

    def test_repr(self):
        m = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(repr(m), "Matrix(20, 30, 40, 50, 60, 70)")

    def test_static_multiply(self):
        m1 = Matrix(2, 3, 4, 5, 6, 7)
        m2 = Matrix(20, 30, 40, 50, 60, 70)
        self.assertEqual(Matrix.multiply(m1, m2), Matrix(190, 240, 294, 400, 510, 627))

    def test_static_unit(self):
        m = Matrix.unit()
        self.assertEqual(m, Matrix(1, 0, 0, 0, 1, 0))

    def test_static_scale(self):
        m = Matrix.scale(2)
        self.assertEqual(m, Matrix(2, 0, 0, 0, 2, 0))

    def test_static_translate(self):
        m = Matrix.translate(10, 20)
        self.assertEqual(m, Matrix(1, 0, 10, 0, 1, 20))

    def test_static_rotate(self):
        m = Matrix.rotate(math.radians(30))
        self.assertEqual(m==Matrix(0.8660254037, -0.5, 0, 0.5, 0.8660254037, 0), True)

