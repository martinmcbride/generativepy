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

import textures.image
import textures.generate

img = textures.image.create_image(128, 128, 1)
textures.generate.noise(img)
textures.generate.noise(img)
textures.image.save(img, "noise.png")
