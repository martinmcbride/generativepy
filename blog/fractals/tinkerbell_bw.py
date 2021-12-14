# Author:  Martin McBride
# Created: 2021-12-13
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray

MAX_COUNT = 100000
A = 0.9
B = -0.6013
C = 2.0
D = 0.5


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, startx=-2, starty=-2)

    x = 0.01
    y = 0.01
    for i in range(MAX_COUNT):
        x, y = x*x - y*y + A*x + B*y, 2*x*y + C*x + D*y
        px, py = scaler.user_to_device(x, y)
        image[py, px] = 0

make_nparray('tinkerbell-bw.png', paint, 600, 600, channels=1)

