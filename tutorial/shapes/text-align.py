# Author:  Martin McBride
# Created: 2022-01-04
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Circle


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_width, background=Color(0.8))

    Text(ctx).of("Left", (50, 50)).font("Times").size(20).align_left().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (50, 70)).font("Times").size(20).align_left().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (50, 90)).font("Times").size(20).align_left().align_baseline().fill(Color('blue'))

    Text(ctx).of("Centre", (250, 50)).font("Times").size(20).align_center().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (250, 70)).font("Times").size(20).align_center().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (250, 90)).font("Times").size(20).align_center().align_baseline().fill(Color('blue'))

    Text(ctx).of("Right", (450, 50)).font("Times").size(20).align_right().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (450, 70)).font("Times").size(20).align_right().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (450, 90)).font("Times").size(20).align_right().align_baseline().fill(Color('blue'))

    Circle(ctx).of_center_radius((190, 200), 2).fill(Color(0, 0, 1))
    Text(ctx).of("gTop", (200, 200)).font("Times").size(20).align_left().align_top().fill(Color('black'))

    Circle(ctx).of_center_radius((190, 250), 2).fill(Color(0, 0, 1))
    Text(ctx).of("gMid", (200, 250)).font("Times").size(20).align_left().align_middle().fill(Color('black'))

    Circle(ctx).of_center_radius((190, 300), 2).fill(Color(0, 0, 1))
    Text(ctx).of("gBase", (200, 300)).font("Times").size(20).align_left().align_baseline().fill(Color('black'))

    Circle(ctx).of_center_radius((190, 350), 2).fill(Color(0, 0, 1))
    Text(ctx).of("gBottom", (200, 350)).font("Times").size(20).align_left().align_bottom().fill(Color('black'))


make_image("text-align.png", draw, 500, 400)