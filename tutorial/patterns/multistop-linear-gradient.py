# Author:  Martin McBride
# Created: 2021-11-07
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create a simple linear gradient

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, LinearGradient

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.4))

    gradient = LinearGradient().of_points((150, 150), (350, 250))\
                               .with_stops([(0, Color('yellow')),
                                            (0.5, Color('blue')),
                                            (1, Color('red'))])\
                               .build()
    Rectangle(ctx).of_corner_size((150, 150), 200, 100).fill(gradient)

make_image("multistop-linear-gradient.png", draw, 500, 400)