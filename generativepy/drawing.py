# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
import colorsys

# Color modes
RGB = 1
HSL = 2

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

cssColors = {
"purple":(128,0,128),
"fuchsia":(255,0,255),
"lime":(0,255,0),
"teal":(0,128,128),
"aqua":(0,255,255),
"blue":(0,0,255),
"navy":(0,0,128),
"black":(0,0,0),
"gray":(128,128,128),
"silver":(192,192,192),
"white":(255,255,255),
"indianred":(205,92,92),
"lightcoral":(240,128,128),
"salmon":(250,128,114),
"darksalmon":(233,150,122),
"lightsalmon":(255,160,122),
"crimson":(220,20,60),
"red":(255,0,0),
"firebrick":(178,34,34),
"darkred":(139,0,0),
"pink":(255,192,203),
"lightpink":(255,182,193),
"hotpink":(255,105,180),
"deeppink":(255,20,147),
"mediumvioletred":(199,21,133),
"palevioletred":(219,112,147),
"coral":(255,127,80),
"tomato":(255,99,71),
"orangered":(255,69,0),
"darkorange":(255,140,0),
"orange":(255,165,0),
"gold":(255,215,0),
"yellow":(255,255,0),
"lightyellow":(255,255,224),
"lemonchiffon":(255,250,205),
"lightgoldenrodyellow":(250,250,210),
"papayawhip":(255,239,213),
"moccasin":(255,228,181),
"peachpuff":(255,218,185),
"palegoldenrod":(238,232,170),
"khaki":(240,230,140),
"darkkhaki":(189,183,107),
"lavender":(230,230,250),
"thistle":(216,191,216),
"plum":(221,160,221),
"violet":(238,130,238),
"orchid":(218,112,214),
"fuchsia":(255,0,255),
"magenta":(255,0,255),
"mediumorchid":(186,85,211),
"mediumpurple":(147,112,219),
"blueviolet":(138,43,226),
"darkviolet":(148,0,211),
"darkorchid":(153,50,204),
"darkmagenta":(139,0,139),
"purple":(128,0,128),
"rebeccapurple":(102,51,153),
"indigo":(75,0,130),
"mediumslateblue":(123,104,238),
"slateblue":(106,90,205),
"darkslateblue":(72,61,139),
"greenyellow":(173,255,47),
"chartreuse":(127,255,0),
"lawngreen":(124,252,0),
"lime":(0,255,0),
"limegreen":(50,205,50),
"palegreen":(152,251,152),
"lightgreen":(144,238,144),
"mediumspringgreen":(0,250,154),
"springgreen":(0,255,127),
"mediumseagreen":(60,179,113),
"seagreen":(46,139,87),
"forestgreen":(34,139,34),
"green":(0,128,0),
"darkgreen":(0,100,0),
"yellowgreen":(154,205,50),
"olivedrab":(107,142,35),
"olive":(128,128,0),
"darkolivegreen":(85,107,47),
"mediumaquamarine":(102,205,170),
"darkseagreen":(143,188,143),
"lightseagreen":(32,178,170),
"darkcyan":(0,139,139),
"teal":(0,128,128),
"aqua":(0,255,255),
"cyan":(0,255,255),
"lightcyan":(224,255,255),
"paleturquoise":(175,238,238),
"aquamarine":(127,255,212),
"turquoise":(64,224,208),
"mediumturquoise":(72,209,204),
"darkturquoise":(0,206,209),
"cadetblue":(95,158,160),
"steelblue":(70,130,180),
"lightsteelblue":(176,196,222),
"powderblue":(176,224,230),
"lightblue":(173,216,230),
"skyblue":(135,206,235),
"lightskyblue":(135,206,250),
"deepskyblue":(0,191,255),
"dodgerblue":(30,144,255),
"cornflowerblue":(100,149,237),
"royalblue":(65,105,225),
"blue":(0,0,255),
"mediumblue":(0,0,205),
"darkblue":(0,0,139),
"navy":(0,0,128),
"midnightblue":(25,25,112),
"cornsilk":(255,248,220),
"blanchedalmond":(255,235,205),
"bisque":(255,228,196),
"navajowhite":(255,222,173),
"wheat":(245,222,179),
"burlywood":(222,184,135),
"tan":(210,180,140),
"rosybrown":(188,143,143),
"sandybrown":(244,164,96),
"goldenrod":(218,165,32),
"darkgoldenrod":(184,134,11),
"peru":(205,133,63),
"chocolate":(210,105,30),
"saddlebrown":(139,69,19),
"sienna":(160,82,45),
"brown":(165,42,42),
"maroon":(128,0,0),
"white":(255,255,255),
"snow":(255,250,250),
"honeydew":(240,255,240),
"mintcream":(245,255,250),
"azure":(240,255,255),
"aliceblue":(240,248,255),
"ghostwhite":(248,248,255),
"whitesmoke":(245,245,245),
"seashell":(255,245,238),
"beige":(245,245,220),
"oldlace":(253,245,230),
"floralwhite":(255,250,240),
"ivory":(255,255,240),
"antiquewhite":(250,235,215),
"linen":(250,240,230),
"lavenderblush":(255,240,245),
"mistyrose":(255,228,225),
"gainsboro":(220,220,220),
"lightgray":(211,211,211),
"lightgrey":(211,211,211),
"silver":(192,192,192),
"darkgray":(169,169,169),
"darkgrey":(169,169,169),
"gray":(128,128,128),
"grey":(128,128,128),
"dimgray":(105,105,105),
"dimgrey":(105,105,105),
"lightslategray":(119,136,153),
"lightslategrey":(119,136,153),
"slategray":(112,128,144),
"slategrey":(112,128,144),
"darkslategray":(47,79,79),
"darkslategrey":(47,79,79),
"black":(0,0,0),
}

class Color():

    def __init__(self, *args):
        global cssColors
        self.useRange = True
        self.allowHSL = True
        if len(args) == 1:
            if args[0] in cssColors:
                self.color = cssColors[args[0]]
                self.useRange = False
                self.allowHSL = False
            else:
                self.color = (args[0],)*3
            self.alpha = ()
            self.allowHSB = False
        elif len(args) == 2:
            if args[0] in cssColors:
                self.color = cssColors[args[0]]
                self.useRange = False
                self.allowHSL = False
            else:
                self.color = (args[0],) * 3
            self.alpha = (args[1],)
            self.allowHSB = False
        elif len(args) == 3:
            self.color = tuple(args)
            self.alpha = ()
        elif len(args) == 4:
            self.color = tuple(args[:3])
            self.alpha = (args[3],)
        else:
            raise ValueError("Color takes 1, 2, 3 or 4 arguments")

    def getRGB(self, mode=RGB, scale=1):
        if not self.useRange:
            scale = 256
        self.color = tuple(x / scale for x in self.color)
        self.alpha = tuple(x / scale for x in self.alpha)
        if mode == RGB or not self.allowHSL:
            return self.color + self.alpha
        else:
            h, s, l = self.color
            return colorsys.hls_to_rgb(h, l, s) + self.alpha

    def __str__(self):
        return str(self.color) + ' ' + str(self.alpha)


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

    def image(self, imagepath, x, y):
        ims = cairo.ImageSurface.create_from_png(imagepath)
        self.ctx.set_source_surface(ims, x, y)
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


