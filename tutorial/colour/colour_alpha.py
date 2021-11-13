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

def draw_alpha(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(1))

    Rectangle(ctx).of_corner_size((10, 50), 450, 20).fill(Color(0))

    pos = [20, 10]
    w = 100
    space =110
    h = 100

    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(1.0, 0.5, 0.0, 0.5))
    pos[0] += space
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color(0.6, 0.5))
    pos[0] += space
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color("tomato", 0.5))
    pos[0] += space
    Rectangle(ctx).of_corner_size(pos, w, h).fill(Color.of_hsla(0.4, 0.5, 0.5, 0.5))
    pos[0] += space

make_image("colour-alpha.png", draw_alpha, 470, 120)