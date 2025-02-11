import unittest
import math

from generativepy.math import Vector3


class TestVector(unittest.TestCase):

    def test_create_from_numbers(self):
        v = Vector3(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_create_from_list(self):
        v = Vector3([1, 2, 3])
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_create_from_vector(self):
        v0 = Vector3(1, 2, 3)
        v = Vector3(v0)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_create_bad_sequence(self):
        with self.assertRaises(ValueError):
            v = Vector3([1, 2])
        with self.assertRaises(ValueError):
            v = Vector3(1, 2)
        with self.assertRaises(ValueError):
            v = Vector3([1, 2, 3, 4])
        with self.assertRaises(ValueError):
            v = Vector3(1, 2, 3, 4)

    def test_iter(self):
        v = Vector3(10, 20, 30)
        l = list(v)
        self.assertEqual(l, [10, 20, 30])

    def test_len(self):
        v = Vector3(0, 0, 0)
        self.assertEqual(len(v), 3)

    def test_get_item(self):
        v = Vector3(10, 20, 30)
        self.assertEqual(v[0], 10)
        self.assertEqual(v[1], 20)
        self.assertEqual(v[2], 30)
        self.assertEqual(v[-1], 30)
        self.assertEqual(v[-2], 20)
        self.assertEqual(v[-3], 10)
        with self.assertRaises(IndexError):
            v[3]
        with self.assertRaises(IndexError):
            v[-4]

    def test_eq(self):
        v1 = Vector3(10, 20, 30)
        v2 = Vector3(10, 20, 30)
        v3 = Vector3(1, 20, 30)
        self.assertEqual(v1 == v2, True)
        self.assertEqual(v1 == v3, False)

    def test_neg(self):
        v1 = Vector3(10, 20, 30)
        v2 = -v1
        self.assertEqual(v2, Vector3(-10, -20, -30))

    def test_add(self):
        v1 = Vector3(10, 20, 30)
        v2 = Vector3(1, 2, 3)
        v3 = v1 + v2
        self.assertEqual(v3, Vector3(11, 22, 33))

    def test_sub(self):
        v1 = Vector3(10, 20, 30)
        v2 = Vector3(1, 2, 3)
        v3 = v1 - v2
        self.assertEqual(v3, Vector3(9, 18, 27))

    def test_mul(self):
        # mul
        v1 = Vector3(10, 20, 30)
        v2 = v1 * 2
        self.assertEqual(v2, Vector3(20, 40, 60))
        #rmul
        v2 = -3 * v1
        self.assertEqual(v2, Vector3(-30, -60, -90))

    def test_div(self):
        v1 = Vector3(10, 20, 30)
        # truediv
        v2 = v1 / 2
        self.assertEqual(v2, Vector3(5, 10, 15))
        # floordiv
        v2 = v1 // 3
        self.assertEqual(v2, Vector3(3, 6, 10))

    def test_lerp(self):
        v1 = Vector3(10, 20, 30)
        v2 = Vector3(50, 40, 10)
        self.assertEqual(v1.lerp(v2, 0), Vector3(10, 20, 30))
        self.assertEqual(v1.lerp(v2, 1), Vector3(50, 40, 10))
        self.assertEqual(v1.lerp(v2, 0.4), Vector3(26, 28, 0))
        self.assertEqual(v1.lerp(v2, -.2), Vector3(2, 16, 0))
        self.assertEqual(v1.lerp(v2, 2), Vector3(90, 60, 0))

    def test_str(self):
        v = Vector3(2, 5, 9)
        s = str(v)
        self.assertEqual(s, "Vector3(2, 5, 9)")

    def test_repr(self):
        v = Vector3(math.sqrt(2), math.sqrt(5), 1)
        s = repr(v)
        self.assertEqual(s, "Vector3(1.4142135623730951, 2.23606797749979, 1)")


if __name__ == '__main__':
    unittest.main()
