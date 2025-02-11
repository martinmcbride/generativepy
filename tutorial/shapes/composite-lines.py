# Author:  Martin McBride
# Created: 2022-01-05
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Line

def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    black = Color(0)

    Line(ctx).of_start_end((100, 50), (200, 50)).stroke(black, 20)
    Line(ctx).of_start_end((200, 50), (100, 200)).stroke(black, 20)
    Line(ctx).of_start_end((100, 200), (50, 200)).stroke(black, 20)
    Line(ctx).of_start_end((50, 200), (100, 50)).stroke(black, 20)

    Line(ctx).of_start_end((300, 50), (400, 50)).add()
    Line(ctx).of_end((300, 200)).extend_path().add()
    Line(ctx).of_end((250, 200)).extend_path().stroke(black, 20)

    Line(ctx).of_start_end((500, 50), (600, 50)).add()
    Line(ctx).of_end((500, 200)).extend_path().add()
    Line(ctx).of_end((450, 200)).extend_path(close=True).stroke(black, 20)

make_image("composite-lines.png", draw2, 700, 300)