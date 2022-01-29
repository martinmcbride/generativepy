# Author:  Martin McBride
# Created: 2022-09-29
# Copyright (C) 2022, Martin McBride
# License: MIT

# Demonstrate markers

from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Line, Polygon, AngleMarker, Text, TickMarker, ParallelMarker


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, width=10, background=Color(0.8))

    a = (1, 2)
    b = (7, 2)
    c = (3, 8)
    d = (9, 8)
    e = (5, 2)
    f = (5, 8)

    Polygon(ctx).of_points([a, b, d, c]).stroke(Color('blue'), line_width=.05)
    Line(ctx).of_start_end(e, f).stroke(Color('blue'), line_width=.05)

    AngleMarker(ctx).of_points(b, a, c).with_radius(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    AngleMarker(ctx).of_points(a, b, d).with_radius(.5).stroke(Color('blue'), line_width=.05)
    AngleMarker(ctx).of_points(c, d, b).with_radius(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    AngleMarker(ctx).of_points(a, c, d).with_radius(.5).stroke(Color('blue'), line_width=.05)
    AngleMarker(ctx).of_points(e, f, d).with_radius(.5).as_right_angle().stroke(Color('blue'), line_width=.05)

    Text(ctx).of('a', a).size(1).offset_towards(d, -0.5).fill(Color('red'))
    Text(ctx).of('b', b).size(1).offset_towards(c, -0.9).fill(Color('red'))
    Text(ctx).of('c', c).size(1).offset_towards(b, -0.9).fill(Color('red'))
    Text(ctx).of('d', d).size(1).offset_towards(a, -0.5).fill(Color('red'))
    Text(ctx).of('e', e).size(1).offset_towards(f, -0.3).fill(Color('red'))
    Text(ctx).of('f', f).size(1).offset_towards(e, -0.9).fill(Color('red'))

make_image("angle-markers.png", draw, 600, 600)


def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, width=10, background=Color(0.8))

    a = (1, 2)
    b = (7, 2)
    c = (3, 8)
    d = (9, 8)
    e = (5, 2)
    f = (5, 8)

    Polygon(ctx).of_points([a, b, d, c]).stroke(Color('blue'), line_width=.05)

    TickMarker(ctx).of_start_end(a, b).with_length(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    TickMarker(ctx).of_start_end(c, d).with_length(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    TickMarker(ctx).of_start_end(a, c).with_length(.5).stroke(Color('blue'), line_width=.05)
    TickMarker(ctx).of_start_end(b, d).with_length(.5).stroke(Color('blue'), line_width=.05)

    Text(ctx).of('a', a).size(1).offset_towards(d, -0.5).fill(Color('red'))
    Text(ctx).of('b', b).size(1).offset_towards(c, -0.5).fill(Color('red'))
    Text(ctx).of('c', c).size(1).offset_towards(b, -0.9).fill(Color('red'))
    Text(ctx).of('d', d).size(1).offset_towards(a, -0.5).fill(Color('red'))

make_image("tick-markers.png", draw2, 600, 600)

def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, width=10, background=Color(0.8))

    a = (1, 2)
    b = (7, 2)
    c = (3, 8)
    d = (9, 8)
    e = (5, 2)
    f = (5, 8)

    Polygon(ctx).of_points([a, b, d, c]).stroke(Color('blue'), line_width=.05)

    ParallelMarker(ctx).of_start_end(a, b).with_length(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    ParallelMarker(ctx).of_start_end(c, d).with_length(.5).with_count(2).with_gap(0.15).stroke(Color('blue'), line_width=.05)
    ParallelMarker(ctx).of_start_end(a, c).with_length(.5).stroke(Color('blue'), line_width=.05)
    ParallelMarker(ctx).of_start_end(b, d).with_length(.5).stroke(Color('blue'), line_width=.05)

    Text(ctx).of('a', a).size(1).offset_towards(d, -0.5).fill(Color('red'))
    Text(ctx).of('b', b).size(1).offset_towards(c, -0.5).fill(Color('red'))
    Text(ctx).of('c', c).size(1).offset_towards(b, -0.9).fill(Color('red'))
    Text(ctx).of('d', d).size(1).offset_towards(a, -0.5).fill(Color('red'))

make_image("parallel-markers.png", draw3, 600, 600)

