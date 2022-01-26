# Author:  Martin McBride
# Created: 2022-01-22
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.color import Color
from generativepy.drawing import make_image, setup
import math

from generativepy.geometry import Polygon, Transform

def create_spiro(a, b, d):
    dt = 0.01
    t = 0
    pts = []
    while t < 2*math.pi*b/math.gcd(a, b):
        t += dt
        x = (a - b) * math.cos(t) + d * math.cos((a - b)/b * t)
        y = (a - b) * math.sin(t) - d * math.sin((a - b)/b * t)
        pts.append((x, y))
    return pts


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 14
    b = 6
    d = 4
    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('red'), line_width=0.1)


make_image("spirograph.png", draw, 600, 600)

def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 16
    b = 13
    d = 5
    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('firebrick'), line_width=0.1)

    a = 16
    b = 9
    d = 8
    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('goldenrod'), line_width=0.1)

    a = 16
    b = 11
    d = 6
    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('darkgreen'), line_width=0.1)


make_image("spirograph2.png", draw2, 600, 600)

def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    for i in range(6):
        a = 13
        b = 7
        d = 5
        with Transform(ctx).rotate(0.05*i):
            Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('dodgerblue').with_l_factor(1.1**i), line_width=0.1)


make_image("spirograph3.png", draw3, 600, 600)

