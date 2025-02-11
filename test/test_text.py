import unittest
import cairo
from generativepy.geometry import Text


class TestText(unittest.TestCase):

    # Test text extent
    def test_text_extent(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        x_bearing, y_bearing, width, height, x_advance, y_advance = Text(ctx).of('abc', (0, 0)).get_metrics()
        self.assertAlmostEqual(x_bearing, 0)
        self.assertAlmostEqual(y_bearing, -7)
        self.assertAlmostEqual(width, 17)
        self.assertAlmostEqual(height, 7)
        self.assertAlmostEqual(x_advance, 17)
        self.assertAlmostEqual(y_advance, 0)

    # Test text size
    def test_text_size(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        width, height = Text(ctx).of('abc', (0, 0)).get_size()
        self.assertAlmostEqual(width, 17)
        self.assertAlmostEqual(height, 7)

if __name__ == '__main__':
    unittest.main()
