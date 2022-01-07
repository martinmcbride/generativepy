# Author:  Martin McBride
# Created: 2022-01-07
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Image


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    Image(ctx).of_file_position('cat.png', (50, 50)).paint()
    Image(ctx).of_file_position('cat.png', (300, 50)).scale(0.5).paint()
    Image(ctx).of_file_position('cat.png', (50, 300)).scale(1.5).paint()


make_image("image.png", draw, 500, 600)