from generativepy import vector_image
import math
import numpy as np


LINECOLOR = (0, 0, 0.5)
LINEWIDTH = 0.01
A = 5
B = 15.2
P = 30
Q = 30


def harm(t):
    x = math.cos(A*t)*math.exp(-t/P) + math.cos(B*t)*math.exp(-t/Q)
    y = math.sin(A*t)*math.exp(-t/P)
    return x, y


def draw(ctx, **extras):
    ctx.move_to(*harm(0))
    for t in np.arange(0, 100, 0.01):
        ctx.line_to(*harm(t))
    ctx.set_source_rgb(*LINECOLOR)
    ctx.set_line_width(LINEWIDTH)
    ctx.stroke()


vector_image.make_vector_png("/tmp/harmonograph3.png", draw, pixel_size=(1000, 1000), width=4.2,
                             startx=-2.1, starty=-2.1, color=(1, 1, 1))
