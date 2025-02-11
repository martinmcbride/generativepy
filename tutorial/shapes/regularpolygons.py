# Author:  Martin McBride
# Created: 2022-06-05
# Copyright (C) 2022, Martin McBride
# License: MIT

# Create some polygons and lines

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import RegularPolygon, Circle
import math

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    red = Color('crimson')
    green = Color('darkgreen')
    blue = Color('dodgerblue')

    RegularPolygon(ctx).of_centre_sides_radius((150, 150), 5, 100)\
                       .fill(blue)\
                       .stroke(green, 5)

    RegularPolygon(ctx).of_centre_sides_radius((400, 150), 6, 100)\
                       .fill(blue)\
                       .stroke(green, 5)

    RegularPolygon(ctx).of_centre_sides_radius((650, 150), 6, 100, math.pi/12)\
                       .fill(blue)\
                       .stroke(green, 5)

    p = RegularPolygon(ctx).of_centre_sides_radius((150, 400), 5, 100)\
                       .fill(blue)\
                       .stroke(green, 5)
    Circle(ctx).of_center_radius((150, 400), p.inner_radius).stroke(red, 5)

    p = RegularPolygon(ctx).of_centre_sides_radius((400, 400), 5, 100)\
                       .fill(blue)\
                       .stroke(green, 5)
    Circle(ctx).of_center_radius((400, 400), p.outer_radius).stroke(red, 5)

    p = RegularPolygon(ctx).of_centre_sides_radius((650, 400), 5, 100)\
                       .fill(blue)\
                       .stroke(green, 5)
    for v in p.vertices:
        Circle(ctx).of_center_radius(v, 10).fill(red)



make_image("regularpolygons-tutorial.png", draw, 800, 550)