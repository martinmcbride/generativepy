# Author:  Martin McBride
# Created: 2021-12-13
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.analytics import print_stats, print_histogram
import numpy as np

MAX_COUNT = 256
C1 = -0.79
C2 = 0.15

def calc(x, y):
    for i in range(MAX_COUNT):
        x, y = x*x - y*y + C1, 2*x*y + C2
        if x*x + y*y > 4:
            return i+1
    return 0


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3.2, startx=-1.6, starty=-1.2)

    for px in range(pixel_width):
        for py in range(pixel_height):
            x, y = scaler.device_to_user(px, py)
            count = calc(x, y)
            image[py, px] = count


def colorise(counts):
    counts = np.reshape(counts, (counts.shape[0], counts.shape[1]))

    colormap = make_npcolormap(MAX_COUNT+1,
                               [Color('black'), Color('darkblue'), Color('green'), Color('cyan'), Color('yellow'), Color('black')],
                               [16, 16, 32, 32, 128])

    outarray = np.zeros((counts.shape[0], counts.shape[1], 3), dtype=np.uint8)
    apply_npcolormap(outarray, counts, colormap)
    return outarray


data = make_nparray_data(paint, 800, 600, channels=1)

frame = colorise(data)

save_nparray_image('julia.png', frame)
