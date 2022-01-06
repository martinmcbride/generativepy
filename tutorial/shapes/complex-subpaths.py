# Author:  Martin McBride
# Created: 2022-01-05
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup, EVEN_ODD
from generativepy.color import Color
from generativepy.geometry import Line, Rectangle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    black = Color(0)

    Rectangle(ctx).of_corner_size((50, 50), 350, 250).add()
    Rectangle(ctx).of_corner_size((100, 100), 250, 150).as_sub_path()\
        .fill(Color('red'), fill_rule=EVEN_ODD)\
        .stroke(Color('blue'), 5)

make_image("complex-subpaths.png", draw, 500, 400)