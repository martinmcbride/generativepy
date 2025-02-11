# Author:  Martin McBride
# Created: 2021-12-09
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create some bezier curves

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Bezier, Polygon, Line, Circle, Text

# Draw some Bezier curves
def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    thickness = 2

    Bezier(ctx).of_abcd((50, 150), (100, 50), (150, 50), (200, 150)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((250, 150), (250, 50), (350, 50), (400, 150)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((50, 350), (100, 250), (150, 450), (200, 350)).stroke(blue, thickness)
    Bezier(ctx).of_abcd((250, 350), (450, 250), (200, 250), (400, 350)).stroke(blue, thickness)

make_image("bezier-tutorial.png", draw, 500, 500)

# Draw a curve marking the control points
def show_bezier_points(ctx, a, b, c, d):
    blue = Color('blue')
    red = Color('red')
    grey = Color(0.2)
    thickness = 2
    Bezier(ctx).of_abcd(a, b, c, d).stroke(blue, thickness)
    Line(ctx).of_start_end(a, b).stroke(grey, thickness, dash=[5])
    Line(ctx).of_start_end(c, d).stroke(grey, thickness, dash=[5])
    Circle(ctx).of_center_radius(a, 5).fill(red)
    Circle(ctx).of_center_radius(b, 5).fill(red)
    Circle(ctx).of_center_radius(c, 5).fill(red)
    Circle(ctx).of_center_radius(d, 5).fill(red)

# Draw a curve marking the control points
def show_bezier_labels(ctx, a, b, c, d):
    grey = Color(0.2)
    thickness = 2
    show_bezier_points(ctx, a, b, c, d)
    Text(ctx).of('a', a).size(20).align_center().align_middle().offset_towards(b, -20).fill(grey)
    Text(ctx).of('b', b).size(20).align_center().align_middle().offset_towards(a, -20).fill(grey)
    Text(ctx).of('c', c).size(20).align_center().align_middle().offset_towards(d, -20).fill(grey)
    Text(ctx).of('d', d).size(20).align_center().align_middle().offset_towards(c, -20).fill(grey)

# Draw the previous curves with their control points
def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    show_bezier_labels(ctx, (50, 150), (100, 50), (150, 50), (200, 150))
    show_bezier_labels(ctx, (250, 150), (250, 50), (350, 50), (400, 150))
    show_bezier_labels(ctx, (50, 350), (100, 250), (150, 450), (200, 350))
    show_bezier_labels(ctx, (250, 350), (450, 250), (200, 250), (400, 350))

make_image("bezier-tutorial-points.png", draw2, 500, 500)

## Draw a polygon
def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    thickness = 4
    points = [(100, 250), (100, 50), (200, 100, 300, 200, 400, 50), (400, 250)]
    Polygon(ctx).of_points(points).fill(red).stroke(blue, thickness)

make_image("bezier-tutorial-polygon.png", draw3, 500, 300)

## Draw two smoothly joined points

def draw4(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    grey = Color(0.2)
    thickness = 2

    a0 = (50, 200)
    b0 = (100, 200)
    c0 = (100, 50)
    d0 = (200, 50)
    a1 = (200, 50)
    b1 = (300, 50)
    c1 = (350, 220)
    d1 = (450, 200)
    points = [a0, (*b0, *c0, *d0), (*b1, *c1, *d1)]
    Polygon(ctx).of_points(points).open().stroke(blue, thickness)

    show_bezier_points(ctx, (50, 200), (100, 200), (100, 50), (200, 50))
    show_bezier_points(ctx, (200, 50), (300, 50), (350, 220), (450, 200))

    Text(ctx).of('a0', a0).size(20).align_center().align_middle().offset_towards(b0, -20).fill(grey)
    Text(ctx).of('b0', b0).size(20).align_center().align_middle().offset_towards(a0, -20).fill(grey)
    Text(ctx).of('c0', c0).size(20).align_center().align_middle().offset_towards(d0, -20).fill(grey)
    Text(ctx).of('d0/a1', d0).size(20).align_center().align_middle().offset(0, -20).fill(grey)
    Text(ctx).of('b1', b1).size(20).align_center().align_middle().offset_towards(a1, -20).fill(grey)
    Text(ctx).of('c1', c1).size(20).align_center().align_middle().offset_towards(d1, -20).fill(grey)
    Text(ctx).of('d1', d1).size(20).align_center().align_middle().offset_towards(c1, -20).fill(grey)


make_image("bezier-tutorial-joined.png", draw4, 500, 250)

