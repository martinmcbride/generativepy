# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
import cairo
import math
from generativepy.drawing import LEFT, CENTER, RIGHT, BOTTOM, MIDDLE, BASELINE, TOP
from generativepy.drawing import EVEN_ODD, WINDING
from generativepy.drawing import MITER, ROUND, BEVEL, BUTT, SQUARE
from generativepy.color import Color


class Shape():

    def __init__(self, ctx):
        self.ctx = ctx
        self.extend = False
        self.sub_path = False
        self.final_close = False
        self.added = False

    def extend_path(self, close=False):
        self.sub_path = True
        self.extend = True
        self.final_close = close
        return self

    def as_sub_path(self):
        self.sub_path = True
        return self

    def _do_path_(self):
        if not self.sub_path:
            self.ctx.new_path()

    def add(self):
        raise NotImplementedError()

    def fill(self, color=Color(0), fill_rule=WINDING):
        if not self.added:
            self.add()
            self.added = True
        self.ctx.set_source_rgba(*color)

        if fill_rule == WINDING:
            self.ctx.set_fill_rule(cairo.FillRule.WINDING)
        else:
            self.ctx.set_fill_rule(cairo.FillRule.EVEN_ODD)

        self.ctx.fill_preserve()
        return self

    def stroke(self, color=Color(0), line_width=1, dash=[], cap=SQUARE, join=MITER, miter_limit=None):
        if not self.added:
            self.add()
            self.added = True

        self.ctx.set_source_rgba(*color)

        self.ctx.set_line_width(line_width)

        self.ctx.set_dash(dash)

        if cap == ROUND:
            self.ctx.set_line_cap(cairo.LineCap.ROUND)
        elif cap == BUTT:
            self.ctx.set_line_cap(cairo.LineCap.BUTT)
        else:
            self.ctx.set_line_cap(cairo.LineCap.SQUARE)

        if join == ROUND:
            self.ctx.set_line_join(cairo.LineJoin.ROUND)
        elif join == BEVEL:
            self.ctx.set_line_join(cairo.LineJoin.BEVEL)
        else:
            self.ctx.set_line_join(cairo.LineJoin.MITER)

        if miter_limit != None:
            self.ctx.set_miter_limit(miter_limit)

        self.ctx.stroke_preserve()
        return self

    def fill_stroke(self, fill_color, stroke_colour, line_width=1):
        self.fill(fill_color)
        self.stroke(stroke_color, line_width)
        return self

    def clip(self):
        if not self.added:
            self.add()
            self.added = True
        return self.ctx.clip_preserve()

    def path(self):
        if not self.added:
            self.add()
            self.added = True
        return self.ctx.copy_path_flat()


