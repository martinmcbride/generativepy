# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle


def draw_hsl(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color('cornflowerblue'))

    pos = [10, 10]
    w = 70
    h = 100

    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.1, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.2, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.3, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.4, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.5, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.6, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.7, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.8, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.9, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(1.0, 0.5, 0.5))
    pos[0] += w

    pos = [10, 120]
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.0, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.1, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.2, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.3, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.4, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.6, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.7, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.8, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 0.9, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.0, 1.0, 0.5))
    pos[0] += w

    pos = [10, 230]
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.1))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.2))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.3))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.4))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.6))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.7))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.8))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 0.9))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsl(0.66, 0.5, 1.0))
    pos[0] += w


make_image("colour-hsl.png", draw_hsl, 790, 340)
