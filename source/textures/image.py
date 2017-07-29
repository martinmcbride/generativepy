#####
# Author:  Martin McBride
# Created: 2017-01-22
# Copyright (C) 2017, Martin McBride
#
# Python texture library
#####
from PIL import Image
import numpy as np


class Img:
    def __init__(self, other):
        self.data = np.copy(other)

    def __init__(self, width, height):
        self.data = np.zeros((height, width, 4))

    def save(self, filename):
        """
        Save the image as a file
        :param filename: name of file, extension indicates the format
        :return:
        """

        a = self.data * 256
        a = np.clip(a, 0, 255)
        b = a.astype(np.uint8)
        im = Image.fromarray(b)
        im.save(filename)
