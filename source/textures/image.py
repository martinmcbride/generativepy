#####
# Author:  Martin McBride
# Created: 2017-01-22
# Copyright (C) 2017, Martin McBride
#
# Python texture library
#####
from PIL import Image
import numpy as np

def create_image(rows, cols, channels):
    """
    Create a new np array to hold an image
    :param rows: Image height in pixels
    :param cols: Image width in pixels
    :param channels: Number of channels
    :return:
    """
    return np.zeros((rows, cols, channels))


def save(img, filename):
    """
    Save the image as a file
    :param img: numpy array of floats, nominally in range 0.0 to 1.0
    :param filename: name of file, extension indicates the format
    :return:
    """

    a = img * 256
    # If the array is a monochrome image (rows, cols, 1), convert ir to a 2D array (rows, cols) otherwise pillow
    # will give an error.
    if len(a.shape) > 2 and a.shape[2] == 1:
        a.shape = a.shape[:2]
    a = np.clip(a, 0, 255)
    b = a.astype(np.uint8)
    im = Image.fromarray(b)
    im.save(filename)
