# Author:  Martin McBride
# Created: 2019-01-24
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import numpy as np
from PIL import Image

'''
The movie functions operate pn lazy sequences of images. The images are stored as numpy arrays.
'''

def duplicateFrame(frame, count):
    '''
    Duplicate a single frame, multiple times
    :param frame: the frame, a numpy array
    :param count: Number of times to duplicate
    :return: Generator
    '''
    for i in range(count):
        yield frame

def makeFrame(draw, width, height, channels=3):
    '''
    Create a numpy frame file using cairo
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    surface = cairo.ImageSurface(fmt, width, height)
    ctx = cairo.Context(surface)
    draw(ctx, width, height, 0, 1)
    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (height, width, 4)
    if channels==3:
        a[:, :, [0, 1, 2]] = a[:, :, [2, 1, 0]]
    elif channels==4:
        a[:, :, [0, 1, 2, 3]] = a[:, :, [2, 1, 0, 3]]
    return a

def makeFrames(draw, width, height, count, channels=3):
    '''
    Create a numpy frame file using cairo
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    ;param count: number of frames to create
    :param channels: 3 for rgb, 4 for rgba
    :return: a lazy sequence of frame buffers
    '''
    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    for i in range(count):
        surface = cairo.ImageSurface(fmt, width, height)
        ctx = cairo.Context(surface)
        draw(ctx, width, height, i, count)
        buf = surface.get_data()
        a = np.frombuffer(buf, np.uint8)
        a.shape = (height, width, 4)
        if channels == 3:
            a[:, :, [0, 1, 2]] = a[:, :, [2, 1, 0]]
        elif channels == 4:
            a[:, :, [0, 1, 2, 3]] = a[:, :, [2, 1, 0, 3]]
        yield a

def saveFrame(filepath, frame):
    """
    Save a frame as a png image
    :param filepath: Full name and path of the file (.png extension optional)
    :param frame: The sequence of frames
    :return:
    """
    if not filepath.lower().endswith('.png'):
        filepath += '.png'
    image = Image.fromarray(frame)
    image.save(filepath)

def saveFrames(filepath, frames):
    """
    Save a sequence of frame as a sequence of png images
    :param filepath: Base name and path of the file
    :param frames: The sequence of frames
    :return:
    """

    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        image.save(filepath + str(i).zfill(8) + '.png')

