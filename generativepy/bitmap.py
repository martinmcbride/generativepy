# Author:  Martin McBride
# Created: 2019-04-27
# Copyright (C) 2019, Martin McBride
# License: MIT

import numpy as np
from generativepy import movie

class BitmapScaling():

    def __init__(self, pixelSize, width=None, height=None, startX=0, startY=0):
        self.pixelSize = pixelSize
        self.startX = startX
        self.startY = startY

        self.width = width
        self.height = height
        if not height and not width:
            self.width = pixelSize[0]
            self.height = pixelSize[1]
        elif not height:
            self.height = width * pixelSize[1] / pixelSize[0]
        elif not width:
            self.width = height * pixelSize[0] / pixelSize[1]

    def p2u(self, pixel):
        ux =


def makeBitmapImage(outfile, draw, pixelSize, width=None, height=None,
              startX=0, startY=0, channels=3):
    '''
    Create a PNG file using numpy
    :param outfile: Name of output file
    :param draw: the draw function
    :param pixelSize: size in pixels tuple (x, y)
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    shape = (pixelSize[0], pixelSize[1], channels)
    array = np.zeros(shape)
    array = draw(array, pixelSize, channels)
    img = np.clip(array*256, 0, 255).astype(np.uint8)
    img = img.transpose(1, 0, 2)
    movie.saveFrame(outfile, img)
