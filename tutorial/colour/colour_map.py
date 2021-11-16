# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color, make_colormap
from generativepy.geometry import Rectangle


def draw_map(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(0.5))

    w = 2
    h = 100

    pos = [10, 10]
    colormap = make_colormap(256, [Color('red'), Color('blue')])
    for i in range(256):
        Rectangle(ctx).of_corner_size(pos, w, h).fill(colormap[i])
        pos[0] += 2

    pos = [10, 120]
    colormap = make_colormap(256, [Color('red'), Color('blue'), Color('yellow')])
    for i in range(256):
        Rectangle(ctx).of_corner_size(pos, w, h).fill(colormap[i])
        pos[0] += 2

    pos = [10, 230]
    colormap = make_colormap(256, [Color('red'), Color('blue'), Color('yellow')], [3, 1])
    for i in range(256):
        Rectangle(ctx).of_corner_size(pos, w, h).fill(colormap[i])
        pos[0] += 2

    pos = [10, 340]
    colormap = make_colormap(256, [Color('red'), Color('blue'), Color('yellow'), Color('green')], [3, 0, 1])
    for i in range(256):
        Rectangle(ctx).of_corner_size(pos, w, h).fill(colormap[i])
        pos[0] += 2


make_image("colour-map.png", draw_map, 532, 450)