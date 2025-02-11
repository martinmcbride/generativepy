# Author:  Martin McBride
# Created: 2021-12-15
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.utils import temp_file
from generativepy.analytics import print_stats, print_histogram
import numpy as np
import math

MAX_COUNT = 10000000
A = 0.1
B = 5
C = -1

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return(0)

def colorise(counts):
    counts = np.reshape(counts, (counts.shape[0], counts.shape[1]))
    power_counts = np.power(counts, 0.25)
    maxcount = np.max(power_counts)
    normalised_counts = (power_counts * 1023 / max(maxcount, 1)).astype(np.uint32)

    colormap = make_npcolormap(1024, [Color('black'), Color('green'), Color('yellow'), Color('red')])

    outarray = np.zeros((counts.shape[0], counts.shape[1], 3), dtype=np.uint8)
    apply_npcolormap(outarray, normalised_counts, colormap)
    return outarray

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=300, startx=-150, starty=-150)

    x = -1
    y = 0
    for i in range(MAX_COUNT):
        x, y = y-math.sqrt(abs(B*x-C))*sign(x), A-x
        px, py = scaler.user_to_device(x, y)
        if 0 <= px < pixel_width and 0 <= py < pixel_height:
            image[py, px] += 1


filename = temp_file('hopalong-variant.dat')

data = make_nparray_data(paint, 600, 600, channels=1)
save_nparray(filename, data)
data = load_nparray(filename)

frame = colorise(data)

save_nparray_image('hopalong-variant.png', frame)
