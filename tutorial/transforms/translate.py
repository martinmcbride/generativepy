# Author:  Martin McBride
# Created: 2022-01-09
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Transform

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    thickness = 2

    Rectangle(ctx).of_corner_size((10, 10), 200, 150).stroke(blue, thickness)

    with Transform(ctx).translate(0, 200):
        Rectangle(ctx).of_corner_size((10, 10), 200, 150).stroke(red, thickness)


    with Transform(ctx) as t:
        Rectangle(ctx).of_corner_size((250, 100), 50, 150).fill(blue)
        t.translate(60, 10)
        Rectangle(ctx).of_corner_size((250, 100), 50, 150).fill(red)
        t.translate(60, 10)
        Rectangle(ctx).of_corner_size((250, 100), 50, 150).fill(red)

make_image("translate-tutorial.png", draw, 450, 400)