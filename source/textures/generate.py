#####
# Author:  Martin McBride
# Created: 2017-03-16
# Copyright (C) 2017, Martin McBride
#
# Python texture library
#####

import numpy as np
import random

def noise(img, min=0, max=1):
    """
    File an image with random values.
    :param img: The image
    :param min: Minimum noise value
    :param max: Maximum noise value
    :return: img
    """

    img.data *= 0
    for row in img.data:
        for x in np.nditer(row, op_flags=['readwrite']):
            x += random.uniform(min, max)

    return img

def fill(img, color):
    """
    Fill an image with a fixed color
    :param img: Existing image
    :param color: Colour (4-tuple)
    :return: img
    """

    img.data[:,:] = color
    return img
