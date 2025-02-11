# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle


def draw_rgb(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color("cornflowerblue"))

    pos = [10, 10]
    w = 100
    h = 100

    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0, 0, 0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0.5, 0, 0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(1, 0, 0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0.5, 1, 0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0.5, 0, 1))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0, 1, .5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0.5, 0.5, 0.5))
    pos[0] += w


make_image("colour-rgb.png", draw_rgb, 720, 120)
