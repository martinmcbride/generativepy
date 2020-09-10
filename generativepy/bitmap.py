# Author:  Martin McBride
# Created: 2020-09-05
# Copyright (C) 2020, Martin McBride
# License: MIT

from PIL import Image

class Scaler:

    def __init__(self, pixel_width, pixel_height, width=None, height=None, startx=0, starty=0):
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        if not height and not width:
            self.width = pixel_width
            self.height = pixel_height
        elif not height:
            self.height = self.width * pixel_height / pixel_width
        elif not width:
            self.width = self.height * pixel_width / pixel_height

    def device_to_user(self, device_x, device_y):
        user_x = device_x * self.width / self.pixel_width + self.startx
        user_y = device_y * self.height / self.pixel_height + self.starty
        return user_x, user_y

    def user_to_device(self, user_x, user_y):
        device_x = int((user_x - self.startx) * self.pixel_width / self.width)
        device_y = int((user_y - self.starty) * self.pixel_height / self.height)
        return device_x, device_y


def make_bitmap(outfile, paint, pixel_width, pixel_height, channels=3):
    '''
    Create a PNG file using PIL
    :param outfile: Name of output file
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return:
    '''
    if channels == 1:
        mode = 'L'
    elif channels == 4:
        mode = 'RGBA'
    else:
        mode = 'RGB'

    image = Image.new(mode, (pixel_width, pixel_height), 'white')
    paint(image, pixel_width, pixel_height, 0, 1)
    image.save(outfile)
