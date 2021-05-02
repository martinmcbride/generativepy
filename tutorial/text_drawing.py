# Author:  Martin McBride
# Created: 2021-05-02
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text


def draw_alpha(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(1))

    Text(ctx).of("Filled Times", (100, 100)).font("Times").size(40).fill(Color('blue'))
    Text(ctx).of("Filled Arial", (100, 150)).font("Arial").size(40).fill(Color('red'))
    Text(ctx).of("Small", (100, 180)).font("Arial").size(20).fill(Color('darkgreen'))
    Text(ctx).of("Large", (100, 240)).font("Arial").size(60).fill(Color('magenta'))
    Text(ctx).of("Stroke", (100, 310)).font("Arial").size(60).stroke(Color('black'), 4)
    Text(ctx).of("Fill Stroke", (100, 380)).font("Arial").size(60)\
                                           .fill(Color('blue')).stroke(Color('red'), 2)
    Text(ctx).of("Dashed", (100, 450)).font("Arial").size(60).stroke(Color('black'), 3, dash=[4])


make_image("text-drawing.png", draw_alpha, 500, 500)