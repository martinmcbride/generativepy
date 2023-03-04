import unittest
import math

from generativepy.math import Matrix, Vector
from generativepy.shape2d import Points


class TestPoints(unittest.TestCase):

    def test_create_from_numbers(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(p[0], Vector(1, 2))
        self.assertEqual(p[1], Vector(3, 4))
        self.assertEqual(p[2], Vector(5, 6))

    def test_iter(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        l = list(p)
        self.assertEqual(l, [Vector(1, 2), Vector(3, 4), Vector(5, 6)])

    def test_len(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(len(p), 3)

    def test_get_item(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(p[0], Vector(1, 2))
        self.assertEqual(p[1], Vector(3, 4))
        self.assertEqual(p[2], Vector(5, 6))
        self.assertEqual(p[-1], Vector(5, 6))
        self.assertEqual(p[-3], Vector(1, 2))
        with self.assertRaises(IndexError):
            p[3]
        with self.assertRaises(IndexError):
            p[-4]

    def test_eq(self):
        p1 = Points([[1, 2], [3, 4], [5, 6]])
        p2 = Points([[1, 2], [3, 4], [5, 6]])
        p3 = Points([[1, 2], [3, 4]])
        p4 = Points([[1, 2], [3, 4], [5, 6], [7, 8]])
        p5 = Points([[1, 2], [30, 4], [5, 6]])
        self.assertEqual(p1 == p2, True)
        self.assertEqual(p1 == p3, False)
        self.assertEqual(p1 == p4, False)
        self.assertEqual(p1 == p5, False)

    def test_mul_matrix(self):
        m = Matrix(1, 2, 3, 4, 5, 6)
        p = Points([[1, 2], [3, 4], [5, 6]])
        expected = Points([[8, 20], [14, 38], [20, 56]])
        self.assertEqual(m*p, expected)

    def test_str(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(str(p), "Points(Vector(1, 2), Vector(3, 4), Vector(5, 6))")

    def test_str(self):
        p = Points([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(repr(p), "Points(Vector(1, 2), Vector(3, 4), Vector(5, 6))")

    def test_regular_flat(self):
        p = Points.regular_polygon(4, (0, 0), 1)
        s = math.sqrt(2)/2
        self.assertEqual(p, Points([(s, s), (-s, s), (-s, -s), (s, -s)]))

    def test_regular_not_flat(self):
        p = Points.regular_polygon(4, (0, 0), 1, flat_base=False)
        exp = Points([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.assertEqual(p, exp)

