# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
import cairo

from generativepy.drawing import LEFT, BASELINE, CENTER, RIGHT, BOTTOM, TOP


class Shape():

    def __init__(self, ctx):
        self.ctx = ctx

    def add(self):
        raise NotImplementedError()

    def fill(self, color=None):
        self.ctx.new_path()
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
        self.ctx.fill()
        return self

    def stroke(self, color=None, line_width=1):
        self.ctx.new_path()
        self.add()
        if color:
            self.ctx.set_source_rgba(*color)
            self.ctx.set_line_width(line_width)
        self.ctx.stroke()
        return self

    def fill_stroke(self, fill_color, stroke_colour, line_width=1):
        self.ctx.new_path()
        self.add()
        self.ctx.set_source_rgba(*fill_color)
        self.ctx.fill_preserve()
        self.ctx.set_source_rgba(*stroke_colour)
        self.ctx.set_line_width(line_width)
        self.ctx.stroke()
        return self

class Rectangle(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def add(self):
        self.ctx.rectangle(self.x, self.y, self.width, self.height)
        return self

    def of_corner_size(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        return self


def rectangle(ctx, x, y, width, height):
    Rectangle(ctx).of_corner_size(x, y, width, height).add()

# TODO create Text object
def text(ctx, txt, x, y, font=None, size=None, color=None, alignx=LEFT, aligny=BASELINE, flip=False):
    '''
    Draw text using ths supplied ctx
    :param ctx: The context
    :param txt: The text, string
    :param x: x position
    :param y: y position
    :param font: font name, string
    :param size: text size
    :param color: text colour, Color
    :param alignx: x alignment
    :param aligny: y alignemen
    :param flip: True to flip the text (for maths drawing)
    :return:
    '''
    if font:
        ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                              cairo.FONT_WEIGHT_BOLD)
    if size:
        ctx.set_font_size(size)

    if color:
        ctx.set_source_rgba(*color)

    xb, yb, width, height, dx, dy = ctx.text_extents(txt)

    x -= xb
    if alignx == CENTER:
        x -= width / 2
    elif alignx == RIGHT:
        x -= width

    if aligny == CENTER:
        dy = -yb / 2
    elif aligny == BOTTOM:
        dy = -(yb + height)
    elif aligny == TOP:
        dy = -yb

    if flip:
        ctx.move_to(x, y - dy)
        ctx.save()
        ctx.scale(1, -1)
        ctx.show_text(txt)
        ctx.restore()
    else:
        ctx.move_to(x, y + dy)
        ctx.show_text(txt)


# TODO create Polygon object
def polygon(ctx, points, close=True):
    '''
    Create a polygon in ths ctx
    :param ctx:
    :param points:
    :param close:
    :return:
    '''
    first = True
    for p in points:
        if first:
            ctx.move_to(*p)
            first = False
        else:
            ctx.line_to(*p)
    if close:
        ctx.close_path()