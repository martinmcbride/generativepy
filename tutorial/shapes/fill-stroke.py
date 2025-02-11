# Author:  Martin McBride
# Created: 2021-12-11
# Copyright (C) 2021, Martin McBride
# License: MIT

# Demonstrate fill and stroke

from generativepy.drawing import make_image, setup, SQUARE, BUTT, ROUND, BEVEL, MITER, EVEN_ODD, WINDING
from generativepy.color import Color
from generativepy.geometry import Rectangle, Line, Triangle

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    Rectangle(ctx).of_corner_size((50, 50), 100, 300)\
                  .fill(Color('magenta'))

    Rectangle(ctx).of_corner_size((200, 50), 100, 300)\
                  .stroke(Color('blue'), 10)

    Rectangle(ctx).of_corner_size((350, 50), 100, 300)\
                  .stroke(Color('black'), 20)\
                  .fill(Color('yellow'))

    Rectangle(ctx).of_corner_size((500, 50), 100, 300)\
                  .fill(Color('yellow'))\
                  .stroke(Color('black'), 20)


make_image("fill-stroke-tutorial.png", draw, 650, 400)


def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    black = Color(0)

    Line(ctx).of_start_end((50, 50), (450, 50)).stroke(black, 20, cap=SQUARE)
    Line(ctx).of_start_end((50, 100), (450, 100)).stroke(black, 20, cap=BUTT)
    Line(ctx).of_start_end((50, 150), (450, 150)).stroke(black, 20, cap=ROUND)

    Line(ctx).of_start_end((50, 250), (450, 250)).stroke(black, 20, cap=SQUARE, dash=[30])
    Line(ctx).of_start_end((50, 300), (450, 300)).stroke(black, 20, cap=BUTT, dash=[30])
    Line(ctx).of_start_end((50, 350), (450, 350)).stroke(black, 20, cap=ROUND, dash=[30])

    Line(ctx).of_start_end((50, 450), (450, 450)).stroke(black, 20, cap=BUTT, dash=[30, 40])
    Line(ctx).of_start_end((50, 500), (450, 500)).stroke(black, 20, cap=BUTT, dash=[30, 10, 20, 10])



make_image("stroke-style-tutorial.png", draw2, 500, 550)


def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    black = Color(0)

    Triangle(ctx).of_corners((50, 50), (200, 100), (100, 200)).stroke(black, 20, join=MITER)
    Triangle(ctx).of_corners((250, 50), (400, 100), (300, 200)).stroke(black, 20, join=ROUND)
    Triangle(ctx).of_corners((450, 50), (600, 100), (500, 200)).stroke(black, 20, join=BEVEL)


make_image("join-style-tutorial.png", draw3, 650, 250)

def draw4(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    black = Color(0)
    orange = Color('orange')

    Triangle(ctx).of_corners((50, 50), (200, 100), (100, 200)).add()
    Triangle(ctx).of_corners((75, 75), (150, 125), (125, 150)).as_sub_path()\
                 .fill(orange, fill_rule=EVEN_ODD).stroke(black, 2)
    Triangle(ctx).of_corners((250, 50), (400, 100), (300, 200)).add()
    Triangle(ctx).of_corners((275, 75), (325, 150), (350, 125)).as_sub_path()\
                 .fill(orange, fill_rule=EVEN_ODD).stroke(black, 2)

    Triangle(ctx).of_corners((50, 250), (200, 300), (100, 400)).add()
    Triangle(ctx).of_corners((75, 275), (150, 325), (125, 350)).as_sub_path()\
                 .fill(orange, fill_rule=WINDING).stroke(black, 2)
    Triangle(ctx).of_corners((250, 250), (400, 300), (300, 400)).add()
    Triangle(ctx).of_corners((275, 275), (325, 350), (350, 325)).as_sub_path()\
                 .fill(orange, fill_rule=WINDING).stroke(black, 2)


make_image("fill-style-tutorial.png", draw4, 450, 450)