class Path(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.path = None
        self.height = 0

    def add(self):
        self._do_path_()
        if self.path:
            self.ctx.append_path(self.path)
        return self

    def of(self, path):
        self.path = path
        return self


class Rectangle(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def add(self):
        self._do_path_()
        self.ctx.rectangle(self.x, self.y, self.width, self.height)
        return self

    def of_corner_size(self, corner, width, height):
        self.x = corner[0]
        self.y = corner[1]
        self.width = width
        self.height = height
        return self


def rectangle(ctx, corner, width, height):
    Rectangle(ctx).of_corner_size(corner, width, height).add()


class Square(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.x = 0
        self.y = 0
        self.width = 0

    def add(self):
        self._do_path_()
        self.ctx.rectangle(self.x, self.y, self.width, self.width)
        return self

    def of_corner_size(self, corner, width):
        self.x = corner[0]
        self.y = corner[1]
        self.width = width
        return self


def square(ctx, corner, width):
    Square(ctx).of_corner_size(corner, width).add()


class Triangle(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.a = (0, 0)
        self.b = (0, 0)
        self.c = (0, 0)

    def add(self):
        self._do_path_()
        self.ctx.move_to(*self.a)
        self.ctx.line_to(*self.b)
        self.ctx.line_to(*self.c)
        self.ctx.close_path()
        return self

    def of_corners(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        return self


def triangle(ctx, a, b, c):
    Triangle(ctx).of_corners(a, b, c).add()


class Text(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.text = 'text'
        self.position = (0, 0)
        self._size = None
        self._font = None
        self.alignx = LEFT
        self.aligny = BASELINE
        self._flip = False
        self._offset = (0, 0)

    def add(self):
        self._do_path_()
        if self._font:
            self.ctx.select_font_face(self._font, cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)
        if self._size:
            self.ctx.set_font_size(self._size)

        x, y = self.position
        x += self._offset[0]
        y += self._offset[1]
        xb, yb, width, height, dx, dy = self.ctx.text_extents(self.text)

        x -= xb
        if self.alignx == CENTER:
            x -= width / 2
        elif self.alignx == RIGHT:
            x -= width

        if self.aligny == CENTER:
            dy = -yb / 2
        elif self.aligny == BOTTOM:
            dy = -(yb + height)
        elif self.aligny == TOP:
            dy = -yb

        if self._flip:
            self.ctx.move_to(x, y - dy)
            self.ctx.save()
            self.ctx.scale(1, -1)
            self.ctx.text_path(self.text)
            self.ctx.restore()
        else:
            self.ctx.move_to(x, y + dy)
            self.ctx.text_path(self.text)
        return self

    def of(self, text, position):
        self.text = text
        self.position = position
        return self

    def font(self, font):
        self._font = font
        return self

    def size(self, size):
        self._size = size
        return self

    def align(self, alignx, aligny):
        self.alignx = alignx
        self.aligny = aligny
        return self

    def align_left(self):
        self.alignx = LEFT
        return self

    def align_center(self):
        self.alignx = CENTER
        return self

    def align_right(self):
        self.alignx = RIGHT
        return self

    def align_right(self):
        self.alignx = RIGHT
        return self

    def align_bottom(self):
        self.aligny = BOTTOM
        return self

    def align_baseline(self):
        self.aligny = BASELINE
        return self

    def align_middle(self):
        self.aligny = MIDDLE
        return self

    def align_top(self):
        self.aligny = TOP
        return self

    def flip(self):
        self._flip = True
        return self

    def offset(self, x=0, y=0):
        self._offset = (x, y)
        return self



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

    shape = Text(ctx).of(txt, (x, y)).align(alignx, aligny)
    if font:
        shape = shape.font(font)
    if size:
        shape = shape.flip()
    if flip:
        shape = shape.flip()

    if color:
        ctx.set_source_rgba(*color)

    shape.add()
    ctx.fill()


class Line(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.start = (0, 0)
        self.end = (0, 0)

    def add(self):
        self._do_path_()
        if not self.extend:
            self.ctx.move_to(*self.start)
        self.ctx.line_to(*self.end)
        if self.final_close:
            self.ctx.close_path()
        return self

    def of_start_end(self, start, end):
        self.start = start
        self.end = end
        return self

    def of_end(self, end):
        self.start = (0, 0)
        self.end = end
        return self


def line(ctx, start, end):
    '''
    Create a line segment in the ctx
    :param ctx:
    :param start: start point
    :param end: end point
    :return:
    '''
    Line(ctx).of_start_end(start, end).add()


class Bezier(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.a = (0, 0)
        self.b = (0, 0)
        self.c = (0, 0)
        self.d = (0, 0)

    def add(self):
        self._do_path_()
        if not self.extend:
            self.ctx.move_to(*self.a)
        self.ctx.curve_to(*self.b, *self.c, *self.d)
        if self.final_close:
            self.ctx.close_path()
        return self

    def of_abcd(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        return self

    def of_bcd(self, b, c, d):
        self.a = (0, 0)
        self.b = b
        self.c = c
        self.d = d
        return self


class Polygon(Shape):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.points = []
        self.closed = True

    def add(self):
        self._do_path_()
        first = True
        for p in self.points:
            if first:
                if not self.extend:
                    self.ctx.move_to(*p)
                first = False
            else:
                if len(p) == 6:
                    self.ctx.curve_to(*p)
                else:
                    self.ctx.line_to(*p)
        if self.closed or self.final_close:
            self.ctx.close_path()
        return self

    def of_points(self, points):
        self.points = points
        return self

    def open(self):
        self.closed = False
        return self


def polygon(ctx, points, closed=True):
    '''
    Create a polygon in ths ctx
    :param ctx:
    :param points:
    :param closed:
    :return:
    '''
    shape = Polygon(ctx).of_points(points)
    if not closed:
        shape.open()
    shape.add()


class Circle(Shape):

    arc = 1
    sector = 2
    segment = 3

    def __init__(self, ctx):
        super().__init__(ctx)
        self.center = (0, 0)
        self.radius = 0
        self.start_angle = 0
        self.end_angle = 2*math.pi
        self.type = Circle.arc

    def add(self):
        self._do_path_()
        if self.type == Circle.sector:
            self.ctx.move_to(*self.center)
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
            self.ctx.close_path()
        elif self.type == Circle.segment:
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
            self.ctx.close_path()
        else:
            self.ctx.arc(*self.center, self.radius, self.start_angle, self.end_angle)
            if self.final_close:
                self.ctx.close_path()
        return self

    def of_center_radius(self, center, radius):
        self.center = center
        self.radius = radius
        return self

    def as_arc(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.arc
        return self

    def as_sector(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.sector
        return self

    def as_segment(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.segment
        return self

def circle(ctx, center, radius):
    '''
    Create a circle in ths ctx
    :param ctx:
    :param center:
    :param radius:
    :return:
    '''
    Circle(ctx).of_center_radius(center, radius).add()


class Ellipse(Shape):

    arc = 1
    sector = 2
    segment = 3

    def __init__(self, ctx):
        super().__init__(ctx)
        self.center = (0, 0)
        self.radius_x = 0
        self.radius_y = 0
        self.start_angle = 0
        self.end_angle = 2*math.pi
        self.type = Circle.arc

    def add(self):
        self._do_path_()
        scale_factor = self.radius_y/self.radius_x
        self.ctx.save()
        self.ctx.translate(*self.center)
        self.ctx.scale(1, scale_factor)
        if self.type == Circle.sector:
            self.ctx.move_to(0, 0)
            self.ctx.arc(0, 0, self.radius_x, self.start_angle, self.end_angle)
            self.ctx.close_path()
        elif self.type == Circle.segment:
            self.ctx.arc(0, 0, self.radius_x, self.start_angle, self.end_angle)
            self.ctx.close_path()
        else:
            self.ctx.arc(0, 0, self.radius_x, self.start_angle, self.end_angle)
            if self.final_close:
                self.ctx.close_path()
        self.ctx.restore()
        return self

    def of_center_radius(self, center, radius_x, radius_y):
        self.center = center
        self.radius_x = radius_x
        self.radius_y = radius_y
        return self

    def as_arc(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.arc
        return self

    def as_sector(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.sector
        return self

    def as_segment(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.segment
        return self

def ellipse(ctx, center, radius_x, radius_y):
    '''
    Create a circle in ths ctx
    :param ctx:
    :param center:
    :param radius:
    :return:
    '''
    Ellipse(ctx).of_center_radius(center, radius_x, radius_y).add()


def angle_marker(ctx, a, b, c, count=1, radius=8, gap=2, right_angle=False):
    '''
    Draw an angle marker
    :param ctx: Context
    :param a:
    :param b:
    :param c:
    :param count:
    :param radius:
    :param gap:
    :param rightangle:
    :return:
    '''
    ang1 = math.atan2(a[1] - b[1], a[0] - b[0])
    ang2 = math.atan2(c[1] - b[1], c[0] - b[0])
    ctx.new_path()
    if right_angle:
        radius /= 2
        v = (math.cos(ang1), math.sin(ang1));
        pv = (math.cos(ang2), math.sin(ang2));
        polygon(ctx, [(b[0] + v[0] * radius, b[1] + v[1] * radius),
                      (b[0] + (v[0] + pv[0])*radius, b[1] + (v[1]+pv[1])*radius),
                      (b[0] + pv[0]*radius, b[1] + pv[1]*radius)], False)
    elif count==2:
        ctx.arc(b[0], b[1], radius - gap / 2, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius + gap / 2, ang1, ang2)
    elif count == 3:
        ctx.arc(b[0], b[1], radius - gap, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius, ang1, ang2)
        ctx.new_sub_path()
        ctx.arc(b[0], b[1], radius + gap, ang1, ang2)
    else:
        ctx.arc(b[0], b[1], radius, ang1, ang2)

def tick(ctx, a, b, count=1, length=4, gap=1):

    def do_line(ctx, a, b):
        ctx.move_to(*a)
        ctx.line_to(*b)

    # Midpoint of line
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    ctx.new_path()
    if count==1:
        pos = (pmid[0], pmid[1])
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2),
             (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2),
             (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0], pmid[1])
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        do_line(ctx, (pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2), (pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2))

def paratick(ctx, a, b, count=1, length=4, gap=1):

    def draw(x, y, ox1, oy1, ox2, oy2):
        ctx.move_to(x, y)
        ctx.line_to(x + ox1, y + oy1)
        ctx.move_to(x, y)
        ctx.line_to(x + ox2, y + oy2)

    # Midpoint ofgline
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    ctx.new_path()
    if count==1:
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)

def arrowhead(ctx, a, b, length=4):

    def draw(x, y, ox1, oy1, ox2, oy2):
        ctx.move_to(x + ox1, y + oy1)
        ctx.line_to(x, y)
        ctx.line_to(x + ox2, y + oy2)

    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    ctx.new_path()
    draw(b[0], b[1], (-vector[0] + pvector[0]) * length / 2, (-vector[1] + pvector[1]) * length / 2,
         (-vector[0] - pvector[0]) * length / 2, (-vector[1] - pvector[1]) * length / 2)
