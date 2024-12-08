# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT
import dataclasses
import itertools

import cairo
import math
import numpy as np
import copy
from dataclasses import dataclass

from generativepy.geometry import Text, Shape, FillParameters, StrokeParameters, FontParameters, Circle, Polygon, Line
from generativepy.drawing import BUTT, FONT_WEIGHT_BOLD, FONT_SLANT_NORMAL, WINDING, SQUARE, MITER
from generativepy.color import Color
from generativepy import drawing
from generativepy.math import Vector as V

# Point styles for graphs
POINT_CIRCLE = 0  # Circular points

# Point styles for graphs
SCATTER_NO_LINE = 0  # All points on scatter chart are left unconnected
SCATTER_STALK = 1  # Stalk chart style
SCATTER_CONNECTED = 2  # Points are joined one to the next

# Axis positions
AXIS_NONE = 0
AXIS_ZERO = 1
AXIS_MIN = 2
AXIS_MAX = 3

@dataclass
class AxesAppearance:
    '''
    Parameters that control the appearance and  position of the axes (colours, line styles).
    '''
    background: any = dataclasses.field(default_factory=lambda: FillParameters(Color(1)))
    textcolor: any = Color(0.2)
    fontparams: any = dataclasses.field(default_factory=lambda: FontParameters('arial', size=15, weight=FONT_WEIGHT_BOLD))
    divlines: any = dataclasses.field(default_factory=lambda: StrokeParameters(Color(0.8, 0.8, 1), line_width=2, cap=BUTT))
    subdivlines: any = dataclasses.field(default_factory=lambda: StrokeParameters(Color(0.9, 0.9, 1), line_width=2, cap=BUTT))
    axislines: any = dataclasses.field(default_factory=lambda: StrokeParameters(Color(0.2), line_width=2, cap=BUTT))
    featurescale: any = 1
    divisions: any = (1, 1)
    subdivisions: any = False
    subdivisionfactor: any = (1, 1)
    text_height: any = 0
    x_div_formatter: any = None
    y_div_formatter: any = None
    start: any = (0, 0)
    extent: any = (10, 10)
    border: any = False
    x_axis_pos: int = AXIS_ZERO
    y_axis_pos: int = AXIS_ZERO

    # x and y offset of tick labels. The actual offset is:
    # text height (height of 0 character using fontparams) DIVIDED by ticklabeloffset
    ticklabeloffset: any = 1.1


