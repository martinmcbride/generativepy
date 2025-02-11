# Author:  Martin McBride
# Created: 2022-01-19
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.bitmap import Scaler
from generativepy.nparray import make_nparray_data, save_nparray, load_nparray, make_npcolormap, apply_npcolormap, save_nparray_image
from generativepy.color import Color
from generativepy.analytics import print_stats, print_histogram
from generativepy.utils import temp_file
import math
import numpy as np

MAX_COUNT = 1000
H1 = 0.4
H2 = 0.7
WIDTH = 600
USERWIDTH = 4

def calc(x, y):
    xn = x - H1*math.sin(y + math.tan(3*y))
    yn = y - H1*math.sin(x + math.tan(3*x))
    return xn, yn


def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=USERWIDTH, startx=-USERWIDTH/2, starty=-USERWIDTH/2)

    image[...] = 0

    for i in range(0, WIDTH, 1):
        print(i)
        for j in range(0, WIDTH, 1):
            x, y = scaler.device_to_user(i, j)
            for _ in range(MAX_COUNT):
                x, y = calc(x, y)
                px, py = scaler.user_to_device(x, y)
                if 0 <= px < WIDTH and 0 <= py < WIDTH:
                    image[py, px] += 1

def colorise(counts):
    counts = np.reshape(counts, (counts.shape[0], counts.shape[1]))

    colormap = make_npcolormap(int(np.max(counts))+1,
                               [Color('firebrick'), Color('goldenrod'), Color('lime'), Color('green'),
                                Color('darkgreen'), Color('white')],
                               [5, 5, 5, 10, 10240])

    outarray = np.zeros((counts.shape[0], counts.shape[1], 3), dtype=np.uint8)
    apply_npcolormap(outarray, counts, colormap)
    return outarray


filename = temp_file('popcorn2.dat')


data = make_nparray_data(paint, WIDTH, WIDTH, channels=1)
save_nparray(filename, data)

data = load_nparray(filename)
print_stats(data)
print_histogram(data)

frame = colorise(data)

save_nparray_image('popcorn2.png', frame)
