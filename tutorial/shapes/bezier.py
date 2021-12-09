# Author:  Martin McBride
# Created: 2021-12-09
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create some ellipses, arcs etc

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Bezier, Polygon, Line, Circle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    thickness = 2

    Bezier(ctx).of_abcd((50, 150), (100, 50), (150, 50), (200, 150)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((250, 150), (250, 50), (350, 50), (400, 150)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((50, 350), (100, 250), (150, 450), (200, 350)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((250, 350), (450, 250), (200, 250), (400, 350)).stroke(blue, thickness)

make_image("bezier-tutorial.png", draw, 500, 500)

def show_bezier(ctx, a, b, c, d):
    blue = Color('blue')
    red = Color('red')
    grey = Color(0,7)
    thickness = 2
    Bezier(ctx).of_abcd(a, b, c, d).stroke(blue, thickness)
    Line(ctx).of_start_end(a, b).stroke(grey, thickness, dash=[5])
    Line(ctx).of_start_end(c, d).stroke(grey, thickness, dash=[5])
    Circle(ctx).of_center_radius(a, 5).fill(red)
    Circle(ctx).of_center_radius(b, 5).fill(red)
    Circle(ctx).of_center_radius(c, 5).fill(red)
    Circle(ctx).of_center_radius(d, 5).fill(red)


def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    thickness = 2

    show_bezier(ctx, (50, 150), (100, 50), (150, 50), (200, 150))
    show_bezier(ctx, (250, 150), (250, 50), (350, 50), (400, 150))
    show_bezier(ctx, (50, 350), (100, 250), (150, 450), (200, 350))
    show_bezier(ctx, (250, 350), (450, 250), (200, 250), (400, 350))

make_image("bezier-tutorial-points.png", draw2, 500, 500)

def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    thickness = 4
    points = [(100, 250), (100, 50), (200, 100, 300, 200, 400, 50), (400, 250)]
    Polygon(ctx).of_points(points).fill(red).stroke(blue, thickness)

make_image("bezier-tutorial-polygon.png", draw3, 500, 300)