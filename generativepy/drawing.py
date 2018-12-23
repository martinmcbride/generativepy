# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math

class Canvas:

    def __init__(self, ctx, pixelSize):
        self.pixelSize = pixelSize
        self.ctx = ctx
        self.initial_matrix = ctx.get_matrix()
        self.fillColor = None
        self.strokeColor = (0, 0, 0)
        self.lineWidth = 1

    def setColor(self, color):
        if len(color)==4:
            self.ctx.set_source_rgba(*color)
        else:
            self.ctx.set_source_rgb(*color)

    def fillStroke(self):
        if self.fillColor:
            self.setColor(self.fillColor)
            if self.strokeColor:
                self.ctx.fill_preserve()
            else:
                self.ctx.fill()
        if self.strokeColor:
            self.ctx.set_line_width(self.lineWidth)
            self.setColor(self.strokeColor)
            self.ctx.stroke()

    def scale(self, x, y=None):
        if y:
            self.ctx.scale(x, y)
        else:
            self.ctx.scale(x, x)
        return self

    def translate(self, x, y):
        self.ctx.translate(x, y)
        return self

    def background(self, color):
        if color:
            self.ctx.save()
            self.ctx.set_matrix(self.initial_matrix)
            self.ctx.rectangle(0, 0, self.pixelSize[0], self.pixelSize[1])
            self.setColor(color)
            self.ctx.fill()
            self.ctx.restore()
        return self

    def fill(self, color):
        self.fillColor = color
        return self

    def noFill(self):
        self.fillColor = None
        return self

    def stroke(self, color):
        self.strokeColor = color
        return self

    def noStroke(self):
        self.strokeColor = None
        return self

    def strokeWeight(self, weight):
        self.lineWidth = weight
        return self

    def line(self, x0, y0, x1, y1):
        self.ctx.move_to(x0, y0)
        self.ctx.line_to(x1, y1)
        self.fillStroke()
        return self

    def rect(self, a, b, c, d):
        self.ctx.rectangle(a, b, c, d)
        self.fillStroke()
        return self

    def circle(self, a, b, r):
        self.ctx.arc(a, b, r, 0, 2*math.pi)
        self.fillStroke()
        return self

    def polygon(self, points, close=True):
        first = True
        for p in points:
            if first:
                self.ctx.move_to(*p)
                first = False
            else:
                self.ctx.line_to(*p)
        if close:
            self.ctx.close_path()
        self.fillStroke()
        return self



def makeImage(outfile, draw, pixelSize, width=None, height=None,
               startX=0, startY=0, color=None, channels=3):
    '''
    Create a PNG file using cairo
    :param outfile: Name of output file
    :param draw: the draw function
    :param pixelSize: size in pixels tuple (x, y)
    :param width: width in user coords
    :param height: height in user coord
    :param startX: x value of left edge of image, user coords
    :param startY: y value of top edge of image, user coords
    :param color: background color
    :param channels: 3 for rgb, 4 for rgba
    :param extras: optional extra params for draw function
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
    canvas = Canvas(ctx, pixelSize).background(color)
    canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
    draw(canvas)
    surface.write_to_png(outfile)


