# Author:  Martin McBride
# Created: 2022-01-22
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.color import Color
from generativepy.drawing import make_image, setup, EVEN_ODD
import math

from generativepy.geometry import Polygon, Circle, Transform


def sinsq(x):
    q = 2*x/math.pi
    q, r = int(q)%4, q - int(q)
    if q==0:
        return r
    elif q == 1:
        return 1 - r
    elif q==2:
        return -r
    else:
        return -1 + r

def cossq(x):
    q = 2*x/math.pi
    q, r = int(q)%4, q - int(q)
    if q==3:
        return r
    elif q == 0:
        return 1 - r
    elif q==1:
        return -r
    else:
        return -1 + r

def sintri(x):
    q = 3*x/(2*math.pi)
    q, r = int(q)%3, q - int(q)
    n = math.sqrt(3)/2
    if q==0:
        return r*n
    elif q == 1:
        return n*(1 - 2*r)
    else:
        return -(1-r)*n

def costri(x):
    q = 3*x/(2*math.pi)
    q, r = int(q)%3, q - int(q)
    n = math.sqrt(3)/2
    if q==0:
        return 1 - (1+n)*r
    elif q == 1:
        return -n
    else:
        return -n + (1+n)*r

def create_spiro_square(a, b, d):
    dt = 0.01
    t = 0
    pts = []
    while t < 2*math.pi*b/math.gcd(a, b):
        t += dt
        x = (a - b) * cossq(t) + d * cossq((a - b)/b * t)
        y = (a - b) * sinsq(t) - d * sinsq((a - b)/b * t)
        pts.append((x, y))
    return pts

def create_spiro_triangle(a, b, d):
    dt = 0.01
    t = 0
    pts = []
    while t < 2*math.pi*b/math.gcd(a, b):
        t += dt
        x = (a - b) * costri(t) + d * costri((a - b)/b * t)
        y = (a - b) * sintri(t) - d * sintri((a - b)/b * t)
        pts.append((x, y))
    return pts


def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 16
    b = 9
    d = 6
    Polygon(ctx).of_points(create_spiro_square(a, b, d)).fill(Color('gold'), fill_rule=EVEN_ODD).stroke(Color('darkblue'), line_width=0.1)


make_image("spirograph-square.png", draw, 600, 600)

def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    a = 16
    b = 9
    d = 6
    Polygon(ctx).of_points(create_spiro_square(a, b, d)).fill(Color('lime'), fill_rule=EVEN_ODD) #.stroke(Color('darkblue'), line_width=0.1)

    a = 17
    b = 11
    d = 10
    Polygon(ctx).of_points(create_spiro_square(a, b, d)).fill(Color('darkgreen', 0.4), fill_rule=EVEN_ODD) #.stroke(Color('ligh'), line_width=0.1)


make_image("spirograph-square2.png", draw2, 600, 600)

def draw3(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    # x = [i/100 for i in range(1000)]
    # y = [-sintri(i) for i in x]
    # Polygon(ctx).of_points(zip(x, y)).open().stroke(Color('black'), line_width=0.1)
    #
    # x = [i/100 for i in range(1000)]
    # y = [-costri(i) + 2 for i in x]
    # Polygon(ctx).of_points(zip(x, y)).open().stroke(Color('black'), line_width=0.1)
    #
    # x = [i/100 for i in range(1000)]
    # y = [-int(3*i/(2*math.pi)) - 2 for i in x]
    # Polygon(ctx).of_points(zip(x, y)).open().stroke(Color('black'), line_width=0.1)

    a = 16
    b = 10
    d = 7
    Polygon(ctx).of_points(create_spiro_triangle(a, b, d)).fill(Color('gold'), fill_rule=EVEN_ODD).stroke(Color('darkblue'), line_width=0.1)


make_image("spirograph-triangle.png", draw3, 600, 600)

def draw4(ctx, pixel_width, pixel_height, frame_no, frame_count):

    width = 32
    setup(ctx, pixel_width, pixel_height, width=width, startx=-width/2, starty=-width/2, background=Color(1))

    colors = [Color('magenta', 0.7),
              Color('red', 0.7),
              Color('blue', 0.7),
              Color('gold', 0.7),
              ]

    for i, color in enumerate(colors):
        a = 16
        b = 10
        d = 7
        with Transform(ctx).rotate(i*math.pi/6):
            Polygon(ctx).of_points(create_spiro_triangle(a, b, d)).fill(color, fill_rule=EVEN_ODD)


make_image("spirograph-triangle2.png", draw4, 600, 600)

