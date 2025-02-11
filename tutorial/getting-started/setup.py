# Author:  Martin McBride
# Created: 2021-11-07
# Copyright (C) 2021, Martin McBride
# License: MIT

# Example of setup function

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, width=5, background=Color(0.4))

    color = Color(1, 0.5, 0)

    Rectangle(ctx).of_corner_size((1, 1.5), 2.5, 2).fill(color)

make_image("setup.png", draw, 500, 400)