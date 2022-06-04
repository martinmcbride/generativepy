# Author:  Martin McBride
# Created: 2022-06-04
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color, ArtisticColorScheme
from generativepy.geometry import Square

# Select a colour scheme
cs = ArtisticColorScheme()

def draw_color_scheme(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color("white"))

    # Fill a square with red
    Square(ctx).of_corner_size((50, 50), 200).fill(cs.RED)

    # Fill a square with a lighter version of RED, stroke with a darker version
    Square(ctx).of_corner_size((300, 50), 200).fill(cs.RED.light1).stroke(cs.RED.dark1, 10)


make_image("colour-scheme.png", draw_color_scheme, 600, 300)
