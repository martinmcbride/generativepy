import unittest
from generativepy.color import Color


class TestColour(unittest.TestCase):

    # Test RGB and RGBA colours
    def test_rgb_rgb_black(self):
        color = Color(0, 0, 0)
        self.assertEqual(color.get_rgb(), (0, 0, 0))

    def test_rgb_rgb_color(self):
        color = Color(1, 0.5, 0.25)
        self.assertEqual(color.get_rgb(), (1, 0.5, 0.25))

    def test_rgb_rgba_black(self):
        color = Color(0, 0, 0)
        self.assertEqual(color.get_rgba(), (0, 0, 0, 1))

    def test_rgb_rgba_color(self):
        color = Color(1, 0.5, 0.25)
        self.assertEqual(color.get_rgba(), (1, 0.5, 0.25, 1))

    def test_rgba_rgba_transparent(self):
        color = Color(0, 0, 0, 0)
        self.assertEqual(color.get_rgba(), (0, 0, 0, 0))

    def test_rgba_rgba_semi(self):
        color = Color(1, 0.5, 0.25, 0.4)
        self.assertEqual(color.get_rgba(), (1, 0.5, 0.25, 0.4))

    def test_grey_rgb_black(self):
        color = Color(0)
        self.assertEqual(color.get_rgb(), (0, 0, 0))

    # Test grey and grey+alpha modes
    def test_grey_rgb_color(self):
        color = Color(0.25)
        self.assertEqual(color.get_rgb(), (0.25, 0.25, 0.25))

    def test_grey_rgba_black(self):
        color = Color(0)
        self.assertEqual(color.get_rgba(), (0, 0, 0, 1))

    def test_grey_rgba_color(self):
        color = Color(0.25)
        self.assertEqual(color.get_rgba(), (0.25, 0.25, 0.25, 1))

    def test_greya_rgba_transparent(self):
        color = Color(0, 0)
        self.assertEqual(color.get_rgba(), (0, 0, 0, 0))

    def test_greya_rgba_semi(self):
        color = Color(0.25, 0.4)
        self.assertEqual(color.get_rgba(), (0.25, 0.25, 0.25, 0.4))

    # Test CSS and CSS plus alpha modes
    def test_css_rgb(self):
        color = Color('salmon')
        self.assertAlmostEqual(color.get_rgb()[0], 0.98039215)
        self.assertAlmostEqual(color.get_rgb()[1], 0.50196078)
        self.assertAlmostEqual(color.get_rgb()[2], 0.44705882)

    def test_css_rgba(self):
        color = Color('salmon')
        self.assertAlmostEqual(color.get_rgba()[0], 0.98039215)
        self.assertAlmostEqual(color.get_rgba()[1], 0.50196078)
        self.assertAlmostEqual(color.get_rgba()[2], 0.44705882)
        self.assertAlmostEqual(color.get_rgba()[3], 1)

    def test_cssa_rgba_transparent(self):
        color = Color('salmon', 0)
        self.assertAlmostEqual(color.get_rgba()[0], 0.98039215)
        self.assertAlmostEqual(color.get_rgba()[1], 0.50196078)
        self.assertAlmostEqual(color.get_rgba()[2], 0.44705882)
        self.assertAlmostEqual(color.get_rgba()[3], 0)

    def test_cssa_rgba_semi(self):
        color = Color('salmon', 0.7)
        self.assertAlmostEqual(color.get_rgba()[0], 0.98039215)
        self.assertAlmostEqual(color.get_rgba()[1], 0.50196078)
        self.assertAlmostEqual(color.get_rgba()[2], 0.44705882)
        self.assertAlmostEqual(color.get_rgba()[3], 0.7)


if __name__ == '__main__':
    unittest.main()
