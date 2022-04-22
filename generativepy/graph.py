# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
import math
import numpy as np
import copy
from dataclasses import dataclass

from generativepy.geometry import Text, Shape, FillParameters, StrokeParameters, FontParameters
from generativepy.drawing import BUTT, FONT_WEIGHT_BOLD, FONT_SLANT_NORMAL
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
    subdivlines = StrokeParameters(Color(0.9, 0.9, 1), line_width=2, cap=BUTT)
    axislines = StrokeParameters(Color(0.2), line_width=2, cap=BUTT)
    featurescale = 1


class Axes:
    '''
    Controls the range and appearance of a set of Cartesian axes
    '''

    def __init__(self, ctx, position, width, height):
        self.ctx = ctx
        self.appearance = AxesAppearance()
        self.position = position
        self.width = width
        self.height = height
        self.start = (0, 0)
        self.extent = (10, 10)
        self.divisions = (1, 1)
        self.subdivisons = False
        self.subdivisionfactor = (1, 1)
        self.text_height = 0

    def of_start(self, start):
        '''
        Sets the start value of the axes
        :param start: (x, y) value of bottom left corner of axes
        :return: self
        '''
        self.start = start
        return self

    def of_extent(self, extent):
        '''
        Sets the range of the axes
        :param extent: (x, y) range of axes
        :return: self
        '''
        self.extent = extent
        return self

    def with_feature_scale(self, scale):
        '''
        Sets the scale of the features. For example a value of 2 will make all the gridlines and label text
        on the axes twice as big. This is a quick way of resizing everything in one go.
        :param scale: scale facor
        :return: self
        '''
        self.appearance.featurescale = scale
        return self

    def with_divisions(self, divisions):
        '''
        Set divisons spacing
        :param divisions: (x, y) spacing divisions in each direction
        :return: self
        '''
        self.divisions = divisions
        return self

    def with_subdivisions(self, factor):
        '''
        Draw subdivision lines on graph
        :param factor: (x, y) Number of subdivisions per division in each direction
        :return: self
        '''
        self.subdivisons = True
        self.subdivisionfactor = factor
        return self

    def background(self, pattern):
        '''
        Sets the entire graph background
        :param pattern: color or fill pattern
        :return: self
        '''
        self.appearance.background = FillParameters(pattern)
        return self

    def text_color(self, pattern):
        '''
        Sets the color of the axes text
        :param pattern: color or pattern
        :return: self
        '''
        self.appearance.textcolor = pattern
        return self

    def text_style(self, font="arial", weight=FONT_WEIGHT_BOLD, slant=FONT_SLANT_NORMAL, size=15):
        '''
        Set the style of the axis text
        :param font: Font name
        :param weight: Font weight
        :param slant: Font slant
        :param size: Font size in units. This will be multiplied by the featurescale value.
        :return:
        '''
        self.appearance.fontparams = FontParameters(font, weight, slant, size)
        return self

    def axis_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the axis lines
        :param pattern:  the fill pattern or color to use for the outline, None for default
        :param line_width: width of stroke line, None for default
        :param dash: dash patter of line, as for Pycairo, None for default
        :param cap: line end style, None for default
        :param join: line join style, None for default
        :param miter_limit: mitre limit, None for default
        :return: self
        '''
        self.appearance.axislines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def division_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the division lines
        :param pattern:  the fill pattern or color to use for the outline, None for default
        :param line_width: width of stroke line, None for default
        :param dash: dash patter of line, as for Pycairo, None for default
        :param cap: line end style, None for default
        :param join: line join style, None for default
        :param miter_limit: mitre limit, None for default
        :return: self
        '''
        self.appearance.divlines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def subdivision_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the subdivision lines
        :param pattern:  the fill pattern or color to use for the outline, None for default
        :param line_width: width of stroke line, None for default
        :param dash: dash patter of line, as for Pycairo, None for default
        :param cap: line end style, None for default
        :param join: line join style, None for default
        :param miter_limit: mitre limit, None for default
        :return: self
        '''
        self.appearance.subdivlines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def draw(self):
        '''
        Draw the axes
        :return:
        '''

        # Get the text height using the selected font. This is used to control text offset and other sizes.
        _, self.text_height = Text(self.ctx).of('0', (0, 0)) \
                                .font(self.appearance.fontparams.font,
                                      self.appearance.fontparams.weight,
                                      self.appearance.fontparams.slant) \
                                .size(self.appearance.fontparams.size * self.appearance.featurescale) \
                                .get_size()
        self.clip()
        self._draw_background()
        if self.subdivisons:
            self._draw_subdivlines()
        self._draw_divlines()
        self._draw_axes()
        self._draw_axes_values()
        self.unclip()

    def _draw_background(self):
        self.appearance.background.apply(self.ctx)
        self.ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        self.ctx.fill()

    def _draw_divlines(self):
        params = copy.copy(self.appearance.divlines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        for p in self._get_divs(self.start[0], self.extent[0], self.divisions[0]):
            self.ctx.move_to(*self.transform_from_graph((p, self.start[1])))
            self.ctx.line_to(*self.transform_from_graph((p, self.start[1] + self.extent[1])))
        for p in self._get_divs(self.start[1], self.extent[1], self.divisions[1]):
            self.ctx.move_to(*self.transform_from_graph((self.start[0], p)))
            self.ctx.line_to(*self.transform_from_graph((self.start[0] + self.extent[0], p)))
        self.ctx.stroke()

    def _draw_subdivlines(self):
        params = copy.copy(self.appearance.subdivlines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        for p in self._get_subdivs(self.start[0], self.extent[0], self.divisions[0], self.subdivisionfactor[0]):
            self.ctx.move_to(*self.transform_from_graph((p, self.start[1])))
            self.ctx.line_to(*self.transform_from_graph((p, self.start[1] + self.extent[1])))
        for p in self._get_subdivs(self.start[1], self.extent[1], self.divisions[1], self.subdivisionfactor[1]):
            self.ctx.move_to(*self.transform_from_graph((self.start[0], p)))
            self.ctx.line_to(*self.transform_from_graph((self.start[0] + self.extent[0], p)))
        self.ctx.stroke()

    def _draw_axes(self):
        params = copy.copy(self.appearance.axislines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        self.ctx.move_to(*self.transform_from_graph((0, self.start[1])))
        self.ctx.line_to(*self.transform_from_graph((0, self.start[1] + self.extent[1])))
        self.ctx.move_to(*self.transform_from_graph((self.start[0], 0)))
        self.ctx.line_to(*self.transform_from_graph((self.start[0] + self.extent[0], 0)))
        self.ctx.stroke()
        self.ctx.new_path()
        self.ctx.arc(*self.transform_from_graph((0, 0)), self.text_height/1.1, 0, 2 * math.pi)
        self.ctx.stroke()

    def _draw_axes_values(self):
        params = copy.copy(self.appearance.axislines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)

        xoffset = self.text_height/1.1
        yoffset = self.text_height/1.1
        for p in self._get_divs(self.start[0], self.extent[0], self.divisions[0]):
            if abs(p)>0.001:
                position = self.transform_from_graph((p, 0))
                pstr = self._format_div(p, self.divisions[0])
                Text(self.ctx).of(pstr, (position[0] - xoffset, position[1] + yoffset))\
                    .font(self.appearance.fontparams.font, self.appearance.fontparams.weight,
                          self.appearance.fontparams.slant)\
                    .size(self.appearance.fontparams.size*self.appearance.featurescale)\
                    .align(drawing.RIGHT, drawing.TOP).fill(self.appearance.textcolor)
                params.apply(self.ctx)
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
                    .size(self.appearance.fontparams.size*self.appearance.featurescale)\
                    .align(drawing.RIGHT, drawing.TOP).fill(self.appearance.textcolor)
                params.apply(self.ctx)
                self.ctx.new_path()
                self.ctx.move_to(position[0], position[1])
                self.ctx.line_to(position[0] - xoffset, position[1])
                self.ctx.stroke()

    def clip(self):
        '''
        Set the clip region to the axes area.
        :return:
        '''
        self.ctx.rectangle(*self.position, self.width, self.height)
        self.ctx.save()
        self.ctx.clip()

    def unclip(self):
        '''
        Undo a previous clip()
        :return:
        '''
        self.ctx.restore()

    def _get_divs(self, start, extent, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= start + extent:
            divs.append(n)
            n += div
        return divs

    def _contains(self, values, value, tolerance):
        '''
        Return true if the sequence values contains the value to within a given tolerance
        :param values:
        :param value:
        :param tolerance:
        :return:
        '''
        for v in values:
            if abs(value - v) < tolerance:
                return True
        return False

    def _get_subdivs(self, start, extent, div, factor):
        subdiv = div/factor
        divs = self._get_divs(start, extent, div)
        subdivs = []
        n = math.ceil(start/subdiv)*subdiv
        while n <= start + extent:
            if not self._contains(divs, subdiv, extent/100000):
                subdivs.append(n)
            n += subdiv
        return subdivs

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
    '''
    Plot a function in a set of axes.
    '''

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

    def stroke(self, pattern=None, line_width=2, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Stroke overrides the Shape stroke() method. It clips the stroke to the area of the axes. This ensures that if
        the curve goes out of range it will not interfere with other parts of the image.
        :param pattern:
        :param line_width:
        :param dash:
        :param cap:
        :param join:
        :param miter_limit:
        :return:
        '''
        super().stroke(pattern, line_width, dash, cap, join, miter_limit)


    def of_function(self, fn, extent=None, precision=100):
        '''
        Plot a function y = fn(x)
        :param fn: the function to plot. It must take a single argument
        :param extent: the range of x values to plot. If not supplied, the plot will use the full range of the axes.
        :param precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
        :return:
        '''
        self.points = []
        for x in np.linspace(self.axes.start[0], self.axes.start[0] + self.axes.extent[0], precision):
            if not extent or extent[0] <= x <= extent[1]:
                self.points.append(self.axes.transform_from_graph((x, fn(x))))
        return self

    def of_xy_function(self, fn, extent=None, precision=100):
        '''
        Plot a function x = fn(y)
        :param fn: the function to plot. It must take a single argument
        :param extent: the range of y values to plot. If not supplied, the plot will use the full range of the axes.
        :param precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
        :return:
        '''
        self.points = []
        for y in np.linspace(self.axes.start[1], self.axes.start[1] + self.axes.extent[1], precision):
            if not extent or extent[0] <= y <= extent[1]:
                self.points.append(self.axes.transform_from_graph((fn(y), y)))
        return self

    def of_polar_function(self, fn, extent=(0, 2*math.pi), precision=100):
        '''
        Plot a polar function r = fn(theta). theta is measured in radians
        :param fn: the function to plot. It must take a single argument
        :param extent: the range of theta values to plot. If not supplied, the plot will use the range 0 to 2*pi.
        :param precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
        :return:
        '''
        self.points = []
        for theta in np.linspace(extent[0], extent[1], precision):
            r = fn(theta)
            self.points.append(self.axes.transform_from_graph((r*math.cos(theta), r*math.sin(theta))))
        return self

