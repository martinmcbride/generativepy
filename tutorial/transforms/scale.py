# Author:  Martin McBride
# Created: 2022-01-09
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Transform, Circle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    green = Color('green')
    thickness = 8

    Rectangle(ctx).of_corner_size((50, 40), 100, 30).fill(blue)

    with Transform(ctx).scale(1.5, 2):
        Rectangle(ctx).of_corner_size((50, 40), 100, 30).fill(red)


    with Transform(ctx) as t:
        Circle(ctx).of_center_radius((220, 260), 5).fill(green)
        Rectangle(ctx).of_corner_size((20, 160), 400, 200).stroke(blue, thickness)
        t.scale(0.5, 0.5, (220, 260))
        Rectangle(ctx).of_corner_size((20, 160), 400, 200).stroke(red, thickness)
        t.scale(0.5, 0.5, (220, 260))
        Rectangle(ctx).of_corner_size((20, 160), 400, 200).stroke(red, thickness)

make_image("scale-tutorial.png", draw, 450, 400)