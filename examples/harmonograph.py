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


def draw(canvas):
    points = [harm(t) for t in np.arange(0, 100, 0.01)]
    canvas.stroke(LINECOLOR)
    canvas.strokeWeight(LINEWIDTH)
    canvas.polygon(points, False)


canvas.makeImage("/tmp/harmonograph.png", draw, pixelSize=(1000, 1000), width=3,
                       startX=-1.5, startY=-1.5, color=(1, 1, 1))
