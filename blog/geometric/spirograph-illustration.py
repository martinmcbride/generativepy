# Author:  Martin McBride
# Created: 2022-01-22
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.color import Color
from generativepy.drawing import make_image, setup, make_image_frames
import math

from generativepy.geometry import Polygon, Text, Circle, Line
from generativepy.gif import save_animated_gif


def create_spiro(a, b, d, dt=0.01, extent=None):
    if not extent:
        extent = 2*math.pi*b/math.gcd(a, b)
    t = 0
    pts = []
    while t < extent:
        t += dt
        x = (a - b) * math.cos(t) + d * math.cos((a - b)/b * t)
        y = (a - b) * math.sin(t) - d * math.sin((a - b)/b * t)
        pts.append((x, y))
    return pts


# Create an illustration of the first few points of the curve.
def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 14
    b = 6
    d = 4
    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('skyblue'), line_width=0.1)
    points = create_spiro(a, b, d, 0.5, 4)
    Polygon(ctx).of_points(points).open().stroke(Color('red'), 0.1)
    for p in points:
        Circle(ctx).of_center_radius(p, 0.2).fill(Color(0))

make_image("spirograph-points.png", draw, 600, 600)

# Create an illustration of the dimensions A, B, D.
def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 14
    b = 6
    d = 4
    angle = 1

    Origin = (0, 0)
    A = (-a, 0)
    B = ((a-b)*math.cos(angle), (a-b)*math.sin(angle))
    x = (a - b) * math.cos(angle) + d * math.cos((a - b) / b * angle)
    y = (a - b) * math.sin(angle) - d * math.sin((a - b) / b * angle)
    D = (x, y)

    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('skyblue'), line_width=0.1)
    Polygon(ctx).of_points(create_spiro(a, b, d, 0.01, angle)).open().stroke(Color('red'), line_width=0.1)

    Circle(ctx).of_center_radius(Origin, a).stroke(Color('darkgreen'), line_width=0.1)
    Circle(ctx).of_center_radius(Origin, 0.3).fill(Color('darkgreen'))
    Line(ctx).of_start_end(Origin, A).stroke(Color('darkgreen'), line_width=0.1)
    Text(ctx).of('a', (A[0]/2, A[1])).size(1.5).offset(0, -0.5).fill(Color('darkgreen'))
    Circle(ctx).of_center_radius(B, b).stroke(Color('blue'), line_width=0.1)
    Circle(ctx).of_center_radius(B, 0.3).fill(Color('blue'))
    Text(ctx).of('b', (B[0], B[1]+b/2)).size(1.5).offset(0.5, 0).fill(Color('blue'))
    Line(ctx).of_start_end(B, (B[0], B[1]+b)).stroke(Color('blue'), line_width=0.1)
    Circle(ctx).of_center_radius(D, 0.3).fill(Color('black'))
    Line(ctx).of_start_end(B, D).stroke(Color('black'), line_width=0.1)
    Text(ctx).of('d', ((B[0]+D[0])/2, (B[1]+D[1])/2)).size(1.5).offset(0.5, 0.5).fill(Color('black'))


make_image("spirograph-dimensions.png", draw2, 600, 600)

# Create an animation of the curve being drawn.
def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 14
    b = 6
    d = 4
    angle = (frame_no/frame_count)*2*math.pi*b/math.gcd(a, b)
    print(angle)

    Origin = (0, 0)
    A = (-a, 0)
    B = ((a-b)*math.cos(angle), (a-b)*math.sin(angle))
    x = (a - b) * math.cos(angle) + d * math.cos((a - b) / b * angle)
    y = (a - b) * math.sin(angle) - d * math.sin((a - b) / b * angle)
    D = (x, y)

    Polygon(ctx).of_points(create_spiro(a, b, d)).stroke(Color('skyblue'), line_width=0.2)
    Polygon(ctx).of_points(create_spiro(a, b, d, 0.01, angle)).open().stroke(Color('red'), line_width=0.2)

    Circle(ctx).of_center_radius(Origin, a).stroke(Color('darkgreen'), line_width=0.2)
    Circle(ctx).of_center_radius(B, b).stroke(Color('blue'), line_width=0.2)
    Circle(ctx).of_center_radius(B, 0.3).fill(Color('blue'))
    Circle(ctx).of_center_radius(D, 0.3).fill(Color('black'))
    Line(ctx).of_start_end(B, D).stroke(Color('black'), line_width=0.2)


frames = make_image_frames(draw3, 400, 400, 100)
save_animated_gif("spirograph-animation.gif", frames, 0.1)

