# Author:  Martin McBride
# Created: 2022-01-09
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Transform, Line

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')
    green = Color('green')
    thickness = 4

    Text(ctx).of('F', (40, 100)).size(100).fill(blue)
    Line(ctx).of_start_end((100, 20), (100, 110)).stroke(green, thickness)

    with Transform(ctx).scale(-1, 1, (100, 0)):
        Text(ctx).of('F', (40, 100)).size(100).fill(red)

    Text(ctx).of('W', (240, 100)).size(100).fill(blue)
    Line(ctx).of_start_end((240, 70), (340, 70)).stroke(green, thickness)

    with Transform(ctx).scale(1, -1, (0, 60)):
        Text(ctx).of('W', (240, 100)).size(100).fill(red.with_a(0.6))


make_image("mirror-tutorial.png", draw, 450, 150)