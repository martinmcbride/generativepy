#####
# Author:  Martin McBride
# Created: 2017-01-22
# Copyright (C) 2017, Martin McBride
#
# Python image texture library
#####

try:
    import textures
except ImportError:
    # if textures is not installed append directory to sys.path
    import sys, os
    print(os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/../source'))
    sys.path.insert(0, os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/../source'))

import numpy as np
from textures.image import Img
from textures.generate import fill

img = Img(256, 128)
fill(img, (.5, .5, 1, 1))
img.save("fill.png")
