#####
# Author:  Martin McBride
# Created: 2017-01-22
# Copyright (C) 2017, Martin McBride
#
# Python texture library
#####
from PIL import Image
import numpy as np

def create_image(width, height, channels):
    """
    Create a new np array to hold an image
    :param width: Image width in pixels
    :param height: Image height in pixels
    :param channels: Number of channels
    :return:
    """
    return np.zeros((height, width, channels))


def save(img, filename):
    """
    Save the image as a file
    :param img: numpy array of floats, nominally in range 0.0 to 1.0
    :param filename: name of file, extension indicates the format
    :return:
    """
    a = img * 256
    a = np.clip(a, 0, 255)
    b = a.astype(np.uint8)
    print(b)
    im = Image.fromarray(b)
    im.save(filename)
