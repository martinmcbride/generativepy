# Author:  Martin McBride
# Created: 2019-04-27
# Copyright (C) 2019, Martin McBride
# License: MIT

import numpy as np
from generativepy import movie

OR_BITMAP_ROWCOL = 0

def makeBitmapImage(outfile, draw, pixelSize, channels=3, orientation=OR_BITMAP_ROWCOL):
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
##    img = img.transpose(1, 0, 2)
    movie.saveFrame(outfile, img)