class Axes:
    '''
    Controls the range and appearance of a set of Cartesian axes
    '''

    def __init__(self, ctx, position, width, height, appearance=None):

        self.ctx = ctx
        self.position = position
        self.width = width
        self.height = height
        self.appearance = dataclasses.replace(appearance) if appearance is not None else AxesAppearance()

    def of_start(self, start):
        '''
        Sets the start value of the axes

        Args:
            start: (x, y) value of bottom left corner of axes

        Returns:
            self
        '''
        self.appearance.start = start
        return self

    def of_extent(self, extent):
        '''
        Sets the range of the axes

        Args:
            extent: (x, y) range of axes

        Returns:
            self
        '''
        self.appearance.extent = extent
        return self

    def with_feature_scale(self, scale):
        '''
        Sets the scale of the features. For example a value of 2 will make all the gridlines and label text
        on the axes twice as big. This is a quick way of resizing everything in one go.

        Args:
            scale: scale factor

        Returns:
            self
        '''
        self.appearance.featurescale = scale
        return self

    def with_divisions(self, divisions):
        '''
        Set divisions spacing

        Args:
            divisions: (x, y) spacing divisions in each direction

        Returns:
            self
        '''
        self.appearance.divisions = divisions
        return self

    def with_axis_positions(self, x_axis_pos, y_axis_pos):
        '''
        Set axis positions

        x and y axes can be individually positioned at zero, at the minimum edge, at the maximum edge, or not shows at all

        Args:
            x_axis_pos: Position of x axis
            y_axis_pos: Position of y axis

        Returns:
            self
        '''
        self.appearance.x_axis_pos = x_axis_pos
        self.appearance.y_axis_pos = y_axis_pos
        return self

    def with_division_formatters(self, x_div_formatter=None, y_div_formatter=None):
        self.appearance.x_div_formatter = x_div_formatter
        self.appearance.y_div_formatter = y_div_formatter
        return self

    def with_subdivisions(self, factor):
        '''
        Draw subdivision lines on graph

        Args:
            factor: (x, y) Number of subdivisions per division in each direction

        Returns:
            self
        '''
        self.appearance.subdivisions = True
        self.appearance.subdivisionfactor = factor
        return self

    def with_border(self, has_border):
        '''
        Draw border around graph,  The border will be drawn with the style of the axis lines.

        Args:
            has_border: Boolean determines if border is drawn around axis.

        Returns:
            self
        '''
        self.appearance.border = has_border
        return self

    def with_ticklabeloffset(self, ticklabeloffset):
        '''
        Use the tick label offset. The tick text is offset from the tick position on the axis by a fixed amount in the x amd y directions.

        This offset is equal to the text height of the labels divided by the ticklabeloffset. The ticklabeloffset defaults to 1.1, which
        usually works well provided the divisions are reasonably far apart. If the divisions are quite close, or ifthe label font is
        unusually large or small, try adjsuting this value. The larger tha value, the closer the text will be to the axis.

        Args:
            ticklabeloffset: Number, the offset

        Returns:
            self
        '''
        self.appearance.ticklabeloffset = ticklabeloffset
        return self

    def background(self, pattern):
        '''
        Sets the entire graph background

        Args:
            pattern: color or fill pattern

        Returns:
            self
        '''
        self.appearance.background = FillParameters(pattern)
        return self

    def text_color(self, pattern):
        '''
        Sets the color of the axes text

        Args:
            pattern: color or pattern

        Returns:
            self
        '''
        self.appearance.textcolor = pattern
        return self

    def text_style(self, font="arial", weight=FONT_WEIGHT_BOLD, slant=FONT_SLANT_NORMAL, size=15):
        '''
        Set the style of the axis text

        Args:
            font: Font name
            weight: Font weight
            slant: Font slant
            size: Font size in units. This will be multiplied by the featurescale value.

        Returns:
            self
        '''
        self.appearance.fontparams = FontParameters(font, weight, slant, size)
        return self

    def axis_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the axis lines

        Args:
            pattern:  the fill pattern or color to use for the outline, None for default
            line_width: width of stroke line, None for default
            dash: dash patter of line, as for Pycairo, None for default
            cap: line end style, None for default
            join: line join style, None for default
            miter_limit: mitre limit, None for default

        Returns:
            self
        '''
        self.appearance.axislines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def division_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the division lines

        Args:
            pattern:  the fill pattern or color to use for the outline, None for default
            line_width: width of stroke line, None for default
            dash: dash patter of line, as for Pycairo, None for default
            cap: line end style, None for default
            join: line join style, None for default
            miter_limit: mitre limit, None for default

        Returns:
            self
        '''
        self.appearance.divlines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def subdivision_linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the style of the subdivision lines

        Args:
            pattern:  the fill pattern or color to use for the outline, None for default
            line_width: width of stroke line, None for default
            dash: dash patter of line, as for Pycairo, None for default
            cap: line end style, None for default
            join: line join style, None for default
            miter_limit: mitre limit, None for default

        Returns:
            self
        '''
        self.appearance.subdivlines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def draw(self):
        '''
        Draw the axes
        '''

        self.ctx.new_path()
        # Get the text height using the selected font. This is used to control text offset and other sizes.
        _, self.appearance.text_height = Text(self.ctx).of('0', (0, 0)) \
            .font(self.appearance.fontparams.font,
                  self.appearance.fontparams.weight,
                  self.appearance.fontparams.slant) \
            .size(self.appearance.fontparams.size * self.appearance.featurescale) \
            .get_size()
        self.clip()
        self._draw_background()
        if self.appearance.subdivisions:
            self._draw_subdivlines()
        self._draw_divlines()
        self.unclip()
        self._draw_axes()
        if self.appearance.border:
            self._draw_border()

    def _draw_background(self):
        self.appearance.background.apply(self.ctx)
        self.ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        self.ctx.fill()

    def _draw_border(self):
        params = copy.copy(self.appearance.axislines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        self.ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        self.ctx.stroke()

    def _draw_divlines(self):
        params = copy.copy(self.appearance.divlines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        for p in self._get_divs(self.appearance.start [0], self.appearance.extent[0], self.appearance.divisions[0]):
            self.ctx.move_to(*self.transform_from_graph((p, self.appearance.start [1])))
            self.ctx.line_to(*self.transform_from_graph((p, self.appearance.start [1] + self.appearance.extent[1])))
        for p in self._get_divs(self.appearance.start [1], self.appearance.extent[1], self.appearance.divisions[1]):
            self.ctx.move_to(*self.transform_from_graph((self.appearance.start [0], p)))
            self.ctx.line_to(*self.transform_from_graph((self.appearance.start [0] + self.appearance.extent[0], p)))
        self.ctx.stroke()

    def _draw_subdivlines(self):
        params = copy.copy(self.appearance.subdivlines)
        params.line_width *= self.appearance.featurescale
        params.apply(self.ctx)
        for p in self._get_subdivs(self.appearance.start [0], self.appearance.extent[0], self.appearance.divisions[0], self.appearance.subdivisionfactor[0]):
            self.ctx.move_to(*self.transform_from_graph((p, self.appearance.start [1])))
            self.ctx.line_to(*self.transform_from_graph((p, self.appearance.start [1] + self.appearance.extent[1])))
        for p in self._get_subdivs(self.appearance.start [1], self.appearance.extent[1], self.appearance.divisions[1], self.appearance.subdivisionfactor[1]):
            self.ctx.move_to(*self.transform_from_graph((self.appearance.start [0], p)))
            self.ctx.line_to(*self.transform_from_graph((self.appearance.start [0] + self.appearance.extent[0], p)))
        self.ctx.stroke()

    def _draw_axes(self):
        line_params = copy.copy(self.appearance.axislines)
        line_params.line_width *= self.appearance.featurescale

        xoffset = self.appearance.text_height / self.appearance.ticklabeloffset
        yoffset = self.appearance.text_height / self.appearance.ticklabeloffset

        has_origin_marker = self.appearance.x_axis_pos == AXIS_ZERO and self.appearance.y_axis_pos == AXIS_ZERO

        self.clip_x()
        tick_direction = -1 if self.appearance.x_axis_pos == AXIS_MAX else 1
        tick_align = (drawing.RIGHT, drawing.BOTTOM) if self.appearance.x_axis_pos == AXIS_MAX else (drawing.RIGHT, drawing.TOP)
        if self.appearance.x_axis_pos != AXIS_NONE:
            axis_line_pos = 0 if self.appearance.x_axis_pos == AXIS_ZERO else self.appearance.start[1] if self.appearance.x_axis_pos == AXIS_MIN else self.appearance.start[1] + self.appearance.extent[1]
            line_params.apply(self.ctx)
            self.ctx.move_to(*self.transform_from_graph((self.appearance.start[0], axis_line_pos)))
            self.ctx.line_to(*self.transform_from_graph((self.appearance.start[0] + self.appearance.extent[0], axis_line_pos)))
            self.ctx.stroke()
            for p in self._get_divs(self.appearance.start [0], self.appearance.extent[0], self.appearance.divisions[0]):
                if abs(p)>0.001 or not has_origin_marker:
                    position = self.transform_from_graph((p, axis_line_pos))
                    pstr = self._format_div(p, self.appearance.divisions[0], self.appearance.x_div_formatter)
                    Text(self.ctx).of(pstr, (position[0] - xoffset, position[1] + yoffset*tick_direction)) \
                        .font(self.appearance.fontparams.font, self.appearance.fontparams.weight,
                              self.appearance.fontparams.slant) \
                        .size(self.appearance.fontparams.size*self.appearance.featurescale) \
                        .align(*tick_align).fill(self.appearance.textcolor)
                    line_params.apply(self.ctx)
                    self.ctx.new_path()
                    self.ctx.move_to(position[0], position[1])
                    self.ctx.line_to(position[0], position[1] + yoffset*tick_direction)
                    self.ctx.stroke()
        self.unclip()

        self.clip_y()
        tick_direction = -1 if self.appearance.y_axis_pos == AXIS_MAX else 1
        tick_align = (drawing.LEFT, drawing.TOP) if self.appearance.y_axis_pos == AXIS_MAX else (drawing.RIGHT, drawing.TOP)
        if self.appearance.y_axis_pos != AXIS_NONE:
            axis_line_pos = 0 if self.appearance.y_axis_pos == AXIS_ZERO else self.appearance.start[0] if self.appearance.y_axis_pos == AXIS_MIN else self.appearance.start[0] + self.appearance.extent[0]
            line_params.apply(self.ctx)
            self.ctx.move_to(*self.transform_from_graph((axis_line_pos, self.appearance.start[1])))
            self.ctx.line_to(*self.transform_from_graph((axis_line_pos, self.appearance.start[1] + self.appearance.extent[1])))
            self.ctx.stroke()
            for p in self._get_divs(self.appearance.start [1], self.appearance.extent[1], self.appearance.divisions[1]):
                if abs(p)>0.001 or not has_origin_marker:
                    position = self.transform_from_graph((axis_line_pos, p))
                    pstr = self._format_div(p, self.appearance.divisions[1], self.appearance.y_div_formatter)
                    Text(self.ctx).of(pstr, (position[0] - xoffset*tick_direction, position[1] + yoffset)) \
                        .font(self.appearance.fontparams.font, self.appearance.fontparams.weight,
                              self.appearance.fontparams.slant) \
                        .size(self.appearance.fontparams.size*self.appearance.featurescale) \
                        .align(*tick_align).fill(self.appearance.textcolor)
                    line_params.apply(self.ctx)
                    self.ctx.new_path()
                    self.ctx.move_to(position[0], position[1])
                    self.ctx.line_to(position[0] - xoffset*tick_direction, position[1])
                    self.ctx.stroke()
        self.unclip()

        if has_origin_marker:
            line_params.apply(self.ctx)
            self.ctx.new_path()
            self.ctx.arc(*self.transform_from_graph((0, 0)), self.appearance.text_height/1.1, 0, 2 * math.pi)
            self.ctx.stroke()


    def clip_x(self):
        '''
        Set the clip region to width of the axes area.
        The height clip allows a region above and below the graph to be painted
        '''
        self.ctx.rectangle(self.position[0], self.position[1] - self.height, self.width, 3*self.height)
        self.ctx.save()
        self.ctx.clip()

    def clip_y(self):
        '''
        Set the clip region to height of the axes area.
        The width clip allows a region toe the left and right of the graph to be painted
        '''
        self.ctx.rectangle(self.position[0] - self.width, self.position[1], 3*self.width, self.height)
        self.ctx.save()
        self.ctx.clip()

    def clip(self):
        '''
        Set the clip region to the axes area.
        '''
        self.ctx.rectangle(*self.position, self.width, self.height)
        self.ctx.save()
        self.ctx.clip()

    def unclip(self):
        '''
        Undo a previous clip()
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

        Args:
            values
            value
            tolerance

        Returns:
            Result
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

    def _format_div(self, value, div, formatter):
        """
        Formats a division value into a string.
        If the division spacing is an integer, the string will be an integer (no dp).
        If the division spacing is float, the string will be a float with a suitable number of decimal places

        Args:
            value: value to be formatted
            div: division spacing
            formatter: formatting function, accepts vale and div, returns a formatted value string

        Returns:
            String representation of the value
        """
        if formatter:
            return formatter(value, div)

        if isinstance(value, int):
            return str(value)
        return str(round(value*1000)/1000)

    def transform_from_graph(self, point):
        '''
        Coverts a point/list of points defined in axes coordinates to the equivalent vector(s) in user space

        Args:
            point: Either a single point (a sequence of 2 numbers), or a sequence of points

        Returns:
            User space vector
        '''

        def _transform_point(point): # Transform a single point
            if not (hasattr(point, "__getitem__") and hasattr(point, "__iter__") and hasattr(point, "__len__")):
                raise TypeError("point must be a List, Tuple or Vector")
            if len(point) != 2:
                raise ValueError("point must have 2 elements")
            x = ((point[0] - self.appearance.start [0]) * self.width / self.appearance.extent[0]) + self.position[0]
            y = self.height + self.position[1] - ((point[1] - self.appearance.start [1]) * self.height / self.appearance.extent[1])
            return V(x, y)

        if not (hasattr(point, "__getitem__") and hasattr(point, "__iter__") and hasattr(point, "__len__")):
            raise TypeError("point must be a List, Tuple or Vector")
        if len(point) > 0 and isinstance(point[0], (int, float)):
            # If there is at least one element and it is a number, assume it is a single point
            return _transform_point(point)
        else:
            # All other cases assume it is a list of (zero or more) points
            return [_transform_point(p) for p in point]


