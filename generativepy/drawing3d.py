# Author:  Martin McBride
# Created: 2021-019-01
# Copyright (C) 2018, Martin McBride
# License: MIT

import moderngl
import numpy as np
from PIL import Image
from generativepy.color import Color


def make_3dimage(outfile, draw, width, height, background=Color(0), channels=3):
    '''
    Create a PNG file using moderngl
    :param outfile: Name of output file
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param background: background colour
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    frame = make_3dimage_frame(draw, width, height, background, channels)
    image = Image.fromarray(frame)
    image.save(outfile + '.png')

def make_3dimage_frame(draw, width, height, background=Color(0), channels=3):
    '''
    Create a numpy frame file using moderngl
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param background: background colour
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    ctx = moderngl.create_standalone_context()
    fbo = ctx.simple_framebuffer((width, height))
    fbo.use()
    fbo.clear(*background)

    draw(ctx, width, height, 0, 1)

    data = fbo.read()
    frame = np.frombuffer(data, dtype=np.uint8)
    frame = frame.reshape((height, width, 3))
    frame = frame[::-1]
    ctx.release()

    return frame

def make_3dimage_frames(draw, width, height, count, background=Color(0), channels=3):
    '''
    Create a sequence of numpy frame file using moderngl
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param count: number of frames to create
    :param background: background colour
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    for i in range(count):
        ctx = moderngl.create_standalone_context()
        fbo = ctx.simple_framebuffer((width, height))
        fbo.use()
        fbo.clear(*background)

        draw(ctx, width, height, i, count)

        data = fbo.read()
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = frame.reshape((height, width, 3))
        frame = frame[::-1]
        ctx.release()

        yield frame

def make_3dimages(outfile, draw, width, height, background=Color(0), channels=3):
    '''
    Create a sequence of PNG files using moderngl
    :param outfile: Name of output file
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param count: number of frames to create
    :param background: background colour
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    frames = make_3dimage_frames(draw, width, height, background, channels)
    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        image.save(outfile + str(i).zfill(8) + '.png')


