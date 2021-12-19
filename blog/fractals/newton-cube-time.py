# Author:  Martin McBride
# Created: 2021-12-18
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.utils import temp_file
from generativepy.analytics import print_stats, print_histogram
import numpy as np

MAX_COUNT = 100
BLACK = Color(0)
WHITE = Color(1)

ROOTS = [complex(-0.5, 0.866025),
         complex(-0.5, -0.866025),
         complex(1, 0)]

LIMIT = 0.01

def iterate(z):
    if z:
        return z - (z**3 - 1)/(3*z**2)
    else:
        return complex(0)

def converged(z):
    for i, r in enumerate(ROOTS, 1):
        if abs(z - r) < LIMIT:
            return i
    return 0

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, startx=-1.5, starty=-1.5)

    for px in range(pixel_width):
        for py in range(pixel_height):
            x, y = scaler.device_to_user(px, py)
            z = complex(x, y)
            image[py, px] = MAX_COUNT
            for i in range(MAX_COUNT):
                z = iterate(z)
                if converged(z) > 0:
                    image[py, px] = i
                    break


def colorise(counts):
    counts = np.reshape(counts, (counts.shape[0], counts.shape[1]))
    max_count = int(np.max(counts))
    colormap = make_npcolormap(max_count + 1,
                               [Color(0), Color('darkblue'), Color('yellow'), Color(1)],
                               [0.5, 2, 7])
    outarray = np.zeros((counts.shape[0], counts.shape[1], 3), dtype=np.uint8)
    apply_npcolormap(outarray, counts, colormap)
    return outarray


data = make_nparray_data(paint, 600, 600, channels=1)

filename = temp_file('newton-cube-time.dat')
save_nparray(filename, data)
data = load_nparray(filename)

frame = colorise(data)

save_nparray_image('newton-cube-time.png', frame)
