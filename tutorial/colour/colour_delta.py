# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle


from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle

def draw_delta(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(1))

    col = Color("cadetblue")

    pos = [10, 10]
    w = 100
    h = 100

    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_g_factor(0.8))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col)
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_g_factor(1.2))

    pos = [10, 120]

    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_l_factor(0.6))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col)
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_l_factor(1.4))

    pos = [10, 230]

    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_s_factor(0.6))
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col)
    pos[0] += w
    Rectangle(ctx).of_corner_size(pos, w, h).fill(col.with_s_factor(1.4))

make_image("colour-delta.png", draw_delta, 320, 340)