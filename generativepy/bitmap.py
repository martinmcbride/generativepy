# Author:  Martin McBride
# Created: 2020-09-05
# Copyright (C) 2020, Martin McBride
# License: MIT

from PIL import Image
import numpy as np

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

def get_mode(channels):
    '''
    Convert the number of channels into a mode string
    :param channels:
    :return:
    '''
    if channels == 1:
        mode = 'L'
    elif channels == 4:
        mode = 'RGBA'
    else:
        mode = 'RGB'
    return mode

def get_background(channels):
    '''
    Get a suitable background colour for the given channel
    :param channels:
    :return:
    '''
    if channels == 1:
        color = 'white'
    elif channels == 4:
        color = (255, 255, 255, 0)
    else:
        color = 'white'
    return color

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
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
    paint(image, pixel_width, pixel_height, 0, 1)
    image.save(outfile + '.png')

def make_bitmaps(outfile, paint, pixel_width, pixel_height, count, channels=3):
    '''
    Create a set of PNG files using PIL
    :param outfile: Name of output file
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param count: number of frames to create
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return:
    '''
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    for i in range(count):
        image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
        paint(image, pixel_width, pixel_height, i, count)
        image.save(outfile + str(i).zfill(8) + '.png')

def make_bitmap_frame(paint, pixel_width, pixel_height, channels=3):
    '''
    Create frame using PIL
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return: a frame buffer
    '''
    image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
    paint(image, pixel_width, pixel_height, 0, 1)
    frame = np.copy(np.asarray(image))
    return frame

def make_bitmap_frames(paint, pixel_width, pixel_height, count, channels=3):
    '''
    Create frame sequence using PIL
    :param paint: the paint function
    :param pixel_width: width in pixels, int
    :param pixel_height: height in pixels, int
    :param count: number of frames to create
    :param channels: 1 for greyscale, 3 for rgb, 4 for rgba
    :return: a lazy sequence of frame buffers
    '''
    for i in range(count):
        image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
        paint(image, pixel_width, pixel_height, i, count)
        frame = np.copy(np.asarray(image))
        yield frame

