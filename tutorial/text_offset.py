# Author:  Martin McBride
# Created: 2021-05-02
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Circle, Line
import math


def draw_alpha(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(1))

    a = (100, 100)
    Circle(ctx).of_center_radius(a, 5).fill(Color('red'))
    Text(ctx).of("A", a).font("Arial").size(40).offset(20, 30).fill(Color(0))

    b = (300, 100)
    angle = math.pi*3/4
    x = (b[0]+150*math.cos(angle), b[1]+150*math.sin(angle))
    Line(ctx).of_start_end(b, x).stroke(Color('orange'), 4, dash=[5])
    Circle(ctx).of_center_radius(b, 5).fill(Color('red'))
    Text(ctx).of("B", b).font("Arial").size(40).offset_angle(angle, 100).fill(Color(0))

    c = (500, 100)
    d = (600, 50)
    Line(ctx).of_start_end(c, d).stroke(Color('orange'), 4, dash=[5])
    Circle(ctx).of_center_radius(c, 5).fill(Color('red'))
    Circle(ctx).of_center_radius(d, 5).fill(Color('blue'))
    Text(ctx).of("C", c).font("Arial").size(40).offset_towards(d, 30).fill(Color(0))


make_image("text-offset.png", draw_alpha, 700, 200)