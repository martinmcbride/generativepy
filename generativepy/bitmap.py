# Author:  Martin McBride
# Created: 2019-04-27
# Copyright (C) 2019, Martin McBride
# License: MIT

import numpy as np
from generativepy import movie

# Orienatation
BM_ROWCOL = 0   #Left to right, top to bottom
BM_IMAGE = 1    #Top to bottom, left to right


class BitmapScaling():

    def __init__(self, pixelSize, width=None, height=None, startX=0, startY=0, channels=3, orientation=BM_IMAGE):
        self.pixelSize = pixelSize
        self.startX = startX
        self.startY = startY
        self.channels = channels
        self.orientation = orientation

        self.width = width
        self.height = height
        if not height and not width:
            self.width = pixelSize[0]
            self.height = pixelSize[1]
        elif not height:
            self.height = width * pixelSize[1] / pixelSize[0]
        elif not width:
            self.width = height * pixelSize[0] / pixelSize[1]

    def page2user(self, pos):
        x = self.startX + pos[0]*self.width/self.pixelSize[0]
        y = self.startY + pos[1]*self.height/self.pixelSize[1]
        return x, y

    def user2page(self, pos):
        x = (pos[0] - self.startX)*self.pixelSize[0]/self.width
        y = (pos[1] - self.startY)*self.pixelSize[1]/self.height
        if 0 <= x < self.pixelSize[0] and 0 <= y < self.pixelSize[1]:
           return int(x), int(y)
        return None


def makeBitmapImage(outfile, draw, pixelSize, width=None, height=None,
              startX=0, startY=0, channels=3, orientation=BM_IMAGE):
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
    if not height and not width:
        width = pixelSize[0]
        height = pixelSize[1]
    elif not height:
        height = width * pixelSize[1] / pixelSize[0]
    elif not width:
        width = height * pixelSize[0] / pixelSize[1]
    scaling = BitmapScaling(pixelSize, width, height, startX, startY, channels, orientation)
    array = draw(array, scaling)
    img = np.clip(array*256, 0, 255).astype(np.uint8)
    if orientation==BM_IMAGE:
        img = img.transpose(1, 0, 2)
    movie.saveFrame(outfile, img)
