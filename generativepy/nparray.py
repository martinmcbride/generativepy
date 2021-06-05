# Author:  Martin McBride
# Created: 2020-11-22
# Copyright (C) 2020, Martin McBride
# License: MIT

import numpy as np
from generativepy.movie import save_frame, save_frames
from generativepy.color import make_colormap

def make_nparray_frame(paint, pixel_width, pixel_height, channels=3, out=None):
    '''
    Create a frame using numpy
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :param out: optional array to hold result. Must be correct width, height and channels, but can be any int type
    :return: a frame buffer
    '''
    if out is not None:
        if out.shape != (pixel_height, pixel_width, channels):
            raise ValueError('out array shape not compatible with image dimensions')
        array = out
    else:
        array = np.full((pixel_height, pixel_width, channels), 255, dtype=np.uint)
    paint(array, pixel_width, pixel_height, 0, 1)
    array = np.clip(array, 0, 255).astype(np.uint8)
    return array

def make_nparray_data(paint, pixel_width, pixel_height, channels=3, dtype=np.uint):
    '''
    Create a frame using numpy
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :param out: optional array to hold result. Must be correct width, height and channels, but can be any int type
    :return: a frame buffer
    '''
    array = np.full((pixel_height, pixel_width, channels), 0, dtype=dtype)
    paint(array, pixel_width, pixel_height, 0, 1)
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
    frames = make_nparray_frames(paint, pixel_width, pixel_height, count, channels)
    save_frames(outfile, frames)

def save_nparray(outfile, array):
    '''
    Save an array to file
    :param outfile: file path including extension
    :param array: numpy array to be saved
    :return:
    '''
    with open(outfile, 'wb') as f:
        np.save(f, array)

def save_nparray_image(outfile, array):
    '''
    Save an array to an image file
    :param outfile: file path including extension
    :param array: numpy array to be saved
    :return:
    '''
    array = np.clip(array, 0, 255).astype(np.uint8)
    save_frame(outfile, array)

def load_nparray(infile):
    '''
    Load a numpy array from file
    :param infile: file path including extension
    :return: a numpy array, no checking is done on the array
    '''
    with open(infile, 'rb') as f:
        return np.load(f)

def make_npcolormap(length, colors, bands=None, channels=3):
    '''
    Create a colormap, a list of varying colors, as a numpy array
    :param length: Total size of list
    :param colors: List of colors, must be at least 2 long.
    :param bands: Relative size of each band. bands[i] gives the size of the band between color[i] and color[i+1].
                  len(bands) must be exactly 1 less than len(colors). If bands is None, equal bands will be used.
    :param channels: 3 for RGB, 4 for RGBA
    :return: an array of shape (length, channels) containing the RGB(A) values for each entry, as integers from 0-255
    '''

    colors = make_colormap(length, colors, bands)

    npcolormap = np.zeros((length, channels), dtype=np.uint8)
    for i in range(length):
        rgba = colors[i].as_rgba_bytes()
        npcolormap[i, 0] = rgba[0]
        npcolormap[i, 1] = rgba[1]
        npcolormap[i, 2] = rgba[2]
        if channels==4:
            npcolormap[i, 3] = rgba[3]

    return npcolormap

def apply_npcolormap(out, counts, npcolormap):
    '''
    Apply a color map to an array of counts, filling an existing output array
    :param out: The output array, height x width x channels (channels is 3 or 4)
    :param counts: The counts array, height x width, count range 0 to max_count
    :param npcolormap: A numpy color map, must have at least maxcount+1 elements
    :return:
    '''

    if out.shape[0] != counts.shape[0] or out.shape[1] != counts.shape[1]:
        raise ValueError('out and counts are incompatible shapes')

    if np.max(counts) > npcolormap.shape[0]:
        raise ValueError('npcolormap too small for maximum value in counts array')

    out[...] = npcolormap[counts]