# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import numpy as np
from PIL import Image

class array_image_scale():

    def __init__(self, pixel_size, width, height, startx, starty):
        self.pixel_size = pixel_size
        self.width = width
        self.height = height
        self.startx = startx
        self.starty = starty

    def user2pixel(self, pos):
        x = (pos[0] - self.startx) * self.pixel_size[0] / self.width
        y = (pos[1] - self.starty) * self.pixel_size[1] / self.height
        if 0 <= x < self.pixel_size[0] and 0 <= y < self.pixel_size[1]:
            return int(x), int(y)
        return None


def save_array_image(outfile, img):
    img = np.clip(img*256, 0, 255).astype(np.uint8)
    img = img.transpose(1, 0, 2)
    image = Image.fromarray(img)
    image.save(outfile)


def make_array_png(outfile, draw, pixel_size, width=None, height=None,
                       startx=0, starty=0, color=None, channels=3, **extras):
    '''
    Create a PNG file using numpy
    :param outfile: Name of output file
    :param draw: the draw function
    :param pixel_size: size in pixels tuple (x, y)
    :param width: width in user coords
    :param height: height in user coord
    :param startx: x value of left edge of image, user coords
    :param starty: y value of top edge of image, user coords
    :param color: background color
    :param channels: 3 for rgb, 4 for rgba
    :param extras: optional extra params for draw function
    :return:
    '''
    if not height and not width:
        width = pixel_size[0]
        height = pixel_size[1]
    elif not height:
        height = width * pixel_size[1] / pixel_size[0]
    elif not width:
        width = height * pixel_size[0] / pixel_size[1]

    img = np.zeros([pixel_size[0], pixel_size[1], channels], np.float32)
    if color:
        img[:, :] = color
    scale = array_image_scale(pixel_size, width, height, startx, starty)
    draw(img, scale=scale, pixel_size=pixel_size, width=width, height=height, startx=startx, starty=starty, **extras)
    save_array_image(outfile, img)

