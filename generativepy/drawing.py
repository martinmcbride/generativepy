# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
from generativepy.color import Color

def makeImage(outfile, draw, width, height, channels=3):
    '''
    Create a PNG file using cairo
    :param outfile: Name of output file
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
    surface.write_to_png(outfile)


def makeImages(outfile, draw, width, height, count, channels=3):
    '''
    Create a sequence of PNG files using cairo
    :param outfile: Base name of output files
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param count: number of frames to create
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    for i in range(count):
        fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
        surface = cairo.ImageSurface(fmt, width, height)
        ctx = cairo.Context(surface)
        draw(ctx, width, height, i, count)
        surface.write_to_png(outfile + str(i).zfill(8) + '.png')


def makeSvg(outfile, draw, width, height):
    '''
    Create an SVG file using cairo
    :param outfile: Name of output file
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param pixelSize: size in pixels tuple (x, y)
    :return:
    '''
    surface = cairo.SVGSurface(outfile, width, height)
    ctx = cairo.Context(surface)
    draw(ctx, width, height, 0, 1)
    ctx.show_page()

