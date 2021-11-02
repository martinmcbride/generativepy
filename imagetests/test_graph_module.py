import unittest
import math
from generativepy.drawing import setup, make_image, ROUND, BUTT
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.graph import Axes, Plot
from generativepy.geometry import LinearGradient

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
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'))
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'))

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
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'), line_width=3, dash=[5])
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'), line_width=5, dash=[10, 10, 20, 10],
                                cap=ROUND)
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'), line_width=4, dash=[5], cap=BUTT)

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_dashed_line.png', creator))

    def test_graph_scale_factor(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8))\
                        .with_feature_scale(2)
            axes.draw()

            # Add various curves
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'))
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_scale_factor.png', creator))


    def test_graph_subdivisions(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-100, -1.1)).of_extent((500, 2.2))\
                .with_divisions((90, 0.5)).with_subdivisions((2, 5))
            axes.draw()

            # Add curve. Deliberate low precision to test it works
            Plot(axes).of_function(lambda x: math.sin(x*math.pi/180), precision=25).stroke(pattern=Color('red'))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_subdivisions.png', creator))


    def test_graph_styles(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400)\
                .of_start((-100, -1.1))\
                .of_extent((500, 2.2))\
                .with_divisions((90, 0.5))\
                .with_subdivisions((2, 5))\
                .background(Color('wheat'))\
                .text_color(Color('darkgreen'))\
                .axis_linestyle(Color('darkblue'), line_width=3)\
                .division_linestyle(Color('steelblue'), line_width=3)\
                .subdivision_linestyle(Color('lightblue'), line_width=2, dash=[4, 2])
            axes.draw()

            # Add curve
            Plot(axes).of_function(lambda x: math.sin(x*math.pi/180), precision=100).stroke(pattern=Color('red'))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_styles.png', creator))


    def test_large_graph_scale(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(150, 150), width=1500, height=1200).of_start((-100, -1.1)).of_extent((500, 2.2))\
                .with_divisions((90, 0.5)).with_subdivisions((2, 5)).with_feature_scale(3)
            axes.draw()

            # Add curve. Deliberate low precision to test it works
            Plot(axes).of_function(lambda x: math.sin(x*math.pi/180), precision=25).stroke(pattern=Color('red'))

        def creator(file):
            make_image(file, draw, 1800, 1800)

        self.assertTrue(run_image_test('test_large_graph_scale.png', creator))


    def test_graph_gradient_background(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            gradient = LinearGradient().of_points((0, 50), (0, 450)).with_start_end(Color('white'), Color('skyblue')).build()

            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8))\
                                                                      .background(gradient)
            axes.draw()

            # Add various curves
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'))
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'))

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_gradient_background.png', creator))

    def test_graph_gradient_plot(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8))
            axes.draw()

            # Add various curves
            gradient = LinearGradient().of_points((0, 50), (0, 450)).with_start_end(Color('red'), Color('darkblue')).build()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=gradient, line_width=4)
            Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=gradient)
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=gradient)

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_graph_gradient_plot.png', creator))
