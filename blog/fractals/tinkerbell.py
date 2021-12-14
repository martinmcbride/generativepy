# Author:  Martin McBride
# Created: 2021-12-13
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.utils import temp_file
from generativepy.analytics import print_stats, print_histogram
import numpy as np

MAX_COUNT = 10000000
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
        image[py, px] += 1


def colorise(counts):
    counts = np.reshape(counts, (counts.shape[0], counts.shape[1]))
    power_counts = np.power(counts, 0.25)
    maxcount = np.max(power_counts)
    normalised_counts = (power_counts * 1023 / max(maxcount, 1)).astype(np.uint32)

    colormap = make_npcolormap(1024, [Color('black'), Color('red'), Color('orange'), Color('yellow'), Color('white')])

    outarray = np.zeros((counts.shape[0], counts.shape[1], 3), dtype=np.uint8)
    apply_npcolormap(outarray, normalised_counts, colormap)
    return outarray


data = make_nparray_data(paint, 600, 600, channels=1)

filename = temp_file('tinkerbell.dat')
save_nparray(filename, data)
data = load_nparray(filename)

frame = colorise(data)

save_nparray_image('tinkerbell.png', frame)
