import unittest
import cairo
from generativepy.geometry import Transform


class TestTransform(unittest.TestCase):

    def test_scale(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).scale(2, 3):
            self.assertEqual([2, 0, 0, 3, 0, 0], list(ctx.get_matrix()))

    def test_scale_centre(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).scale(2, 3, (50, 100)):
            self.assertEqual([2, 0, 0, 3, -50, -200], list(ctx.get_matrix()))

    def test_translate(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).translate(20, 30):
            self.assertEqual([1, 0, 0, 1, 20, 30], list(ctx.get_matrix()))

    def test_rotate(self):
        expected = [0.9950041652780258,
                    0.09983341664682815,
                    -0.09983341664682815,
                    0.9950041652780258,
                    0.0,
                    0.0]
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).rotate(0.1):
            self.assertEqual(expected, list(ctx.get_matrix()))

    def test_rotate_centre(self):
        expected = [0.9800665778412416,
                    0.19866933079506122,
                    -0.19866933079506122,
                    0.9800665778412416,
                    20.863604187444043,
                    -7.940124323877214]
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).rotate(0.2, (50, 100)):
            self.assertEqual(expected, list(ctx.get_matrix()))

    def test_nested_transforms(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).translate(1, 2):
            self.assertEqual([1, 0, 0, 1, 1, 2], list(ctx.get_matrix()))
            with Transform(ctx).scale(10, 20) as t:
                self.assertEqual([10, 0, 0, 20, 1, 2], list(ctx.get_matrix()))
                t.translate(5, 6)
                self.assertEqual([10, 0, 0, 20, 51, 122], list(ctx.get_matrix()))
            self.assertEqual([1, 0, 0, 1, 1, 2], list(ctx.get_matrix()))

    def test_matrix(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        with Transform(ctx).matrix([1, 0, 1, 0, 1, 2]):
            with Transform(ctx).matrix([10, 0, 0, 0, 20, 0]):
                with Transform(ctx).matrix([1, 0, 5, 0, 1, 6]):
                    # Note that ctx.get_matrix() return a cairo.Matrix. It has the elements in a different order to
                    # a generativepy.math.Matrix.
                    self.assertEqual([10.0, 0.0, 0.0, 20.0, 51.0, 122.0], list(ctx.get_matrix()))


if __name__ == '__main__':
    unittest.main()
