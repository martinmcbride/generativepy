# Author:  Martin McBride
# Created: 2021-12-16
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray

MAX_COUNT = 100000
A = 1.4
B = 0.3


# Show teh full Henon attractor
def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, startx=-1.5, starty=-1.5)

    x = 0.01
    y = 0.01
    for i in range(MAX_COUNT):
        x, y = 1 - A*x*x + y, B*x
        px, py = scaler.user_to_device(x, y)
        if 0 <= px < pixel_width and 0 <= py < pixel_height:
            image[py, px] = 0

make_nparray('henon.png', paint, 600, 600, channels=1)


# Zoom in on the right hand loop
def paint2(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=.5, startx=0.8, starty=-0.25)

    x = 0.01
    y = 0.01
    for i in range(MAX_COUNT):
        x, y = 1 - A*x*x + y, B*x
        px, py = scaler.user_to_device(x, y)
        if 0 <= px < pixel_width and 0 <= py < pixel_height:
            image[py, px] = 0

make_nparray('henon2.png', paint2, 600, 600, channels=1)

