# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

# Compare all the example images

from PIL import Image
from PIL import ImageChops


def compare_images(name):
    with Image.open(name) as im1:
        with Image.open("images/" + name) as im2:
            if im1.size != im2.size:
                return False
            if im1.mode != im2.mode:
                return False
            diff = ImageChops.difference(im1, im2)
            if diff.getbbox():
                return False

    return True


tests = [compare_images("colour-rgb.png"),
         compare_images("colour-grey.png"),
         compare_images("colour-css.png"),
         compare_images("colour-hsl.png"),
         compare_images("colour-alpha.png"),
         compare_images("colour-delta.png"),
         compare_images("text-drawing.png"),
         compare_images("text-offset.png"),
         ]

print("Passed" if all(tests) else "Failed")
