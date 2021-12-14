# Author:  Martin McBride
# Created: 2021-12-13
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray

MAX_COUNT = 256

def calc(c1, c2):
    x = y = 0
    for i in range(MAX_COUNT):
        x, y = x*x - y*y + c1, 2*x*y + c2
        if x*x + y*y > 4:
            return i+1
    return 0


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, startx=-2, starty=-1.5)

    for px in range(pixel_width):
        for py in range(pixel_height):
            x, y = scaler.device_to_user(px, py)
            count = calc(x, y)
            if count==0:
                image[py, px] = 0

make_nparray('mandelbrot-bw.png', paint, 600, 600, channels=1)