import unittest
from generativepy.drawing import setup, make_image, ROUND, BUTT
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.graph import Axes, Plot

"""
Test the graph module.
"""


class TestGraphImages(unittest.TestCase):

    def test_graph_simple(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8))
            axes.draw()

            # Add various curves
            Plot(axes).of_function(lambda x: x * x).stroke(color=Color('red'))
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(color=Color('green'))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(color=Color('blue'))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_simple.png', creator))

    def test_graph_dashed_line(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=300, height=500).of_start((-4, -1)).of_extent((6, 10))
            axes.draw()

            # Add various curves
            Plot(axes).of_function(lambda x: x * x).stroke(color=Color('red'), line_width=3, dash=[5])
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(color=Color('green'), line_width=5, dash=[10, 10, 20, 10],
                                cap=ROUND)
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(color=Color('blue'), line_width=4, dash=[5], cap=BUTT)

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_dashed_line.png', creator))

