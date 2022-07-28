import unittest
from generativepy.drawing import setup, make_image
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.geometry import Image, Text
from generativepy.formulas import rasterise_formula
import math

"""
Test the formulas module.
"""


class TestGeometryImages(unittest.TestCase):

    def test_formula_default_dpi(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))
            image, size = rasterise_formula("formula-test-temp", r"\cosh{x} = \frac{e^{x}+e^{-x}}{2}", Color("dodgerblue"))
            Image(ctx).of_file_position(image, (50, 50)).paint()
            Text(ctx).of("Size = " + str(size), (50, 300)).size(20).fill(Color(0))

        def creator(file):
            make_image(file, draw, 800, 400)

        self.assertTrue(run_image_test('test_formula_default_dpi.png', creator))

    def test_formula_optional_package(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))
            image, size = rasterise_formula("formula-test-temp", r"\frac{a\cancel{b}}{\cancel{b}}\si{kg.m/s^2}", Color("crimson"), dpi=400, packages=["cancel", "siunitx"])
            Image(ctx).of_file_position(image, (50, 50)).paint()
            Text(ctx).of("Size = " + str(size), (50, 300)).size(20).fill(Color(0))

        def creator(file):
            make_image(file, draw, 800, 400)

        self.assertTrue(run_image_test('test_formula_optional_package.png', creator))

    def test_formula_dpi(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))
            image, size = rasterise_formula("formula-test-temp", r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}", Color("crimson"), dpi=400)
            Image(ctx).of_file_position(image, (50, 50)).paint()
            Text(ctx).of("Size = " + str(size), (50, 300)).size(20).fill(Color(0))

        def creator(file):
            make_image(file, draw, 800, 400)

        self.assertTrue(run_image_test('test_formula_dpi.png', creator))




