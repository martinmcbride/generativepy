import unittest
from generativepy.drawing import setup, make_image, BUTT, ROUND, BEVEL
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.geometry import LinearGradient, Text, Circle, circle, Bezier, Polygon, Square, square, Rectangle,\
                                  rectangle, Line, line, Ellipse, ellipse, tick, paratick, arrowhead, polygon,\
                                  angle_marker, Path, Triangle, triangle, Turtle
import math

"""
Test gradient fills
"""


class TestGradientImages(unittest.TestCase):

    def test_shapes_linear_gradient_fill(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=10, background=Color(0.8))

            gradient = LinearGradient().of_points((0, 1), (0, 3)).with_start_end(Color(0), Color('red')).build()
            Square(ctx).of_corner_size((1, 1), 2).fill(gradient)

            gradient = LinearGradient().of_points((3, 1), (6.2, 2.5)).with_start_end(Color(1), Color('green')).build()
            Rectangle(ctx).of_corner_size((4, 1), 2.2, 1.5).fill(gradient)

            gradient = LinearGradient().of_points((7, 1), (9, 1)).with_start_end(Color('blue'), Color('yellow')).build()
            Circle(ctx).of_center_radius((8, 2), 1.5).fill(gradient)

            gradient = LinearGradient().of_points((0, 4), (0, 6)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((1, 4), 2).fill(gradient)

            gradient = LinearGradient().of_points((4, 4), (6, 6)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (0.8, Color('green')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((4, 4), 2).fill(gradient)

            gradient = LinearGradient().of_points((7, 4), (7, 6)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (0.5, Color('blue')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((7, 4), 2).fill(gradient)

            gradient = LinearGradient().of_points((0, 7), (0, 9)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((1.1, 7.1), 1.8).stroke(gradient, .2)

            gradient = LinearGradient().of_points((4, 7), (6, 9)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (0.8, Color('green')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((4.1, 7.1), 1.8).stroke(gradient, .2)

            gradient = LinearGradient().of_points((7, 7), (7, 9)).with_stops(((0, Color(0)),
                                                                              (0.5, Color('red')),
                                                                              (0.5, Color('blue')),
                                                                              (1.0, Color('blue')))).build()
            Square(ctx).of_corner_size((7.1, 7.1), 1.8).stroke(gradient, .2)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_shapes_linear_gradient_fill.png', creator))

