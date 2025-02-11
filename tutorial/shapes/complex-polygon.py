# Author:  Martin McBride
# Created: 2022-01-05
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup, EVEN_ODD
from generativepy.color import Color
from generativepy.geometry import Polygon
import math

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    black = Color(0)
    red = Color('red')

    Polygon(ctx).of_points([(150, 50),
                            (100, 250),
                            (250, 150),
                            (50, 150),
                            (200, 250),
                            ]).fill(red).stroke(black, 5)


    Polygon(ctx).of_points([(450, 50),
                            (400, 250),
                            (550, 150),
                            (350, 150),
                            (500, 250),
                            ]).fill(red, fill_rule=EVEN_ODD).stroke(black, 5)

make_image("complex-polygon.png", draw, 700, 300)