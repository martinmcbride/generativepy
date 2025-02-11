# Author:  Martin McBride
# Created: 2022-01-10
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Circle, Square, Text, Transform

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, background=Color(0.8))

    # Create a circular clip region and draw some squares in it
    with Transform(ctx):
        Circle(ctx).of_center_radius((190, 190), 100).clip()
        Square(ctx).of_corner_size((100, 100), 80).fill(Color('red'))
        Square(ctx).of_corner_size((100, 200), 80).fill(Color('green'))
        Square(ctx).of_corner_size((200, 100), 80).fill(Color('blue'))
        Square(ctx).of_corner_size((200, 200), 80).fill(Color('black'))

    with Transform(ctx):
        Text(ctx).of("ABC", (150, 350)).font("Times").size(150).align_left().align_top().clip()
        circles = [(200, 380, 'orange'), (200, 450, 'cyan'), (300, 380, 'green'),
                   (300, 450, 'purple'), (400, 380, 'yellow'), (400, 450, 'blue')]
        for x, y, color in circles:
            Circle(ctx).of_center_radius((x, y), 70).fill(Color(color))


make_image("clip-tutorial.png", draw, 500, 500)
