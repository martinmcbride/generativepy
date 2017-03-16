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
    :param img: The image, any number of channels
    :param min: Minimum noise value
    :param max: Maximum noise value
    :return: img
    """

    img *= 0
    for row in img:
        for x in np.nditer(row, op_flags=['readwrite']):
            x += random.uniform(min, max)

    return img
