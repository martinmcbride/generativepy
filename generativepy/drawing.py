# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
from generativepy.color import Color, RGB

#Ellipse and rectangle modes
CENTER = 0 #Also used for text
RADIUS = 1
CORNER = 2
CORNERS = 3

#Arc types
OPEN = 0
CHORD = 1
PIE = 2

#Line join/end
ROUND = 0
SQUARE = 1
PROJECT = 2
MITER = 3
BEVEL = 4

#Text align
LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4
BASELINE = 5

# Orienatation
OR_IMAGE = 1    #Top to bottom, left to right
OR_MATH  = 2    #Bottom to top, left to right

def convertMode(mode, a, b, c, d):
    '''
    Convert the parameters a, b, c, d for a rectangle or ellipse based on the mode
    :param mode:
    :param a:
    :param b:
    :param c:
    :param d:
    :return: cx, cy, rx, ry as tuple
    '''
    if mode == RADIUS:
        return a, b, c, d
    elif mode == CENTER:
        return a, b, c / 2, d / 2
    elif mode == CORNERS:
        return (a+c)/2, (b+d)/2, (c-a)/2, (d-b)/2
    else:
        return a+c/2, b+d/2, c/2, d/2


class Canvas:

    def __init__(self, ctx, pixelSize, orientation=OR_IMAGE):
        self.pixelSize = pixelSize
        self.ctx = ctx
        self.orientation = orientation
        if orientation == OR_MATH:
            ctx.scale(1, -1)
            ctx.translate(0, -pixelSize[1])
        self.initial_matrix = ctx.get_matrix()
        self.fillColor = None
        self.strokeColor = Color(0, 0, 0)
        self.lineWidth = 1
        self.vStrokeDash = []
        self.vRectMode = CORNER
        self.vEllipseMode = CENTER
        self.vStrokeJoin = MITER
        self.vStrokeCap = ROUND
        self.vTextAlignX = LEFT
        self.vTextAlignY = BASELINE
        self.vTextSize = 10
        self.font = 'Ariel'
        self.vColorMode = RGB
        self.vColorRange = 1

    def page2user(self, x):
        matrix = self.ctx.get_matrix()
        scaleFactor = math.hypot(matrix[0], matrix[1])
        return (x * self.pixelSize[0]) / (100 * scaleFactor)

    def setColor(self, color):
        rgb = color.getRGB(self.vColorMode, self.vColorRange)
        if len(rgb) == 4:
            self.ctx.set_source_rgba(*rgb)
        else:
            self.ctx.set_source_rgb(*rgb)

    def setStrokeCap(self):
        if self.vStrokeCap == SQUARE:
            self.ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        elif self.vStrokeCap == PROJECT:
            self.ctx.set_line_cap(cairo.LINE_CAP_SQUARE)
        else:
            self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    def setStrokeJoin(self):
        if self.vStrokeJoin == BEVEL:
            self.ctx.set_line_join(cairo.LINE_JOIN_BEVEL)
        elif self.vStrokeJoin == ROUND:
            self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        else:
            self.ctx.set_line_join(cairo.LINE_JOIN_MITER)

    def fillStroke(self):
        if self.fillColor:
            self.setColor(self.fillColor)
            if self.strokeColor:
                self.ctx.fill_preserve()
            else:
                self.ctx.fill()
        if self.strokeColor:
            self.ctx.set_line_width(self.lineWidth)
            self.setStrokeCap()
            self.setStrokeJoin()
            self.ctx.set_dash(self.vStrokeDash)
            self.setColor(self.strokeColor)
            self.ctx.stroke()

    def colorMode(self, mode):
        self.vColorMode = mode

    def colorRange(self, range):
        self.vColorRange = range

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

    def strokeCap(self, cap):
        self.vStrokeCap = cap
        return self

    def strokeJoin(self, join):
        self.vStrokeJoin = join
        return self

    def strokeDash(self, dash):
        self.vStrokeDash = dash
        return self

    def line(self, x0, y0, x1, y1):
        self.ctx.move_to(x0, y0)
        self.ctx.line_to(x1, y1)
        self.fillStroke()
        return self

    def rectMode(self, mode):
        self.vRectMode = mode
        return self

    def ellipseMode(self, mode):
        self.vEllipseMode = mode
        return self

    def point(self, a, b):
        if self.strokeColor:
            self.ctx.rectangle(a, b, 1, 1)
            self.setColor(self.strokeColor)
            self.ctx.fill()
        return self

    def rect(self, a, b, c, d):
        cx, cy, rx, ry = convertMode(self.vRectMode, a, b, c, d)
        self.ctx.rectangle(cx-rx, cy-ry, 2*rx, 2*ry)
        self.fillStroke()
        return self

    def triangle(self, x0, y0, x1, y1, x2, y2):
        self.ctx.move_to(x0, y0)
        self.ctx.line_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.close_path()
        self.fillStroke()
        return self

    def quad(self, x0, y0, x1, y1, x2, y2, x3, y3):
        self.ctx.move_to(x0, y0)
        self.ctx.line_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.line_to(x3, y3)
        self.ctx.close_path()
        self.fillStroke()
        return self

    def ellipse(self, a, b, c, d):
        cx, cy, rx, ry = convertMode(self.vEllipseMode, a, b, c, d)
        self.ctx.save()
        self.ctx.translate(cx, cy)
        self.ctx.scale(rx, ry)
        self.ctx.arc(0, 0, 1, 0, 2*math.pi)
        self.ctx.restore()
        self.fillStroke()
        return self

    def arc(self, a, b, c, d, start, end, mode=OPEN):
        cx, cy, rx, ry = convertMode(self.vEllipseMode, a, b, c, d)
        self.ctx.save()
        self.ctx.translate(cx, cy)
        self.ctx.scale(rx, ry)
        if mode == OPEN:
            self.ctx.arc(0, 0, 1, start, end)
        elif mode == CHORD:
            self.ctx.arc(0, 0, 1, start, end)
            self.ctx.close_path()
        elif mode == PIE:
            self.ctx.move_to(0, 0)
            self.ctx.arc(0, 0, 1, start, end)
            self.ctx.close_path()
        self.ctx.restore()
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

    def image(self, image, x, y):
        if isinstance(image, str):
            image = cairo.ImageSurface.create_from_png(image)
        self.ctx.set_source_surface(image, x, y)
        self.ctx.paint()
        return self

    def textAlign(self, alignx, aligny=BASELINE):
        self.vTextAlignX = alignx
        self.vTextAlignY = aligny
        return self

    def textSize(self, size):
        self.vTextSize = size
        return self

    def textFont(self, font):
        self.font = font
        return self

    def text(self, txt, x, y):
        self.ctx.select_font_face(self.font, cairo.FONT_SLANT_NORMAL,
                                  cairo.FONT_WEIGHT_BOLD)
        self.ctx.set_font_size(self.vTextSize)
        self.setColor(self.fillColor)

        xb, yb, width, height, dx, dy = self.ctx.text_extents(txt)

        x -= xb
        if self.vTextAlignX == CENTER:
            x -=  width/2
        elif self.vTextAlignX == RIGHT:
            x -=  width

        if self.vTextAlignY == CENTER:
            dy = -yb/2
        elif self.vTextAlignY == BOTTOM:
            dy = -(yb + height)
        elif self.vTextAlignY == TOP:
            dy = -yb

        if self.orientation == OR_MATH:
            self.ctx.move_to(x, y - dy)
            self.ctx.save()
            self.ctx.scale(1, -1)
            self.ctx.show_text(txt)
            self.ctx.restore()
        else:
            self.ctx.move_to(x, y + dy)
            self.ctx.show_text(txt)
        return self


