# Author:  Martin McBride
# Created: 2021-11-07
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create a simple linear gradient with several circle shapes

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Circle, LinearGradient

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.4))

    gradient = LinearGradient().of_points((150, 150), (350, 250)).with_start_end(Color('yellow'), Color('red')).build()
    Circle(ctx).of_center_radius((100, 100), 75).fill(gradient)
    Circle(ctx).of_center_radius((270, 100), 75).fill(gradient)
    Circle(ctx).of_center_radius((150, 300), 75).fill(gradient)
    Circle(ctx).of_center_radius((400, 300), 75).fill(gradient)

make_image("circles-linear-gradient.png", draw, 500, 400)