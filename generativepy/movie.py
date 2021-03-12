# Author:  Martin McBride
# Created: 2019-01-24
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import numpy as np
from PIL import Image

'''
The movie functions operate pn lazy sequences of images. The images are stored as numpy arrays.
'''

def normalise_array(array):
    """
    If greyscale array has a shape [a, b, 1] it must be normalised to [a, b] otherwise
    the pillow fromarray function will give n#an error
    :param array: The array
    :return: squeezed array if necessary, else the original array
    """
    if array.ndim == 3 and array.shape[2] == 1:
        return np.squeeze(array, axis=2)
    return array

def duplicate_frame(frame, count):
    '''
    Duplicate a single frame, multiple times
    :param frame: the frame, a numpy array
    :param count: Number of times to duplicate
    :return: Generator
    '''
    for i in range(count):
        yield frame

def save_frame(outfile, frame):
    """
    Save a frame as a png image
    :param outfile: Full name and path of the file (.png extension optional)
    :param frame: The sequence of frames
    :return:
    """

    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    image = Image.fromarray(normalise_array(frame))
    image.save(outfile + '.png')

def save_frames(outfile, frames):
    """
    Save a sequence of frame as a sequence of png images
    :param outfile: Base name and path of the file (.png extension optional)
    :param frames: The sequence of frames
    :return:
    """

    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    for i, frame in enumerate(frames):
        image = Image.fromarray(normalise_array(frame))
        image.save(outfile + str(i).zfill(8) + '.png')

