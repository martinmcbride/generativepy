# Author:  Martin McBride
# Created: 2021-11-07
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create a simple linear gradient across the whole page

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, LinearGradient, Circle, Line

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.4))

    gradient = LinearGradient().of_points((150, 150), (350, 250)).with_start_end(Color('yellow'), Color('red')).build()
    Rectangle(ctx).of_corner_size((0, 0), 500, 400).fill(gradient)

    Line(ctx).of_start_end((150, 150), (350, 250)).stroke(Color(0), 2, [5, 5])
    Line(ctx).of_start_end((150, 150), (250, -50)).as_line().stroke(Color(0), 2, [5, 5])
    Line(ctx).of_start_end((350, 250), (450, 50)).as_line().stroke(Color(0), 2, [5, 5])
    Circle(ctx).of_center_radius((150, 150), 5).fill(Color(0))
    Circle(ctx).of_center_radius((350, 250), 5).fill(Color(0))

make_image("fullpage-linear-gradient.png", draw, 500, 400)