def makeImage(outfile, draw, pixelSize, width=None, height=None,
              startX=0, startY=0, background=None, channels=3, orientation=OR_IMAGE):
    '''
    Create a PNG file using cairo
    :param outfile: Name of output file
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
    canvas = Canvas(ctx, pixelSize, orientation).background(background)
    canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
    draw(canvas)
    surface.write_to_png(outfile)


def makeImages(outfile, draw, pixelSize, count, width=None, height=None,
              startX=0, startY=0, background=None, channels=3, orientation=OR_IMAGE):
    '''
    Create a sequence of PNG files using cairo
    :param outfile: Base name of output files
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

    for i in range(count):
        fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
        surface = cairo.ImageSurface(fmt, pixelSize[0], pixelSize[1])
        ctx = cairo.Context(surface)
        canvas = Canvas(ctx, pixelSize, orientation).background(background)
        canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
        draw(canvas, i, count)
        surface.write_to_png(outfile + str(i).zfill(8) + '.png')


def makeSvg(outfile, draw, pixelSize, width=None, height=None,
              startX=0, startY=0, background=None, orientation=OR_IMAGE):
    '''
    Create an SVG file using cairo
    :param outfile: Name of output file
    :param draw: the draw function
    :param pixelSize: size in pixels tuple (x, y)
    :param width: width in user coords
    :param height: height in user coord
    :param startX: x value of left edge of image, user coords
    :param startY: y value of top edge of image, user coords
    :param background: background color
    :return:
    '''
    if not height and not width:
        width = pixelSize[0]
        height = pixelSize[1]
    elif not height:
        height = width * pixelSize[1] / pixelSize[0]
    elif not width:
        width = height * pixelSize[0] / pixelSize[1]

    surface = cairo.SVGSurface(outfile, pixelSize[0], pixelSize[1])
    ctx = cairo.Context(surface)
    canvas = Canvas(ctx, pixelSize, orientation).background(background)
    canvas.scale(pixelSize[0] / width, pixelSize[1] / height).translate(-startX, -startY)
    draw(canvas)
    ctx.show_page()

