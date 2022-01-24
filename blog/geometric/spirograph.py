# Author:  Martin McBride
# Created: 2022-01-22
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.color import Color
from generativepy.drawing import make_image, setup
import math

from generativepy.geometry import Polygon

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
    a = 16
    b = 11
    d = 9
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('red'), line_width=0.1)


make_image("spirograph.png", draw, 600, 600)

