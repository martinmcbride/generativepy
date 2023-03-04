import unittest
import math

from generativepy.math import Vector, Matrix


class TestVector(unittest.TestCase):

    def test_create_from_numbers(self):
        v = Vector(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

    def test_create_from_list(self):
        v = Vector([1, 2])
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

    def test_create_from_vector(self):
        v0 = Vector(1, 2)
        v = Vector(v0)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

    def test_create_bad_sequence(self):
        with self.assertRaises(ValueError):
            v = Vector([1, 2, 3])
        with self.assertRaises(ValueError):
            v = Vector(1, 2, 3)

    def test_create_from_polar(self):
        v = Vector.polar(2, math.radians(30))
        self.assertAlmostEqual(v.x, 1.7320508075688774)
        self.assertAlmostEqual(v.y, 1)

        v = Vector.polar(3, -math.radians(45))
        self.assertAlmostEqual(v.x, 2.121320344)
        self.assertAlmostEqual(v.y, -2.121320344)

    def test_static_matrix_premultiply(self):
        m = Matrix(2, 3, 4, 5, 6, 7)
        v = Vector(20, 30)
        self.assertEqual(Vector.matrix_premultiply(m, v), Vector(134, 287))

    def test_iter(self):
        v = Vector(10, 20)
        l = list(v)
        self.assertEqual(l, [10, 20])

    def test_len(self):
        v = Vector(0, 0)
        self.assertEqual(len(v), 2)

    def test_get_item(self):
        v = Vector(10, 20)
        self.assertEqual(v[0], 10)
        self.assertEqual(v[1], 20)
        self.assertEqual(v[-1], 20)
        self.assertEqual(v[-2], 10)
        with self.assertRaises(IndexError):
            v[2]
        with self.assertRaises(IndexError):
            v[-3]

    def test_get_item(self):
        v1 = Vector(10, 20)
        v2 = Vector(10, 20)
        v3 = Vector(1, 2)
        eq1 = v1 == v2
        eq2 = v1 == v3
        self.assertEqual(eq1, True)
        self.assertEqual(eq2, False)

    def test_eq(self):
        v1 = Vector(10, 20)
        v2 = Vector(10, 20)
        v3 = Vector(1, 20)
        self.assertEqual(v1 == v2, True)
        self.assertEqual(v1 == v3, False)

    def test_neg(self):
        v1 = Vector(10, 20)
        v2 = -v1
        self.assertEqual(v2, Vector(-10, -20))

    def test_add(self):
        v1 = Vector(10, 20)
        v2 = Vector(1, 2)
        v3 = v1 + v2
        self.assertEqual(v3, Vector(11, 22))

    def test_sub(self):
        v1 = Vector(10, 20)
        v2 = Vector(1, 2)
        v3 = v1 - v2
        self.assertEqual(v3, Vector(9, 18))

    def test_mul(self):
        # mul
        v1 = Vector(10, 20)
        v2 = v1 * 2
        self.assertEqual(v2, Vector(20, 40))
        #rmul
        v2 = -3 * v1
        self.assertEqual(v2, Vector(-30, -60))

    def test_matrix_mul(self):
        m = Matrix(2, 3, 4, 5, 6, 7)
        v = Vector(20, 30)
        self.assertEqual(m*v, Vector(134, 287))

    def test_div(self):
        v1 = Vector(10, 20)
        # truediv
        v2 = v1 / 2
        self.assertEqual(v2, Vector(5, 10))
        # floordiv
        v2 = v1 // 3
        self.assertEqual(v2, Vector(3, 6))

    def test_lerp(self):
        v1 = Vector(10, 20)
        v2 = Vector(50, 40)
        self.assertEqual(v1.lerp(v2, 0), Vector(10, 20))
        self.assertEqual(v1.lerp(v2, 1), Vector(50, 40))
        self.assertEqual(v1.lerp(v2, 0.4), Vector(26, 28))
        self.assertEqual(v1.lerp(v2, -.2), Vector(2, 16))
        self.assertEqual(v1.lerp(v2, 2), Vector(90, 60))

    def test_length(self):
        v = Vector(10, 20)
        self.assertAlmostEqual(v.length, 22.360679775)

    def test_angle(self):
        v = Vector(10, 20)
        self.assertAlmostEqual(v.angle, 1.10714871779)

    def test_unit(self):
        v = Vector(10, 20)
        u = v.unit
        self.assertAlmostEqual(u.x, 10/math.sqrt(500))
        self.assertAlmostEqual(u.y, 20/math.sqrt(500))

    def test_str(self):
        v = Vector(2, 5)
        s = str(v)
        self.assertEqual(s, "Vector(2, 5)")

    def test_repr(self):
        v = Vector(math.sqrt(2), math.sqrt(5))
        s = repr(v)
        self.assertEqual(s, "Vector(1.4142135623730951, 2.23606797749979)")


if __name__ == '__main__':
    unittest.main()
