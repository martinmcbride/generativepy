import unittest
import math
from generativepy.drawing import (
    setup,
    make_image,
    ROUND,
    BUTT,
    FONT_SLANT_ITALIC,
    FONT_WEIGHT_NORMAL,
    BASELINE,
)
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.graph import Axes, Plot, Scatter, SCATTER_CONNECTED, SCATTER_STALK
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
            axes.clip()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color("red"))
            Plot(axes).of_xy_function(lambda x: 1.5**x).stroke(pattern=Color("green"))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color("blue"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_simple.png", creator))

    def test_graph_multiple(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
            axes.draw()

            # Add various curves
            formula1 = lambda x: math.exp(x)
            formula2 = lambda x: -math.exp(-x)
            formula3 = lambda x: (math.exp(x) - math.exp(-x)) / 2

            axes.clip()
            Plot(axes).of_function(formula1, [-5, 3]).stroke(Color(0, 1, 1), line_width=4)
            Plot(axes).of_function(formula2, [-3, 5]).stroke(Color(1, 0, 1), line_width=4)
            Plot(axes).of_function(formula3, [-3, 3]).stroke(Color(1, 1, 0), line_width=4)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_multiple.png", creator))

    def test_graph_extent(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
            axes.draw()

            # Add various curves
            formula1 = lambda x: math.sin(x)
            formula2 = lambda x: math.sin(x) + 2
            formula3 = lambda x: math.sin(x) - 2

            axes.clip()
            Plot(axes).of_function(formula1, [-7, 1]).stroke(Color(0, 1, 1), line_width=4)
            Plot(axes).of_function(formula2, [-3, 2]).stroke(Color(1, 0, 1), line_width=4)
            Plot(axes).of_function(formula3, [-2, 7]).stroke(Color(1, 1, 0), line_width=4)
            Plot(axes).of_xy_function(formula1, [-7, 1]).stroke(Color(0, 1, 1), line_width=4)
            Plot(axes).of_xy_function(formula2, [-3, 2]).stroke(Color(1, 0, 1), line_width=4)
            Plot(axes).of_xy_function(formula3, [-2, 7]).stroke(Color(1, 1, 0), line_width=4)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_extent.png", creator))

    def test_graph_filled(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
            axes.draw()

            # Add various curves
            formula1 = lambda x: math.sin(x)
            formula2 = lambda x: 2 * x
            formula3 = lambda x: 4 * math.cos(x)
            formula4 = lambda x: 4 * math.sin(x)

            axes.clip()
            Plot(axes).of_function(formula1).stroke(Color("cyan"), line_width=4)
            Plot(axes).of_function(formula1, [-2, -1], close=((-1, 0), (-2, 0))).fill(Color("cyan", 0.5)).stroke(Color("cyan"), line_width=4)
            Plot(axes).of_xy_function(formula1).stroke(Color("red"), line_width=4)
            Plot(axes).of_xy_function(formula1, [-2, -1], close=((0, -1), (0, -2))).fill(Color("red", 0.5)).stroke(Color("red"), line_width=4)
            Plot(axes).of_polar_function(formula2).stroke(Color("orange"), line_width=4)
            Plot(axes).of_polar_function(formula2, [1, 2], close=((0, 0),)).fill(Color("orange", 0.5)).stroke(Color("orange"), line_width=4)
            Plot(axes).of_parametric_function(formula3, formula4, (0, math.pi * 2)).stroke(Color("blue"), line_width=4)
            Plot(axes).of_parametric_function(formula3, formula4, (5.5, 6), close=((0, 0),)).fill(Color("blue", 0.5)).stroke(Color("blue"), line_width=4)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_filled.png", creator))

    def test_graph_dashed_line(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=300, height=500).of_start((-4, -1)).of_extent((6, 10))
            axes.draw()

            # Add various curves
            axes.clip()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color("red"), line_width=3, dash=[5])
            Plot(axes).of_xy_function(lambda x: 1.5**x).stroke(pattern=Color("green"), line_width=5, dash=[10, 10, 20, 10], cap=ROUND)
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color("blue"), line_width=4, dash=[5], cap=BUTT)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_dashed_line.png", creator))

    def test_graph_scale_factor(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8)).with_feature_scale(2)
            axes.draw()

            # Add various curves
            axes.clip()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color("red"))
            Plot(axes).of_xy_function(lambda x: 1.5**x).stroke(pattern=Color("green"))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color("blue"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_scale_factor.png", creator))

    def test_graph_subdivisions(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = (
                Axes(ctx, position=(50, 50), width=500, height=400)
                .of_start((-100, -1.1))
                .of_extent((500, 2.2))
                .with_divisions((90, 0.5))
                .with_subdivisions((2, 5))
            )
            axes.draw()

            # Add curve. Deliberate low precision to test it works
            axes.clip()
            Plot(axes).of_function(lambda x: math.sin(x * math.pi / 180), precision=25).stroke(pattern=Color("red"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_subdivisions.png", creator))

    def test_graph_styles(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = (
                Axes(ctx, position=(50, 50), width=500, height=400)
                .of_start((-100, -1.1))
                .of_extent((500, 2.2))
                .with_divisions((90, 0.5))
                .with_subdivisions((2, 5))
                .background(Color("wheat"))
                .text_color(Color("darkgreen"))
                .text_style(
                    font="Times",
                    size=20,
                    slant=FONT_SLANT_ITALIC,
                    weight=FONT_WEIGHT_NORMAL,
                )
                .axis_linestyle(Color("darkblue"), line_width=3)
                .division_linestyle(Color("steelblue"), line_width=3)
                .subdivision_linestyle(Color("lightblue"), line_width=2, dash=[4, 2])
            )
            axes.draw()

            # Add curve
            axes.clip()
            Plot(axes).of_function(lambda x: math.sin(x * math.pi / 180), precision=100).stroke(pattern=Color("red"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_styles.png", creator))

    def test_large_graph_scale(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = (
                Axes(ctx, position=(150, 150), width=1500, height=1200)
                .of_start((-100, -1.1))
                .of_extent((500, 2.2))
                .with_divisions((90, 0.5))
                .with_subdivisions((2, 5))
                .with_feature_scale(3)
            )
            axes.draw()

            # Add curve. Deliberate low precision to test it works
            axes.clip()
            Plot(axes).of_function(lambda x: math.sin(x * math.pi / 180), precision=25).stroke(pattern=Color("red"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 1800, 1800)

        self.assertTrue(run_image_test("test_large_graph_scale.png", creator))

    def test_graph_gradient_background(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            gradient = LinearGradient().of_points((0, 50), (0, 450)).with_start_end(Color("white"), Color("skyblue")).build()

            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8)).background(gradient)
            axes.draw()

            # Add various curves
            axes.clip()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color("red"))
            Plot(axes).of_xy_function(lambda x: 1.5**x).stroke(pattern=Color("green"))
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color("blue"))
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_gradient_background.png", creator))

    def test_graph_gradient_plot(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a set of axes.
            axes = Axes(ctx, position=(50, 50), width=500, height=400).of_start((-4, -3)).of_extent((10, 8))
            axes.draw()

            # Add various curves
            gradient = LinearGradient().of_points((0, 50), (0, 450)).with_start_end(Color("red"), Color("darkblue")).build()
            axes.clip()
            Plot(axes).of_function(lambda x: x * x).stroke(pattern=gradient, line_width=4)
            Plot(axes).of_xy_function(lambda x: 1.5**x).stroke(pattern=gradient)
            Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=gradient)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_gradient_plot.png", creator))

    def test_graph_formatted_axis_values(self):
        def a_div_formatter(value, div):
            """
            Replace +1 amd -1 with a snd -a, leave others blank
            :param value:
            :param div:
            :return:
            """
            if value - div / 2 < 1 < value + div / 2:
                return "a"

            if value - div / 2 < -1 < value + div / 2:
                return "-a"

            return ""

        def pi_div_formatter(value, div):
            """
            Replace n with n*pi
            :param value:
            :param div:
            :return:
            """
            if value - div / 2 < 1 < value + div / 2:
                return "π"

            if value - div / 2 < -1 < value + div / 2:
                return "-π"

            return str(value) + "π"

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
            axes.with_division_formatters(pi_div_formatter, a_div_formatter)
            axes.draw()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_formatted_axis_values.png", creator))

    def test_graph_multiple(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            axes = Axes(ctx, (50, 50), 500, 500).of_start((-1, -1)).of_extent((11, 11))
            axes.draw()

            # Add various data
            x1 = [1, 2, 3, 4, 5]
            y1 = [2, 5, 4, 1, 3]
            x2 = [1, 2, 3, 4, 5]
            y2 = [6, 9, 8, 5, 7]
            x3 = [4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
            y3 = [2, 5, 4, 1, 3]

            axes.clip()
            Scatter(axes).with_line_style(Color("red"), 4).with_point_style(6, pattern=Color("blue")).plot(x1, y1)
            Scatter(axes).with_line_style(SCATTER_CONNECTED, Color("green"), 4).with_point_style(6, pattern=Color("magenta")).plot(x2, y2)
            Scatter(axes).with_line_style(SCATTER_STALK, Color("yellow"), 4).with_point_style(6, pattern=Color("orange")).plot(x3, y3)
            axes.unclip()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_graph_scatter.png", creator))