class Plot(Shape):
    '''
    Plot a function in a set of axes.
    '''

    def __init__(self, axes):
        super().__init__(axes.ctx)
        self.axes = axes
        self.points = []
        self.closed = False

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
        if self.closed or self.final_close:
            self.ctx.close_path()
        return self

    def stroke(self, pattern=None, line_width=2, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Stroke overrides the Shape stroke() method. It clips the stroke to the area of the axes. This ensures that if
        the curve goes out of range it will not interfere with other parts of the image.

        Args:
            pattern
            line_width
            dash
            cap
            join
            miter_limit

        Returns:
            self
        '''
        super().stroke(pattern, line_width, dash, cap, join, miter_limit)


    def of_function(self, fn, extent=None, precision=100, close=()):
        '''
        Plot a function y = fn(x)

        Args:
            fn: the function to plot. It must take a single argument
            extent: the range of x values to plot. If not supplied, the plot will use the full range of the axes.
            precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
            close: sequence of (x, y) points. One or more additional points, defined in axes coordinates, that will be added
                    to the plot path to create a polygon. The polygon will also be closed. This allows an area under the curve to be filled.

        Returns:
            self
        '''
        self.points = []
        start = self.axes.appearance.start[0]
        end = self.axes.appearance.start[0] + self.axes.appearance.extent[0]
        if extent:
            start = max(start, extent[0])
            end = min(end, extent[1])
        self.points += [self.axes.transform_from_graph((x, fn(x))) for x in np.linspace(start, end, precision)]
        if close:
            self.points += [self.axes.transform_from_graph(p) for p in close]
            self.closed = True
        return self

    def of_xy_function(self, fn, extent=None, precision=100, close=()):
        '''
        Plot a function x = fn(y)

        Args:
            fn: the function to plot. It must take a single argument
            extent: the range of y values to plot. If not supplied, the plot will use the full range of the axes.
            precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
            close: sequence of (x, y) points. One or more additional points, defined in axes coordinates, that will be added
                to the plot path to create a polygon. The polygon will also be closed. This allows an area under the curve to be filled.

        Returns:
            self
        '''
        self.points = []
        start = self.axes.appearance.start[1]
        end = self.axes.appearance.start[1] + self.axes.appearance.extent[1]
        if extent:
            start = max(start, extent[0])
            end = min(end, extent[1])
        self.points += [self.axes.transform_from_graph((fn(y), y)) for y in np.linspace(start, end, precision)]
        if close:
            self.points += [self.axes.transform_from_graph(p) for p in close]
            self.closed = True
        return self

    def of_polar_function(self, fn, extent=(0, 2*math.pi), precision=100, close=()):
        '''
        Plot a polar function r = fn(theta). theta is measured in radians

        Args:
            fn: the function to plot. It must take a single argument
            extent: the range of theta values to plot. If not supplied, the plot will use the range 0 to 2*pi.
            precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
            close: sequence of (x, y) points. One or more additional points, defined in axes coordinates, that will be added
                to the plot path to create a polygon. The polygon will also be closed. This allows an area under the curve to be filled.

        Returns:
            self
        '''
        self.points = []
        for theta in np.linspace(extent[0], extent[1], precision):
            r = fn(theta)
            self.points.append(self.axes.transform_from_graph((r*math.cos(theta), r*math.sin(theta))))
        if close:
            self.points += [self.axes.transform_from_graph(p) for p in close]
            self.closed = True
        return self

    def of_parametric_function(self, fx, fy, extent=(0, 1), precision=100, close=()):
        '''
        Plot a parametric function x = fx(t), y = ft(t).

        Args:
            fx: x as a function of t. It must take a single argument
            fy: y as a function of t. It must take a single argument
            extent: the range of t values to plot. If not supplied the range 0 to 1 is used.
            precision: number of points to plot. Defaults to 100. This can be increased if needed for hi res plots
            close: sequence of (x, y) points. One or more additional points, defined in axes coordinates, that will be added
                to the plot path to create a polygon. The polygon will also be closed. This allows an area under the curve to be filled.

        Returns:
            self
        '''
        self.points = []
        for t in np.linspace(extent[0], extent[1], precision):
            x = fx(t)
            y = fy(t)
            self.points.append(self.axes.transform_from_graph((x, y)))
        if close:
            self.points += [self.axes.transform_from_graph(p) for p in close]
            self.closed = True
        return self


class Scatter:
    '''
    Plot a scatter chart in a set of axes.
    Note that a Scatter plot is not a `Shape` object. It simply draws a scatter plot on the supplied axes.
    '''

    def __init__(self, axes):
        self.axes = axes
        self.ctx = axes.ctx
        self.stroke_params = StrokeParameters()
        self.fill = FillParameters()
        self.point_style = POINT_CIRCLE
        self.point_size = 4
        self.line_style = SCATTER_NO_LINE

    def with_line_style(self, style=SCATTER_NO_LINE, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None):
        """
        Outline the shape. This draws the shape to the supplied context.

        Parameters are as described for `StrokeParameters`.

        Args:
            style: SCATTERXXX constant - the style of the plot. Default no line.
            pattern:  the fill `Pattern` or `Color` to use for the outline, None for default
            line_width: width of stroke line. None for default
            dash: sequence, dash patter of line. None for default
            cap: line end style, None for default.
            join: line join style, None for default.
            miter_limit: mitre limit, number, None for default

        Returns:
            self
        """
        self.line_style = style
        self.stroke_params = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def with_point_style(self, size, style=POINT_CIRCLE, pattern=Color(0), fill_rule=WINDING):
        """
        Sets the style of the points
        Args:
            size: number - the size of the point in user space.
            style: POINTXXX constant - the style of the point. Default circular.
            pattern: the fill `Pattern` or `Color` to use for the points.
            fill_rule: the fill rule to use for the points

        Returns:
            self
        """
        self.point_style = style
        self.point_size = size
        self.fill = FillParameters(pattern, fill_rule)
        return self

    def plot(self, x_values, y_values):
        '''
        Plot a scatter chart of the sample values

        Args:
            x_values: sequence of numbers - the x values for each sample.
            y_values: sequence of numbers - the y values for each sample. The number of x and y values should be equal. If not,
            the minimum count will be used. Eg if there are 10 x values and 8 y values, only 8 points will be plotted.

        Returns:
            self
        '''

        points = [self.axes.transform_from_graph((x, y)) for x, y in zip(x_values, y_values)]
        if self.line_style == SCATTER_CONNECTED:
            Polygon(self.ctx).of_points(points).open().stroke(self.stroke_params)
        if self.line_style == SCATTER_STALK:
            bases = [self.axes.transform_from_graph((x, 0)) for x in x_values]
            for p, b in zip(points, bases):
                Line(self.ctx).of_start_end(b, p).stroke(self.stroke_params)
        for p in points:
            Circle(self.ctx).of_center_radius(p, self.point_size).fill(self.fill.pattern, self.fill.fill_rule)
        return self



