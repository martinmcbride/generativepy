import unittest
from generativepy.drawing import setup, make_image, ROUND, BUTT
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.graph import Axes, plot_curve, plot_xy_curve, plot_polar_curve

"""
Test the graph module.
"""


class TestGraphImages(unittest.TestCase):

    def test_graph_simple(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=12, startx=-6, starty=-6, background=Color(1), flip=True)

            # Creates a set of axes.
            # Use the default size of 10 units, but offset the start toplace the origin inthe centre
            axes = Axes(ctx, start=(-5, -5))
            axes.draw()

            # Add various curves
            plot_curve(axes, lambda x: x * x)
            plot_xy_curve(axes, lambda x: 1.5 ** x, line_color=Color(0, 0, 0.5))
            plot_polar_curve(axes, lambda x: 2 * x, line_color=Color(0, 0.5, 0))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_simple.png', creator))

    def test_graph_dashed_line(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=12, startx=-6, starty=-6, background=Color(1), flip=True)

            # Creates a set of axes.
            # Use the default size of 10 units, but offset the start toplace the origin inthe centre
            axes = Axes(ctx, start=(-5, -5))
            axes.draw()

            # Add various curves
            plot_curve(axes, lambda x: x * x, line_width=2, dash=[5])
            plot_xy_curve(axes, lambda x: 1.5 ** x, line_color=Color(0, 0, 0.5), line_width=2, dash=[5, 5, 10, 5],
                                cap=ROUND)
            plot_polar_curve(axes, lambda x: 2 * x, line_color=Color(0, 0.5, 0), line_width=2, dash=[5], cap=BUTT)

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_dashed_line.png', creator))

