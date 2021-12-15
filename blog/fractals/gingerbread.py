# Author:  Martin McBride
# Created: 2021-12-13
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray

MAX_COUNT = 1000000


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=12, startx=-3.5, starty=-3.5)

    x = -0.1
    y = 0.0
    for i in range(MAX_COUNT):
        x, y = 1 - y + abs(x), x
        px, py = scaler.user_to_device(x, y)
        image[py, px] = 0

make_nparray('gingerbread.png', paint, 600, 600, channels=1)

