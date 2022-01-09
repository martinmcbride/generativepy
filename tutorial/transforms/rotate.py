# Author:  Martin McBride
# Created: 2022-01-09
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Transform, Circle
import math

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    green = Color('green')
    thickness = 4

    Rectangle(ctx).of_corner_size((100, 20), 100, 50).fill(blue)

    with Transform(ctx).rotate(math.pi/4):
        Rectangle(ctx).of_corner_size((100, 20), 100, 50).fill(red)

    with Transform(ctx) as t:
        Rectangle(ctx).of_corner_size((200, 150), 100, 100).stroke(blue, thickness)
        t.rotate(math.pi/6, (200, 150))
        Rectangle(ctx).of_corner_size((200, 150), 100, 100).stroke(red, thickness)
        t.rotate(math.pi/6, (200, 150))
        Rectangle(ctx).of_corner_size((200, 150), 100, 100).stroke(red, thickness)
        Circle(ctx).of_center_radius((200, 150), 5).fill(green)

make_image("rotate-tutorial.png", draw, 450, 400)