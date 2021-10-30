# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
import numpy as np
from dataclasses import dataclass

from generativepy.geometry import Text, Shape, FillParameters, StrokeParameters, FontParameters
from generativepy.drawing import BUTT, FONT_WEIGHT_BOLD
from generativepy.color import Color
from generativepy import drawing

@dataclass
class AxesAppearance:
    '''
    Parameters that control the appearance of the axes (colours, line styles).
    '''
    background = FillParameters(Color(1))
    textcolor = Color(0.2)
    fontparams = FontParameters('arial', size=15, weight=FONT_WEIGHT_BOLD)
    divlines = StrokeParameters(Color(0.8, 0.8, 1), line_width=2, cap=BUTT)
    axislines = StrokeParameters(Color(0.2), line_width=2, cap=BUTT)


class Axes:
    def __init__(self, ctx, position, width, height):
        self.ctx = ctx
        self.appearance = AxesAppearance()
        self.position = position
        self.width = width
        self.height = height
        self.start = (0, 0)
        self.extent = (10, 10)
        self.divisions = (1, 1)

    def of_start(self, start):
        self.start = start
        return self

    def of_extent(self, extent):
        self.extent = extent
        return self

    def draw(self):
        self.clip()
        self._draw_background()
        self._draw_divlines()
        self._draw_axes()
        self._draw_axes_values()
        self.unclip()

    def _draw_background(self):
        self.appearance.background.apply(self.ctx)
        self.ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        self.ctx.fill()

    def _draw_divlines(self):
        self.appearance.divlines.apply(self.ctx)
        for p in self._get_divs(self.start[0], self.extent[0], self.divisions[0]):
            self.ctx.move_to(*self.transform_from_graph((p, self.start[1])))
            self.ctx.line_to(*self.transform_from_graph((p, self.start[1] + self.extent[1])))
        for p in self._get_divs(self.start[1], self.extent[1], self.divisions[1]):
            self.ctx.move_to(*self.transform_from_graph((self.start[0], p)))
            self.ctx.line_to(*self.transform_from_graph((self.start[0] + self.extent[0], p)))
        self.ctx.stroke()

    def _draw_axes(self):
        self.appearance.axislines.apply(self.ctx)
        self.ctx.move_to(*self.transform_from_graph((0, self.start[1])))
        self.ctx.line_to(*self.transform_from_graph((0, self.start[1] + self.extent[1])))
        self.ctx.move_to(*self.transform_from_graph((self.start[0], 0)))
        self.ctx.line_to(*self.transform_from_graph((self.start[0] + self.extent[0], 0)))
        self.ctx.stroke()
        self.ctx.new_path()
        self.ctx.arc(*self.transform_from_graph((0, 0)), 10, 0, 2 * math.pi)
        self.ctx.stroke()

    def _draw_axes_values(self):
        self.appearance.axislines.apply(self.ctx)

        xoffset = 10
        yoffset = 10
        for p in self._get_divs(self.start[0], self.extent[0], self.divisions[0]):
            if abs(p)>0.001:
                position = self.transform_from_graph((p, 0))
                pstr = self._format_div(p, self.divisions[0])
                Text(self.ctx).of(pstr, (position[0] - xoffset, position[1] + yoffset))\
                    .font(self.appearance.fontparams.font, self.appearance.fontparams.weight,
                          self.appearance.fontparams.slant)\
                    .size(self.appearance.fontparams.size).align(drawing.RIGHT, drawing.TOP).fill(self.appearance.textcolor)
                self.ctx.new_path()
                self.ctx.move_to(position[0], position[1])
                self.ctx.line_to(position[0], position[1] + yoffset)
                self.ctx.stroke()

        for p in self._get_divs(self.start[1], self.extent[1], self.divisions[1]):
            if abs(p)>0.001:
                position = self.transform_from_graph((0, p))
                pstr = self._format_div(p, self.divisions[1])
                Text(self.ctx).of(pstr, (position[0] - xoffset, position[1] + yoffset))\
                    .font(self.appearance.fontparams.font, self.appearance.fontparams.weight,
                          self.appearance.fontparams.slant)\
                    .size(self.appearance.fontparams.size).align(drawing.RIGHT, drawing.TOP).fill(self.appearance.textcolor)
                self.ctx.new_path()
                self.ctx.move_to(position[0], position[1])
                self.ctx.line_to(position[0] - xoffset, position[1])
                self.ctx.stroke()

    def clip(self):
        self.ctx.rectangle(*self.position, self.width, self.height)
        self.ctx.save()
        self.ctx.clip()

    def unclip(self):
        self.ctx.restore()

    def _get_divs(self, start, extent, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= start + extent:
            divs.append(n)
            n += div
        return divs

    def _format_div(self, value, div):
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

    def transform_from_graph(self, point):
        '''
        Scale the ctx so that point (x, y) will be correctly positioned in the axes coordinates
        :return:
        '''
        x = ((point[0] - self.start[0]) * self.width / self.extent[0]) + self.position[0]
        y = self.height + self.position[1] - ((point[1] - self.start[1]) * self.height / self.extent[1])
        return x, y


class Plot(Shape):

    def __init__(self, axes):
        super().__init__(axes.ctx)
        self.axes = axes
        self.points = []

    def add(self):
        self._do_path_()
        first = True
        for p in self.points:
            if first:
                if not self.extend:
                    self.ctx.move_to(*p)
                first = False
            else:
                self.ctx.line_to(*p)
        if self.final_close:
            self.ctx.close_path()
        return self

    def stroke(self, color=None, line_width=2, dash=None, cap=None, join=None, miter_limit=None):
        self.axes.clip()
        super().stroke(color, line_width, dash, cap, join, miter_limit)
        self.axes.unclip()


    def of_function(self, fn, extent=None, precision=100):
        self.points = []
        for x in np.linspace(self.axes.start[0], self.axes.start[0] + self.axes.extent[0], precision):
            if not extent or extent[0] <= x <= extent[1]:
                self.points.append(self.axes.transform_from_graph((x, fn(x))))
        return self

    def of_xy_function(self, fn, extent=None, precision=100):
        self.points = []
        for y in np.linspace(self.axes.start[1], self.axes.start[1] + self.axes.extent[1], precision):
            if not extent or extent[0] <= y <= extent[1]:
                self.points.append(self.axes.transform_from_graph((fn(y), y)))
        return self

    def of_polar_function(self, fn, extent=(0, 2*math.pi), precision=100):
        self.points = []
        for theta in np.linspace(extent[0], extent[1], precision):
            r = fn(theta)
            self.points.append(self.axes.transform_from_graph((r*math.cos(theta), r*math.sin(theta))))
        return self

