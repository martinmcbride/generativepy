# Author:  Martin McBride
# Created: 2022-01-10
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Circle

def draw_rect(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.4))
    color = Color(1, 0.5, 0)
    Rectangle(ctx).of_corner_size((1, 1.5), 2.5, 2).fill(color)

make_image("user-scale.png", draw_rect, 500, 400)