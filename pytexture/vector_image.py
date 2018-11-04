# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo


def set_color(ctx, color):
    if len(color)==4:
        ctx.set_source_rgba(*color)
    else:
        ctx.set_source_rgb(*color)


def make_vector_png(outfile, draw, pixel_size, width=None, height=None,
                       startx=0, starty=0, color=None, channels=3, **extras):
    '''
    Create a PNG file using cairo
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
        width = height*pixel_size[0]/pixel_size[1]

    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    surface = cairo.ImageSurface(fmt, pixel_size[0], pixel_size[1])
    ctx = cairo.Context(surface)
    if color:
        ctx.rectangle(0, 0, pixel_size[0], pixel_size[1])
        set_color(ctx, color)
        ctx.fill()
    ctx.scale(pixel_size[0]/width, pixel_size[1]/height)
    ctx.translate(-startx, -starty)
    draw(ctx, pixel_size=pixel_size, width=width, height=height, startx=startx, starty=starty, **extras)
    surface.write_to_png(outfile)


