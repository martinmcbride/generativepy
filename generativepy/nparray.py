# Author:  Martin McBride
# Created: 2020-11-22
# Copyright (C) 2020, Martin McBride
# License: MIT

import numpy as np
from generativepy.movie import save_frame, save_frames

def make_nparray_frame(paint, pixel_width, pixel_height, channels=3):
    '''
    Create a frame using numpy
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return: a frame buffer
    '''
    array = np.full((pixel_height, pixel_width, channels), 255, dtype=np.uint)
    paint(array, pixel_width, pixel_height, 0, 1)
    array = np.clip(array, 0, 255).astype(np.uint8)
    return array

def make_nparray_frames(paint, pixel_width, pixel_height, count, channels=3):
    '''
    Create a frame sequence using numpy
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param count: number of frames to create
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return: a lazy sequence of frame buffers
    '''
    for i in range(count):
        array = np.full((pixel_height, pixel_width, channels), 255, dtype=np.uint)
        paint(array, pixel_width, pixel_height, i, count)
        array = np.clip(array, 0, 255).astype(np.uint8)
        yield array


def make_nparray(outfile, paint, pixel_width, pixel_height, channels=3):
    '''
    Create a PNG file using numpy
    :param outfile: Name of output file
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return:
    '''
    frame = make_nparray_frame(paint, pixel_width, pixel_height, channels)
    save_frame(outfile, frame)

def make_nparrays(outfile, paint, pixel_width, pixel_height, count, channels=3):
    '''
    Create a set of PNG files using numpy
    :param outfile: Name of output file
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param count: number of frames to create
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return:
    '''
    frames = make_nparray_frames(paint, pixel_width, pixel_height, channels)
    save_frames(outfile, frames)

