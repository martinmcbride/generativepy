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

    # Test getters
    def test_get_r(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_r()
        self.assertEqual(val, 0.1)

    def test_get_g(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_g()
        self.assertEqual(val, 0.2)

    def test_get_b(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_b()
        self.assertEqual(val, 0.3)

    def test_get_a(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_a()
        self.assertEqual(val, 0.4)

    def test_get_h(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_h()
        self.assertAlmostEqual(val, 0.58333333)

    def test_get_s(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_s()
        self.assertAlmostEqual(val, 0.5)

    def test_get_l(self):
        val = Color(0.1, 0.2, 0.3, 0.4).get_l()
        self.assertAlmostEqual(val, 0.2)

    # Test setters
    def test_with_r(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_r(0.5)
        self.assertEqual(color.get_rgba(), (0.5, 0.2, 0.3, 0.4))

    def test_with_g(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_g(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.5, 0.3, 0.4))

    def test_with_b(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_b(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.2, 0.5, 0.4))

    def test_with_a(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_a(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.2, 0.3, 0.5))

    def test_with_h(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_h(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.1)
        self.assertAlmostEqual(color.get_rgba()[1], 0.3)
        self.assertAlmostEqual(color.get_rgba()[2], 0.3)
        self.assertAlmostEqual(color.get_rgba()[3], 0.4)

    def test_with_s(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_s(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.1)
        self.assertAlmostEqual(color.get_rgba()[1], 0.2)
        self.assertAlmostEqual(color.get_rgba()[2], 0.3)
        self.assertAlmostEqual(color.get_rgba()[3], 0.4)

    def test_with_l(self):
        color = Color(0.1, 0.2, 0.3, 0.4).with_l(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.25)
        self.assertAlmostEqual(color.get_rgba()[1], 0.5)
        self.assertAlmostEqual(color.get_rgba()[2], 0.75)
        self.assertAlmostEqual(color.get_rgba()[3], 0.4)

    # Test set factors
    def test_with_r_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_r_factor(0.5)
        self.assertEqual(color.get_rgba(), (0.05, 0.3, 0.5, 0.7))

    def test_with_g_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_g_factor(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.15, 0.5, 0.7))

    def test_with_b_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_b_factor(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.3, 0.25, 0.7))

    def test_with_a_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_a_factor(0.5)
        self.assertEqual(color.get_rgba(), (0.1, 0.3, 0.5, 0.35))

    def test_with_h_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_h_factor(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.2)
        self.assertAlmostEqual(color.get_rgba()[1], 0.5)
        self.assertAlmostEqual(color.get_rgba()[2], 0.1)
        self.assertAlmostEqual(color.get_rgba()[3], 0.7)

    def test_with_s_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_s_factor(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.2)
        self.assertAlmostEqual(color.get_rgba()[1], 0.3)
        self.assertAlmostEqual(color.get_rgba()[2], 0.4)
        self.assertAlmostEqual(color.get_rgba()[3], 0.7)

    def test_with_l_factor(self):
        color = Color(0.1, 0.3, 0.5, 0.7).with_l_factor(0.5)
        self.assertAlmostEqual(color.get_rgba()[0], 0.05)
        self.assertAlmostEqual(color.get_rgba()[1], 0.15)
        self.assertAlmostEqual(color.get_rgba()[2], 0.25)
        self.assertAlmostEqual(color.get_rgba()[3], 0.7)

    # Test lerp function
    def test_lerp_0(self):
        color = (Color(0.1, 0.2, 0.3, 0.4).lerp(Color(0.6, 0.7, 0.8, 0.9), 0))
        self.assertEqual(color.get_rgba(), (0.1, 0.2, 0.3, 0.4))

    def test_lerp_1(self):
        color = (Color(0.1, 0.2, 0.3, 0.4).lerp(Color(0.6, 0.7, 0.8, 0.9), 1))
        self.assertEqual(color.get_rgba(), (0.6, 0.7, 0.8, 0.9))

    def test_lerp_0_6(self):
        color = (Color(0.1, 0.2, 0.3, 0.4).lerp(Color(0.6, 0.7, 0.8, 0.9), 0.6))
        self.assertAlmostEqual(color.get_rgba()[0], 0.4)
        self.assertAlmostEqual(color.get_rgba()[1], 0.5)
        self.assertAlmostEqual(color.get_rgba()[2], 0.6)
        self.assertAlmostEqual(color.get_rgba()[3], 0.7)


if __name__ == '__main__':
    unittest.main()
