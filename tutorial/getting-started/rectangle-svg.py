# Author:  Martin McBride
# Created: 2021-11-07
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create a simple rectangle image

from generativepy.drawing import setup, make_svg
from generativepy.color import Color
from generativepy.geometry import Rectangle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.4))

    color = Color(1, 0.5, 0)

    Rectangle(ctx).of_corner_size((100, 150), 250, 200).fill(color)

make_svg("rectangle-svg.svg", draw, 500, 400)