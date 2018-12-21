from generativepy import canvas
import math
import numpy as np


LINECOLOR = (0, 0, 0.5)
LINEWIDTH = 0.01
A = 1


def harm(t):
    x = math.cos(A*t)
    y = math.sin(A*t)
    return x, y


def draw(ctx, **extras):
    ctx.move_to(*harm(0))
    for t in np.arange(0, 100, 0.01):
        ctx.line_to(*harm(t))
    ctx.set_source_rgb(*LINECOLOR)
    ctx.set_line_width(LINEWIDTH)
    ctx.stroke()


canvas.make_vector_png("/tmp/harmonograph.png", draw, pixel_size=(1000, 1000), width=3,
                       startx=-1.5, starty=-1.5, color=(1, 1, 1))
