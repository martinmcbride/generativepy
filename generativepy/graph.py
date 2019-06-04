import cairo
from generativepy import drawing
import numpy as np
import math


class Axes:
    def __init__(self, canvas, start=(0, 0), extent=(10, 10), divisions=(1, 1)):
        self.canvas = canvas
        self.start = start
        self.extent = extent
        self.divisions = divisions


    def draw(self):
        self.canvas.strokeWeight(self.canvas.page2user(0.5))
        self.canvas.noFill()
        self.canvas.stroke(drawing.Color(0.8, 0.8, 1))
        for p in self.get_divs(self.start[0], self.extent[0], self.divisions[0]):
            self.canvas.line(p, self.start[1], p, self.start[1]+self.extent[1])
        for p in self.get_divs(self.start[1], self.extent[1], self.divisions[1]):
            self.canvas.line(self.start[0], p, self.start[0]+self.extent[0], p)

        self.canvas.fill(drawing.Color(0.2, 0.2, 0.2))
        self.canvas.textSize(self.canvas.page2user(3.5))
        self.canvas.textFont('Arial')

        self.canvas.textAlign(drawing.RIGHT, drawing.TOP)
        xoffset = self.canvas.page2user(1)
        yoffset = self.canvas.page2user(1)
        for p in self.get_divs(self.start[0], self.extent[0], self.divisions[0]):
           if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[0])
                self.canvas.text(pstr, p - xoffset, -yoffset)

        self.canvas.textAlign(drawing.RIGHT, drawing.TOP)
        xoffset = self.canvas.page2user(1)
        yoffset = self.canvas.page2user(1)
        for p in self.get_divs(self.start[1], self.extent[1], self.divisions[1]):
            if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[1])
                self.canvas.text(pstr, -xoffset, p - yoffset)

        self.canvas.noFill()
        self.canvas.stroke(drawing.Color(0.2, 0.2, 0.2))
        self.canvas.line(self.start[0], 0, self.start[0]+self.extent[0], 0)
        self.canvas.line(0, self.start[1], 0, self.start[1]+self.extent[1])
        radius = self.canvas.page2user(3)
        self.canvas.ellipseMode(drawing.CENTER)
        self.canvas.ellipse(0, 0, radius, radius)

    def clip(self):
        ctx = self.canvas.ctx
        ctx.move_to(self.start[0], self.start[1])
        ctx.line_to(self.start[0]+self.extent[0], self.start[1])
        ctx.line_to(self.start[0]+self.extent[0], self.start[1]+self.extent[1])
        ctx.line_to(self.start[0], self.start[1]+self.extent[1])
        ctx.close_path()
        ctx.save()
        ctx.clip()

    def unclip(self):
        ctx = self.canvas.ctx
        ctx.restore()

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
        :param value: value to be formated
        :param div: division spacing
        :return: string representation of the value
        """
        if isinstance(value, int):
            return str(value)
        return str(round(value*1000)/1000)


def plotCurve(axes, fn, lineColor=drawing.Color(1, 0, 0), extent=None, line_width=.7):
    """
    Plot an y = fn(x)
    :param axes: Axes to plt in
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the x range
    :param line_width: line width in page space
    :return:
    """
    canvas = axes.canvas
    points = []
    for x in np.linspace(axes.start[0], axes.start[0]+axes.extent[0], 100):
        if not extent or extent[0] <= x <= extent[1]:
            points.append((x, fn(x)))
    if points:
        axes.clip()
        canvas.stroke(lineColor)
        canvas.noFill()
        canvas.strokeWeight(canvas.page2user(line_width))
        canvas.polygon(points, False)
        axes.unclip()


def plotYXCurve(axes, fn, lineColor=drawing.Color(1, 0, 0), extent=None, line_width=.7):
    """
    Plot an x = fn(y)
    :param mctx: maths context
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
    :param line_width: line width in page space
    :return:
    """
    canvas = axes.canvas
    points = []
    for y in np.linspace(axes.start[1], axes.start[1]+axes.extent[1], 100):
        if not extent or extent[0] <= y <= extent[1]:
            points.append((fn(y), y))
    if points:
        axes.clip()
        canvas.stroke(lineColor)
        canvas.noFill()
        canvas.strokeWeight(canvas.page2user(line_width))
        canvas.polygon(points, False)
        axes.unclip()


def plotPolarCurve(axes, fn, lineColor=drawing.Color(1, 0, 0), range=(0, 2*math.pi), extent=None, line_width=.7):
    """
    Plot an r = fn(theta)
    :param mctx: maths context
    :param fn: the function, a function object taking 1 number and returning a number
    :param lineColor: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
    :param line_width: line width in page space
    :return:
    """
    canvas = axes.canvas
    points = []
    for theta in np.linspace(range[0], range[1], 100):
        if not extent or extent[0] <= theta <= extent[1]:
            r = fn(theta)
            points.append((r*math.cos(theta), r*math.sin(theta)))
    if points:
        axes.clip()
        canvas.stroke(lineColor)
        canvas.noFill()
        canvas.strokeWeight(canvas.page2user(line_width))
        canvas.polygon(points, False)
        axes.unclip()
