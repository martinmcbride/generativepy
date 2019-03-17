# Author:  Martin McBride
# Created: 2019-01-24
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import numpy as np
from PIL import Image
from generativepy import drawing

def duplicateFrame(frame, count):
    '''
    Duplicate a single frame, multiple times
    :param frame: the frame
    :param count: Number of times to duplicate
    :return: Generator
    '''
    for i in range(count):
        yield frame

def makeFrame(draw, pixelSize, width=None, height=None,
              startX=0, startY=0, background=None, channels=3, orientation=drawing.OR_IMAGE):
    '''
    Create a numpy frame file using cairo
    :param draw: the draw function
    :param pixelSize: size in pixels tuple (x, y)
    :param width: width in user coords
    :param height: height in user coord
    :param startX: x value of left edge of image, user coords
    :param startY: y value of top edge of image, user coords
    :param background: background color
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    if not height and not width:
        width = pixelSize[0]
        height = pixelSize[1]
    elif not height:
        height = width * pixelSize[1] / pixelSize[0]
    elif not width:
        width = height * pixelSize[0] / pixelSize[1]

    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    surface = cairo.ImageSurface(fmt, pixelSize[0], pixelSize[1])
    ctx = cairo.Context(surface)
    canvas = drawing.Canvas(ctx, pixelSize, orientation).background(background)
    canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
    draw(canvas)
    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (pixelSize[1], pixelSize[0], 4)
    if channels==3:
        a[:, :, [0, 1, 2]] = a[:, :, [2, 1, 0]]
    elif channels==4:
        a[:, :, [0, 1, 2, 3]] = a[:, :, [2, 1, 0, 3]]
    return a

def makeFrames(draw, pixelSize, count, width=None, height=None,
              startX=0, startY=0, background=None, channels=3, orientation=drawing.OR_IMAGE):
    '''
    Create a numpy frame file using cairo
    :param draw: the draw function
    :param pixelSize: size in pixels tuple (x, y)
    :param count: number of frames to create
    :param width: width in user coords
    :param height: height in user coord
    :param startX: x value of left edge of image, user coords
    :param startY: y value of top edge of image, user coords
    :param background: background color
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    if not height and not width:
        width = pixelSize[0]
        height = pixelSize[1]
    elif not height:
        height = width * pixelSize[1] / pixelSize[0]
    elif not width:
        width = height * pixelSize[0] / pixelSize[1]

    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    for i in range(count):
        surface = cairo.ImageSurface(fmt, pixelSize[0], pixelSize[1])
        ctx = cairo.Context(surface)
        canvas = drawing.Canvas(ctx, pixelSize, orientation).background(background)
        canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
        draw(canvas, i, count)
        buf = surface.get_data()
        a = np.frombuffer(buf, np.uint8)
        a.shape = (pixelSize[1], pixelSize[0], 4)
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

