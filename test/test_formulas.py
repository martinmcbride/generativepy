import unittest

from generativepy.color import Color

from generativepy.formulas import rasterise_formula

from generativepy.geometry import Text


class TestFormulas(unittest.TestCase):

    # Test with a valid formula
    def test_formula_valid(self):
        image, size = rasterise_formula("formula-valid-temp", r"e^x", Color("crimson"), dpi=400)
        self.assertEqual(size, (46, 40))

    # Test with an invalid formula
    def test_formula_invalid(self):
        image, size = rasterise_formula("formula-invalid-temp", r"}e^x", Color("crimson"), dpi=400)
        self.assertEqual(size, (46, 40))


    # Test with an empty formula
    def test_formula_null(self):
        image, size = rasterise_formula("formula-empty-temp", r"", Color("crimson"), dpi=400)
        self.assertEqual(size, (1, 1))


if __name__ == '__main__':
    unittest.main()
