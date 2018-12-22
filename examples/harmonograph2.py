from generativepy import canvas
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


def draw(canvas):
    points = [harm(t) for t in np.arange(0, 100, 0.01)]
    canvas.stroke(LINECOLOR)
    canvas.strokeWeight(LINEWIDTH)
    canvas.polygon(points, False)

canvas.makeImage("/tmp/harmonograph.2png", draw, pixelSize=(1000, 1000), width=4.2,
                       startX=-2.1, startY=-2.1, color=(1, 1, 1))

