# Author:  Martin McBride
# Created: 2021-11-29
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create some ellipses, arcs etc

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Ellipse

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    blue = Color('blue')
    grey = Color(0.4)
    thickness = 2

    Ellipse(ctx).of_center_radius((100, 100), 75, 50).stroke(blue, thickness)

    Ellipse(ctx).of_center_radius((300, 100), 75, 50).stroke(grey, thickness, dash=[5])
    Ellipse(ctx).of_center_radius((300, 100), 75, 50).as_arc(0, 1).stroke(blue, thickness)

    Ellipse(ctx).of_center_radius((100, 300), 50, 75).stroke(grey, thickness, dash=[5])
    Ellipse(ctx).of_center_radius((100, 300), 50, 75).as_sector(1, 3).stroke(blue, thickness)

    Ellipse(ctx).of_center_radius((300, 300), 50, 75).stroke(grey, thickness, dash=[5])
    Ellipse(ctx).of_center_radius((300, 300), 50, 75).as_segment(-1, 1).stroke(blue, thickness)


make_image("ellipses-tutorial.png", draw, 400, 400)