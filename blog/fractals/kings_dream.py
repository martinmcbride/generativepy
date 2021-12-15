# Author:  Martin McBride
# Created: 2021-12-14
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.utils import temp_file
import math
import numpy as np

MAX_COUNT = 10000000
A = 2.879879
B = -0.765145
C = -0.966918
D = 0.744728


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=4, startx=-2, starty=-2)

    x = 2
    y = 2
    for i in range(MAX_COUNT):
        x, y = math.sin(A*x)+B*math.sin(A*y), math.sin(C*x)+D*math.sin(C*y)
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

save_nparray_image('kings-dream.png', frame)



