# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo

# Text align
CENTER = 0
MIDDLE = 0
LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4
BASELINE = 5

# Fill rule
EVEN_ODD=0
WINDING=1

## Line cap/join
MITER = 0  # join
ROUND = 1  # join/cap
BEVEL = 2  # join
BUTT = 3   # cap
SQUARE = 4 # cap



def setup(ctx, pixel_width, pixel_height, width=None, height=None, startx=0, starty=0, background=None, flip=False):
    '''
    Set up the context initial sclaling and background color
    :param ctx: The context
    :param width: The user space width
    :param height:  The user space width
    :param startx: The x offset of the top left corner from the origin
    :param starty: The y offset of the top left corner from the origin
    :param background: Color of the background
    :param flip: If true, user space is flipped in the y direction.
    :return:
    '''

    if not height and not width:
        width = pixel_width
        height = pixel_height
    elif not height:
        height = width * pixel_height / pixel_width
    elif not width:
        width = height * pixel_width / pixel_height

    if flip:
        ctx.scale(1, -1)
        ctx.translate(0, -pixel_height)

    ctx.scale(pixel_width / width, pixel_height / height)
    ctx.translate(-startx, -starty)

    if background:
        ctx.set_source_rgba(*background)
        ctx.paint()



def make_image(outfile, draw, width, height, channels=3):
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


def make_images(outfile, draw, width, height, count, channels=3):
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


def make_svg(outfile, draw, width, height):
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


