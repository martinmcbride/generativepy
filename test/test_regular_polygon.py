import math
import unittest
import cairo
from generativepy.geometry import RegularPolygon


class TestRegularPolygon(unittest.TestCase):

    def test_angle_3(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        p = RegularPolygon(ctx).of_centre_sides_radius((0, 0), 3, 100)
        self.assertAlmostEqual(math.degrees(p.interior_angle), 60)
        self.assertAlmostEqual(math.degrees(p.exterior_angle), 120)

    def test_angle_4(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        p = RegularPolygon(ctx).of_centre_sides_radius((0, 0), 4, 100)
        self.assertAlmostEqual(math.degrees(p.interior_angle), 90)
        self.assertAlmostEqual(math.degrees(p.exterior_angle), 90)

    def test_angle_5(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        p = RegularPolygon(ctx).of_centre_sides_radius((0, 0), 5, 100)
        self.assertAlmostEqual(math.degrees(p.interior_angle), 108)
        self.assertAlmostEqual(math.degrees(p.exterior_angle), 72)

    def test_angle_6(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        p = RegularPolygon(ctx).of_centre_sides_radius((0, 0), 6, 100)
        self.assertAlmostEqual(math.degrees(p.interior_angle), 120)
        self.assertAlmostEqual(math.degrees(p.exterior_angle), 60)


if __name__ == '__main__':
    unittest.main()
