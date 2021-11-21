# Author:  Martin McBride
# Created: 2021-11-21
# Copyright (C) 2021, Martin McBride
# License: MIT

# Create some polygons and lines

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Square, Triangle, Polygon, Line

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(0.8))

    red = Color('red')
    green = Color('green')
    blue = Color('blue')
    thickness = 2

    Line(ctx).of_start_end((150, 150), (50, 50)).stroke(red, thickness)
    Line(ctx).of_start_end((300, 150), (200, 50)).as_ray().stroke(red, thickness)
    Line(ctx).of_start_end((450, 150), (350, 50)).as_line().stroke(red, thickness)

    Triangle(ctx).of_corners((50, 200), (150, 200), (125, 300)).stroke(green, thickness)
    Square(ctx).of_corner_size((200, 200), 100).stroke(green, thickness)
    Rectangle(ctx).of_corner_size((350, 200), 100, 75).stroke(green, thickness)

    Polygon(ctx).of_points([(50, 350), (250, 400), (250, 500), (50, 375)]).stroke(blue, thickness)
    Polygon(ctx).of_points([(300, 350), (500, 400), (500, 500), (300, 375)]).open().stroke(blue, thickness)

make_image("polygons-tutorial.png", draw, 550, 550)