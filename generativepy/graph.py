# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
import numpy as np
from generativepy.color import Color
from generativepy import drawing


class Axes:
    def __init__(self, ctx, start=(0, 0), extent=(10, 10), divisions=(1, 1)):
        self.ctx = ctx
        self.start = start
        self.extent = extent
        self.divisions = divisions


    def draw(self):
        self.ctx.set_line_width(self.pts2pixels(0.5))
        self.ctx.set_source_rgba(*Color(0.8, 0.8, 1))
        for p in self.get_divs(self.start[0], self.extent[0], self.divisions[0]):
            self.ctx.move_to(p, self.start[1])
            self.ctx.line_to(p, self.start[1] + self.extent[1])
        for p in self.get_divs(self.start[1], self.extent[1], self.divisions[1]):
            self.ctx.move_to(self.start[0], p)
            self.ctx.line_to(self.start[0]+self.extent[0], p)
        self.ctx.stroke()

        self.ctx.set_source_rgba(*Color(0.2, 0.2, 0.2))
        self.ctx.set_font_size(self.pts2pixels(3.5))
        self.ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

        xoffset = self.pts2pixels(1)
        yoffset = self.pts2pixels(1)
        for p in self.get_divs(self.start[0], self.extent[0], self.divisions[0]):
           if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[0])
                drawing.text(self.ctx, pstr, p - xoffset, -yoffset, alignx=drawing.RIGHT, aligny=drawing.TOP, flip=True)

        xoffset = self.pts2pixels(1)
        yoffset = self.pts2pixels(1)
        for p in self.get_divs(self.start[1], self.extent[1], self.divisions[1]):
           if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[0])
                drawing.text(self.ctx, pstr, -xoffset, p - yoffset, alignx=drawing.RIGHT, aligny=drawing.TOP, flip=True)

        self.ctx.set_line_width(self.pts2pixels(0.5))
        self.ctx.new_path()
        self.ctx.arc(0, 0, self.pts2pixels(2), 0, 2 * math.pi)
        self.ctx.stroke()

    def clip(self):
        self.ctx.move_to(self.start[0], self.start[1])
        self.ctx.line_to(self.start[0]+self.extent[0], self.start[1])
        self.ctx.line_to(self.start[0]+self.extent[0], self.start[1]+self.extent[1])
        self.ctx.line_to(self.start[0], self.start[1]+self.extent[1])
        self.ctx.close_path()
        self.ctx.save()
        self.ctx.clip()

    def unclip(self):
        self.ctx.restore()

    def get_divs(self, start, extent, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= start + extent:
            divs.append(n)
            n += div
        return divs

    def format_div(self, value, div):
        """
        Formats a division value into a string.
        If the division spacing is an integer, the string will be an integer (no dp).
        If the division spacing is float, the string will be a float with a suitable number of decimal places
        :param value: value to be formatted
        :param div: division spacing
        :return: string representation of the value
        """
        if isinstance(value, int):
            return str(value)
        return str(round(value*1000)/1000)

    def pts2pixels(self, points):
        return points/10


def plot_curve(axes, fn, line_color=Color(1, 0, 0), extent=None, line_width=.7):
    """
    Plot a curve y = fn(x)
    :param axes: Axes to plt in
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line, Color
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the x range
    :param line_width: line width in page space
    :return:
    """
    ctx = axes.ctx
    points = []
    for x in np.linspace(axes.start[0], axes.start[0]+axes.extent[0], 100):
        if not extent or extent[0] <= x <= extent[1]:
            points.append((x, fn(x)))
    if points:
        ctx.new_path()
        axes.clip()
        ctx.set_line_width(axes.pts2pixels(line_width))
        ctx.set_source_rgba(*line_color)

        drawing.polygon(ctx, points, False)
        ctx.stroke()
        axes.unclip()

def plot_xy_curve(axes, fn, line_color=Color(1, 0, 0), extent=None, line_width=.7):
    """
    Plot a curve x = fn(y)
    :param axes: Axes to plt in
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line, Color
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
    :param line_width: line width in page space
    :return:
    """
    ctx = axes.ctx
    points = []
    for y in np.linspace(axes.start[1], axes.start[1]+axes.extent[1], 100):
        if not extent or extent[0] <= y <= extent[1]:
            points.append((fn(y), y))
    if points:
        ctx.new_path()
        axes.clip()
        ctx.set_line_width(axes.pts2pixels(line_width))
        ctx.set_source_rgba(*line_color)

        drawing.polygon(ctx, points, False)
        ctx.stroke()
        axes.unclip()

def plot_polar_curve(axes, fn, line_color=Color(1, 0, 0), extent=(0, 2*math.pi), line_width=.7):
    """
    Plot a curve x = fn(y)
    :param axes: Axes to plt in
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line, Color
    :param extent: tuple (start, end) giving angular extent of curve, default 0 to 2*pi
    :param line_width: line width in page space
    :return:
    """
    ctx = axes.ctx
    points = []
    for theta in np.linspace(extent[0], extent[1], 100):
        r = fn(theta)
        points.append((r*math.cos(theta), r*math.sin(theta)))
    if points:
        ctx.new_path()
        axes.clip()
        ctx.set_line_width(axes.pts2pixels(line_width))
        ctx.set_source_rgba(*line_color)

        drawing.polygon(ctx, points, False)
        ctx.stroke()
        axes.unclip()

#
# 
# def plotYXCurve(axes, fn, lineColor=Color(1, 0, 0), extent=None, line_width=.7):
#     """
#     Plot an x = fn(y)
#     :param mctx: maths context
#     :param fn: the function, a function object taking 1 number and returning a number
#     :param lineColor: color of line (r, g, b) each channel in range 0.0 to 1.0
#     :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
#     :param line_width: line width in page space
#     :return:
#     """
#     canvas = axes.canvas
#     points = []
#     for y in np.linspace(axes.start[1], axes.start[1]+axes.extent[1], 100):
#         if not extent or extent[0] <= y <= extent[1]:
#             points.append((fn(y), y))
#     if points:
#         axes.clip()
#         canvas.stroke(lineColor)
#         canvas.noFill()
#         canvas.strokeWeight(canvas.page2user(line_width))
#         canvas.polygon(points, False)
#         axes.unclip()
# 
# 
# def plotPolarCurve(axes, fn, lineColor=drawing.Color(1, 0, 0), extent=(0, 2*math.pi), line_width=.7):
#     """
#     Plot an r = fn(theta)
#     :param mctx: maths context
#     :param fn: the function, a function object taking 1 number and returning a number
#     :param lineColor: color of line (r, g, b) each channel in range 0.0 to 1.0
#     :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
#     :param line_width: line width in page space
#     :return:
#     """
#     canvas = axes.canvas
#     points = []
#     for theta in np.linspace(range[0], range[1], 100):
#         if not extent or extent[0] <= theta <= extent[1]:
#             r = fn(theta)
#             points.append((r*math.cos(theta), r*math.sin(theta)))
#     if points:
#         axes.clip()
#         canvas.stroke(lineColor)
#         canvas.noFill()
#         canvas.strokeWeight(canvas.page2user(line_width))
#         canvas.polygon(points, False)
#         axes.unclip()
