# Author:  Martin McBride
# Created: 2022-01-09
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Transform

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    red = Color('red')

    with Transform(ctx).translate(50, 150):
        with Transform(ctx).matrix([1, 0, -0.5, 1, 0, 0]):
            print(ctx.get_matrix())
            Text(ctx).of('A', (0, 0)).size(100).fill(red)
        Text(ctx).of('B', (80, 0)).size(100).fill(blue)


make_image("advanced-transform.png", draw, 450, 200)