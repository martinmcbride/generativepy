# Author:  Martin McBride
# Created: 2022-01-05
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Circle
import math

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    black = Color(0)

    Circle(ctx).of_center_radius((50, 50), 10).as_arc(math.pi, math.pi*3/2).add()
    Circle(ctx).of_center_radius((250, 50), 10).as_arc(math.pi*3/2, 0).extend_path().add()
    Circle(ctx).of_center_radius((250, 150), 10).as_arc(0, math.pi/2).extend_path().add()
    Circle(ctx).of_center_radius((50, 150), 10).as_arc(math.pi/2, math.pi).extend_path(close=True).stroke(black, 5)


    Circle(ctx).of_center_radius((350, 50), 30).as_arc(math.pi/2, math.pi*3/2).add()
    Circle(ctx).of_center_radius((550, 50), 30).as_arc(math.pi*3/2, math.pi/2).extend_path(close=True).stroke(black, 5)

make_image("complex-roundrect.png", draw, 700, 300)