# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle


def draw_lerp(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color('cornflowerblue'))

    color1 = Color('red')
    color2 = Color('blue')

    pos = [10, 10]
    w = 100
    h = 100

    Rectangle(ctx).of_corner_size(pos, w, h).fill(color1.lerp(color2, 0))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(color1.lerp(color2, 0.25))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(color1.lerp(color2, 0.5))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(color1.lerp(color2, 0.75))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(color1.lerp(color2, 1))
    pos[0] += w


make_image("colour-lerp.png", draw_lerp, 520, 120)