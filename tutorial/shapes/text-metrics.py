# Author:  Martin McBride
# Created: 2022-01-04
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Rectangle


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    x, y = 50, 100
    text = Text(ctx).of("Text size", (x, y)).font("Times").size(100).fill(Color('blue'))
    width, height = text.get_size()
    Text(ctx).of('{} by {}'.format(width, height), (x+400, y))\
        .font("Times").size(40).fill(Color('black'))


    x, y = 50, 200
    text = Text(ctx).of("xyz", (x, y)).font("Times").size(100).fill(Color('blue'))
    width, height = text.get_size()
    Text(ctx).of('{} by {}'.format(width, height), (x+400, y))\
        .font("Times").size(40).fill(Color('black'))

    x, y = 50, 300
    text = Text(ctx).of("Text extents", (x, y)).font("Times").size(100).fill(Color('blue'))
    x_bearing, y_bearing, width, height, x_advance, y_advance = text.get_metrics()
    Rectangle(ctx).of_corner_size((x + x_bearing, y+y_bearing), width, height).stroke(Color('red'))

    x, y = 50, 400
    text = Text(ctx).of("xyz", (x, y)).font("Times").size(100).fill(Color('blue'))
    x_bearing, y_bearing, width, height, x_advance, y_advance = text.get_metrics()
    Rectangle(ctx).of_corner_size((x + x_bearing, y + y_bearing), width, height).stroke(Color('red'))

    x, y = 300, 400
    text = Text(ctx).of("'''", (x, y)).font("Times").size(100).fill(Color('blue'))
    x_bearing, y_bearing, width, height, x_advance, y_advance = text.get_metrics()
    Rectangle(ctx).of_corner_size((x + x_bearing, y + y_bearing), width, height).stroke(Color('red'))


make_image("text-metrics.png", draw, 700, 500)