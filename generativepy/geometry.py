# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
"""
The geometry module provides classes for drawing shapes. There are several classes:

* `Shape` is an abstract base class for classes that draw specific shapes, such as `Rectangle` or `Polygon. A shape can
be filled, stroked, or both, using any `Pattern`. It is possible to create compound shapes, for example shapes with holes
in them. Shapes can also be used to set clipping regions, and a shape can be stored as a path object that can be
reused.
* `Pattern` is an abstract base class for classes that provide area fills. Currently only the `LinearGradient` pattern is
supported.
* `Image` provides a simple way to render an image from a PNG file.
* `Transform` allows user space to be transformed, to implement translation, scaling, rotation, mirroring, shearing, and
general affine transformations.
* `Turtle` provides a simple implementation of turtle graphics.
"""
import itertools
import cairo
import math
from dataclasses import dataclass
from generativepy.drawing import LEFT, CENTER, RIGHT, BOTTOM, MIDDLE, BASELINE, TOP
from generativepy.drawing import WINDING
from generativepy.drawing import FONT_WEIGHT_NORMAL, FONT_WEIGHT_BOLD
from generativepy.drawing import FONT_SLANT_NORMAL, FONT_SLANT_ITALIC, FONT_SLANT_OBLIQUE
from generativepy.drawing import MITER, ROUND, BEVEL, BUTT, SQUARE
from generativepy.drawing import LINE, RAY, SEGMENT
from generativepy.math import Vector as V
from generativepy.color import Color

class Pattern:
    """
    Base class for all patterns.

    In generativepy, shapes can be filled or stroked (outline) using solid colours or patterns. Currently, the only pattern
    supported is linear gradient. More patterns will be supported in future versions.

    Patterns all work in s similar way:

    * The pattern is first constructed using the constructor and any required builder methods.
    * The build method is then called to create the pattern.

    The object returned by get_pattern can be used in place of a Color object when setting a stroke or fill.
    """

    def __init__(self):
        self.pattern = None


    def get_pattern(self):
        """
        Get the Pycairo pattern object associated with this Pattern

        Returns:
            Pycairo pattern object
        """
        return self.pattern


class LinearGradient(Pattern):
    """
    Defines a linear gradient `pattern`
    """

    def __init__(self):
        super().__init__()
        self.start = (0, 0)
        self.end = (0, 0)
        self.stops = []

    def of_points(self, start, end):
        """
        Set the points for the Pycairo LinearGradient pattern

        Args:
            start: Sequence of 2 numbers - The start point, (x, y)
            end: Sequence of 2 numbers - The end point, (x, y)

        Returns:
            self
        """
        self.start = start
        self.end = end
        return self

    def with_start_end(self, color1, color2):
        """
        Set up a simple linear gradient, with a start color at position 0 and an end color at position 1.
        This is equivalent to calling with_stops with ((0, color1), (1, color2)

        Args:
            color1: `Color` - The start colour (ie the colour at the start point).
            color2: `Color` - The end colour (ie the colour at the end point).

        Returns:
            self
        """
        self.stops = [(0, color1), (1, color2)]
        return self

    def with_stops(self, stops):
        """
        Set the gradient stops. There should be 2 or more stops in the sequence.

        Args:
            stops: tuple of numbers - Each stop tuple (position, color) where `position` is a number indicating the position of the stop between
                    the start and end points, and `color`is the `Color` of the stop.

        Returns:
            self
        """
        self.stops = [(pos, color) for pos, color in stops]
        return self

    def build(self):
        """
        Build the pattern. This must be called after all the stops have been added. It creates the Pycairo
        Pattern object that will be returned by get_pattern

        Returns:
            self
        """
        self.pattern = cairo.LinearGradient(self.start[0], self.start[1], self.end[0], self.end[1])
        for position, color in self.stops:
            self.pattern.add_color_stop_rgba(position, color.r, color.g, color.b, color.a)
        return self


@dataclass
class FillParameters:
    """
    Stores parameters for filling a shape, and can apply them to a context
    """

    def __init__(self, pattern=Color(0), fill_rule=WINDING):
        """
        `pattern` specifies the colour or pattern that will be used to stroke the shape. It can either be:

        * A `Color` object to specify a flat colour fill.
        * A `Pattern` object to specify a special fill (for example a `LinearGradient`).

        It defaults to black.

        `fill_rule` only applies to complex paths such as self-intersecting paths. It controls which
        parts of the path will be filled, and which will be left as "holes". Possible values are `drawing.EVEN_ODD` and `drawing.WINDING`.

        Args:
            pattern: the fill `Pattern` or `Color` to use, None for default
            fill_rule: the fill rule to use, None for default.
        """
        self.pattern = Color(0) if pattern is None else pattern
        self.fill_rule = WINDING if fill_rule is None else fill_rule

    def apply(self, ctx):
        """
        Apply the settings to a context. After this, any fill operation using the context will use the
        settings.

        Args:
            ctx: The context to apply the settings to.
        """
        if isinstance(self.pattern, Color):
            ctx.set_source_rgba(*self.pattern)
        else:
            ctx.set_source(self.pattern.get_pattern())

        if self.fill_rule == WINDING:
            ctx.set_fill_rule(cairo.FillRule.WINDING)
        else:
            ctx.set_fill_rule(cairo.FillRule.EVEN_ODD)


@dataclass
class StrokeParameters:
    """
    Stores parameters for stroking a shape, and can apply them to a context
    """

    def __init__(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        """
        `pattern` specifies the colour or pattern that will be used to stroke the shape. It can either be:

        * A `Color` object to specify a flat colour fill.
        * A `Pattern` object to specify a special fill (for example a `LinearGradient`).

        It defaults to `Color` black.

        `line_width` controls the width of the line. The line width is in user units, and default to 1.

        `dash` creates dashed lines, specified by an array of numbers. For example:

        * [5] creates a dash pattern where the dashes are 5 units long, separated by gaps that are 5 units long.
        * [3, 4] creates a dash pattern where the dashes are 3 units long, separated by gaps that are 4 units long.

        `cap` controls the style of the line ends:

        * drawing.ROUND creates rounded line ends.
        * drawing.SQUARE creates square line ends that extend slightly beyond the line start and end points.
        * drawing.BUTT creates square line ends that end exactly on the line start and end points.

        `join` controls the style of the corners (where two line sections meet):

        * drawing.MITRE creates pointed corners.
        * drawing.ROUND creates rounded corners.
        * drawing.BEVEL is similar to MITRE but the sharp point of the corner is cut off.

        miter_limit is used in conjunction with the MITRE join style. For joins at small angles, the mitre can become very long.
        miter_limit automatically switches to BEVEL mode at low angles. miter_limit is enabled by default at an angle of about
        11 degrees, which is suitable for most applications.


        Args:
            pattern:  the fill `Pattern` or `Color` to use for the outline, None for default
            line_width: width of stroke line. None for default
            dash: sequence, dash patter of line. None for default
            cap: line end style, None for default.
            join: line join style, None for default.
            miter_limit: mitre limit, number, None for default
        """
        self.pattern = Color(0) if pattern is None else pattern
        self.line_width = 1 if line_width is None else line_width
        self.dash = [] if dash is None else dash
        self.cap = SQUARE if cap is None else cap
        self.join = MITER if join is None else join
        self.miter_limit = 10 if miter_limit is None else miter_limit

    def apply(self, ctx):
        """
        Apply the settings to a context. After this, any stroke operation using the context will use the
        settings.

        Args:
            ctx: The context to apply the settings to.
        """
        if isinstance(self.pattern, Color):
            ctx.set_source_rgba(*self.pattern)
        else:
            ctx.set_source(self.pattern.get_pattern())

        ctx.set_line_width(self.line_width)

        ctx.set_dash(self.dash)

        if self.cap == ROUND:
            ctx.set_line_cap(cairo.LineCap.ROUND)
        elif self.cap == BUTT:
            ctx.set_line_cap(cairo.LineCap.BUTT)
        else:
            ctx.set_line_cap(cairo.LineCap.SQUARE)

        if self.join == ROUND:
            ctx.set_line_join(cairo.LineJoin.ROUND)
        elif self.join == BEVEL:
            ctx.set_line_join(cairo.LineJoin.BEVEL)
        else:
            ctx.set_line_join(cairo.LineJoin.MITER)

        ctx.set_miter_limit(self.miter_limit)


@dataclass
class FontParameters:
    """
    Stores parameters for font, and can apply them to a context
    """

    def __init__(self, font=None, weight=None, slant=None, size=None):
        """
        Args:
            font: str - name of font face.
            weight: number - font weight. This can be `FONT_WEIGHT_NORMAL` or `FONT_WEIGHT_BOLD`, defined in the`drawing` module.
            slant: int - font slant. This can be `FONT_SLANT_NORMAL`, `FONT_SLANT_ITALIC` or `FONT_SLANT_OBLIQUE`, defined in the`drawing` module.
            size: number - font size. This is the *approximate* size of the characters in user space units.
        """
        self.font = 'Arial' if font is None else font
        self.weight = FONT_WEIGHT_NORMAL if weight is None else weight
        self.slant = FONT_SLANT_NORMAL if slant is None else slant
        self.size = 10 if size is None else size

    def apply(self, ctx):
        """
        Apply the settings to a context. After this, any text operation using the context will use the
        specified font.

        Args:
            ctx: The context to apply the settings to.
        """
        c_weight = cairo.FONT_WEIGHT_NORMAL
        if self.weight == FONT_WEIGHT_BOLD:
            c_weight = cairo.FONT_WEIGHT_BOLD

        c_slant = cairo.FONT_SLANT_NORMAL
        if self.slant == FONT_SLANT_ITALIC:
            c_slant = cairo.FONT_SLANT_ITALIC
        elif self.slant == FONT_SLANT_OBLIQUE:
            c_slant = cairo.FONT_SLANT_OBLIQUE

        ctx.select_font_face(self.font, c_slant, c_weight)
        ctx.set_font_size(self.size)


class Shape():
    """
    Classes derived from `Shape` are intended to supplement the normal Pycairo drawing methods, so make common shapes a
    bit less cumbersome. You can always mix and match native Pycairo calls with shape calls, which is useful for drawing
    complex shapes or using special fills such as gradients or patterns.
    """
    def __init__(self, ctx):
        """
        Args:
            ctx: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.ctx = ctx
        self.extend = False
        self.sub_path = False
        self.final_close = False
        self.added = False

    def extend_path(self, close=False):
        """
        Adds the shape to the context but does not draw it. The shape is added by extending the current path, preserving and adding to
        anything that was previously defined in the drawing context.

        This function is used to join several open shapes, to form a more complex shape. It can be used to join any combination
        of the following shapes:

        * Line.
        * Bezier.
        * Polygon, but the shape should be left open (using the open method).
        * Circle, but only in arc mode (using the as_arc method).

        When the final shape is added, you can optionally set the close flag to create a closed shape.
        You should not add any further sections after this final call. Alternatively, if the close flag is not set it will create an open shape.

        Args:
            close: bool - controls whether the extended path should be closed or left open.

        Returns:
            self
        """
        self.sub_path = True
        self.extend = True
        self.final_close = close
        return self

    def as_sub_path(self):
        """
        Adds the shape to the context but does not draw it. The shape is added as a new subpath, preserving and adding to anything that was previously defined
        in the drawing context.

        This method allows you to create complex paths, consisting of two or more separate shapes.
        This allows you to do things such as creating shapes with holes or creating complex clip paths.

        Returns:
            self
        """
        self.sub_path = True
        return self

    def _do_path_(self):
        if not self.sub_path:
            self.ctx.new_path()

    def add(self):
        """
        Adds the shape to the context but does not draw it. The shape is added as a new path.

        This method is mainly for internal use. Each shape subclass overrides this method to draw the specific shape. This method is called
        to generate the shape path the first time it is is filled, stroked etc.

        Returns:
            self
        """
        raise NotImplementedError()

    def fill(self, pattern=None, fill_rule=None):
        """
        Fill the shape. This draws the shape to the supplied context.

        Parameters are as described for `FillParameters`. Alternatively, if a `FillParameters` object is supplied as a pattern, it will be used and the
        other parameters will be ignored.

        Args:
            pattern: the fill `Pattern` or `Color` to use, or a `FillParameters` object. None for default
            fill_rule: the fill rule to use, None for default.

        Returns:
            self
        """
        if not self.added:
            self.add()
            self.added = True

        if isinstance(pattern, FillParameters):
            pattern.apply(self.ctx)
        else:
            FillParameters(pattern, fill_rule).apply(self.ctx)

        self.ctx.fill_preserve()
        return self

    def stroke(self, pattern=Color(0), line_width=1, dash=None, cap=SQUARE, join=MITER, miter_limit=None):
        """
        Outline the shape. This draws the shape to the supplied context.

        Parameters are as described for `StrokeParameters`.  Alternatively, if a `StrokeParameters` object is supplied as a pattern, it will be used and the
        other parameters will be ignored.

        Args:
            pattern:  the fill `Pattern` or `Color` to use for the outline, or a `StrokeParameters` object. None for default
            line_width: width of stroke line. None for default
            dash: sequence, dash patter of line. None for default
            cap: line end style, None for default.
            join: line join style, None for default.
            miter_limit: mitre limit, number, None for default

        Returns:
            self
        """
        if not self.added:
            self.add()
            self.added = True

        if isinstance(pattern, StrokeParameters):
            pattern.apply(self.ctx)
        else:
            StrokeParameters(pattern, line_width, dash, cap, join, miter_limit).apply(self.ctx)

        self.ctx.stroke_preserve()
        return self

    # Deprecated, use fill() and stroke()
    def fill_stroke(self, fill_color, stroke_color, line_width=1):
        """
        Deprecated. Use `fill` followed by `stroke.
        """
        self.fill(fill_color)
        self.stroke(stroke_color, line_width)
        return self

    def clip(self):
        """
        Creates a clip region from the current context.

        clip is called in a similar way to fill, but instead of filling the current shape, it establishes a
        clipping region using the shape.

        When the clipping region is in force, anything else you draw will be clipped to that region. Anything
        outside that region will be protected from any drawing operations.

        If you apply more than a clipping region A, and then apply another clipping region B, the result will be the
        intersection of the two regions.

        If you wish to undo the clip path later, the easiest method is to place the clipping code inside a `with Transform` block. The clip path
        will be removed on leaving the block. Alternatively (and more advanced), store the old context returned by this function and restore it
        later with a Pycairo call.

        Returns:
            The old context.
        """
        if not self.added:
            self.add()
            self.added = True
        return self.ctx.clip_preserve()

    def path(self):
        """
        Get the current path. This corresponds to the path that would be filled or stroked by the `fill` or `stroke` methods.

        path is called in a similar way to fill, but instead of filling the current shape, it takes a snapshot of the shape
        and returns it as a Pycairo path object.

        You can save this object and pass it into a Path object later. When you fill or stroke the Path, it will recreate the
        shape. This can be useful if you need to use the same shape more than once, or if you want to pass a shape into another
        function as a parameter.

        You can also iterate over the path using Pycairo functions to do fancy things like placing text along a curve.
        Refer to the Pycairo documentation for more information.

        You should generally treat the returned Pycairo path as an opaque object - that is to say, you can pass it around
        but you shouldn't generally try to modify it or use its internal data.

        Note that path returns a flattened path. That is a path where all the curves have been converted to straight-line
        segments. The path will be reproduced perfectly at the same scale, but if you store a path and then redraw it using a
        large scale factor you might see some distortion of the curve.

        Returns:
            The current path
        """
        if not self.added:
            self.add()
            self.added = True
        return self.ctx.copy_path_flat()


class Path(Shape):
    """
    The Path class creates a shape based on a path object.

    A path object can be obtained using the path method of any Shape object - a Rectangle, Circle, or even a
    Text object can be used to create a path.
    """

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
        """
        Creates a shape based on an existing path.

        A `path` object is usually obtained by calling the path method another shape. A Path object recreates the shape and allows
        it to be filled.

        Here is an example:

        ```
        p = Rectangle(ctx).of_corner_size((0.5, 0.5), 1, 3).path()
        Path.of(p).fill(Color('yellow'))
        ```

        The first line creates a rectangle, but doesn't draw it, instead it obtains a path object `p`. At some point later in the
        code, you can draw the shape by passing p into a Path object and filling or stroking it.

        This is useful if you want to reuse a path, drawing it multiple times, or if you need to create a path is one part of your code but store it for use somewhere else. Paths also have advanced applications such as drawing text along a curve.

        Args:
            path:  Pycairo path object that defines the shape

        Returns:
            self
        """
        self.path = path
        return self

class Rectangle(Shape):
    """
    The Rectangle class represents a rectangle shape.
    """

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
        """
        Creates a rectangle based on the position and size.

        Args:

            corner:  (number, number) - A tuple of two numbers, giving the (x, y) position of the top left corner.
            width:  number - The width.
            height:  number - The height.

        Returns:
            self
        """
        self.x = corner[0]
        self.y = corner[1]
        self.width = width
        self.height = height
        return self


def rectangle(ctx, corner, width, height):
    """
    Deprecated, use `Rectangle` class instead
    """
    Rectangle(ctx).of_corner_size(corner, width, height).add()


class Square(Shape):
    """
    The Square class represents a square shape.
    """

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
        """
        Creates a square based on the position and size.

        Args:
            corner:  (number, number) - A tuple of two numbers, giving the (x, y) position of the top left corner.
            width:  number - The width.

        Returns:
            self
        """
        self.x = corner[0]
        self.y = corner[1]
        self.width = width
        return self


def square(ctx, corner, width):
    """
    Deprecated, use `Square` class instead
    """
    Square(ctx).of_corner_size(corner, width).add()


class Triangle(Shape):
    """
    The Triangle class represents a triangle shape.
    """

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
        """
        Creates a triangle based on the corners

        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of corner a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of corner b.
            c:  (number, number) - A tuple of two numbers, giving the (x, y) position of corner c.

        Returns:
            self
        """
        self.a = a
        self.b = b
        self.c = c
        return self


def triangle(ctx, a, b, c):
    """
    Deprecated, use `Triangle` class instead
    """
    Triangle(ctx).of_corners(a, b, c).add()


class Text(Shape):
    """
    The `Text` class is used to draw text. It allows control of the font, the style, and size of the text. It also
    has methods to control the positioning of the text, and to return text metrics.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.text = 'text'
        self.position = (0, 0)
        self._size = None
        self._font = None
        self._weight = None
        self._slant = None
        self.alignx = LEFT
        self.aligny = BASELINE
        self._flip = False
        self._offset = (0, 0)

    def add(self):
        self._do_path_()
        FontParameters(font=self._font, size=self._size, weight=self._weight, slant=self._slant).apply(self.ctx)

        x, y = self.position
        x += self._offset[0]
        y += self._offset[1]
        xb, yb, width, height, _, dy = self.ctx.text_extents(self.text)

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

    def get_metrics(self):
        """
        Get the metrics of the text. This is a tuple (x_bearing, y_bearing, width, height, x_advance, y_advance), see the Pycairo
        documentation for a description of those terms
        """
        FontParameters(font=self._font, size=self._size, weight=self._weight, slant=self._slant).apply(self.ctx)
        return self.ctx.text_extents(self.text)

    def get_size(self):
        """
        Get the size of the text. This is a tuple (width, height) giving the width and height of the part of the page
        marked by the text, in user units.
        """
        FontParameters(font=self._font, size=self._size, weight=self._weight, slant=self._slant).apply(self.ctx)
        extents = self.ctx.text_extents(self.text)
        return extents[2], extents[3]

    def of(self, text, position):
        """
        Sets the text to be displayed, and the position.

        Args:
            text:  str - The text to display. Only single line text is supported.
            position:  (number, number) - (x, y) position of the text. This uses the alignment specified by the
                align functions below.

        Returns:
            self
        """
        self.text = text
        self.position = position
        return self

    def font(self, font, weight=None, slant=None):
        """
        Selects the font face. If this method is not called, the font defaults to 'arial'.

        Args:
            font:  str - The name of the font, such as 'arial'.
            weight:  int - The font weight, either `drawing.FONT_WEIGHT_NORMAL` or `drawing.FONT_WEIGHT_BOLD`.
            slant:  int - The font slant, either `drawing.FONT_SLANT_NORMAL`, `drawing.FONT_SLANT_ITALIC`, or
                    `drawing.FONT_SLANT_OBLIQUE`.

        Returns:
            self
        """
        self._font = font
        self._weight = weight
        self._slant = slant
        return self

    def size(self, size):
        """
        Sets the font size. For western fonts, the font size is approximately equal to the height of the font
        in user units. This may vary slightly for different font faces, and non-western fonts (for example
        Chinese fonts). If size is not called, the size default to 10. The size is measured in userspace units.

        Args:
            size:  number - The size of the text.

        Returns:
            self
        """
        self._size = size
        return self

    def align(self, alignx, aligny):
        """
        Sets the text alignment.

        alignx should be set to drawing.LEFT, drawing.CENTER, or drawing.RIGHT. This causes the left, centre,
        or right of the text bounding box to be aligned with the x value of the text position.

        aligny should be set to drawing.BOTTOM, drawing.MIDDLE, drawing.TOP, or drawing.BASELINE. This causes
        the bottom, middle, top, or baseline of the text to be aligned with the y value of the text position.

        The bottom, middle, and top positions are calculated from the text bounding box, but the baseline comes
        from the font metrics. If you need to correctly align two text strings you should use baseline rather than bottom, because the bottom depends on the string contents.

        If the align function is not called, the default is drawing.LEFT and drawing.BASELINE.

        As an alternative, you can use the `align_xxx()` methods to se the alignment.

        Args:
            alignx:  int - Sets the horizontal alignment of the text.
            aligny:  int - Sets the vertical alignment of the text.

        Returns:
            self
        """
        self.alignx = alignx
        self.aligny = aligny
        return self

    def align_left(self):
        """
        Sets the horizontal alignment to drawing.LEFT but leaves the vertical alignment unchanged.

        Returns:
            self
        """
        self.alignx = LEFT
        return self

    def align_center(self):
        """
        Sets the horizontal alignment to drawing.CENTER but leaves the vertical alignment unchanged.

        Returns:
            self
        """
        self.alignx = CENTER
        return self

    def align_right(self):
        """
        Sets the horizontal alignment to drawing.RIGHT but leaves the vertical alignment unchanged.

        Returns:
            self
        """
        self.alignx = RIGHT
        return self

    def align_bottom(self):
        """
        Sets the vertical alignment to drawing.BOTTOM but leaves the horizontal alignment unchanged.

        Returns:
            self
        """
        self.aligny = BOTTOM
        return self

    def align_baseline(self):
        """
        Sets the vertical alignment to drawing.BASELINE but leaves the horizontal alignment unchanged.

        Returns:
            self
        """
        self.aligny = BASELINE
        return self

    def align_middle(self):
        """
        Sets the vertical alignment to drawing.MIDDLE but leaves the horizontal alignment unchanged.

        Returns:
            self
        """
        self.aligny = MIDDLE
        return self

    def align_top(self):
        """
        Sets the vertical alignment to drawing.TOP but leaves the horizontal alignment unchanged.

        Returns:
            self
        """
        self.aligny = TOP
        return self

    def flip(self):
        """
        Flips the text vertically. This is useful if yiu are working with a flipped userspace.

        Returns:
            self
        """
        self._flip = True
        return self

    def offset(self, x=0, y=0):
        """
        Offsets the text in the x and y axes.

        Args:
            x:  number - The x offset.
            y:  number - The y offset.

        The offset moves the text in the x and y direction. The amount of offset is measured in user space.
        The offset is simple added to the position of the text. So for example:

        `Text(ctx).of("text", p).offset(x, y).fill(color)`

        is equivalent to:

        `Text(ctx).of("text", (p[0]+x, p[1]+y)).fill(color)`

        It is a matter of personal preference which form you use.

        Returns:
            self
        """
        self._offset = (x, y)
        return self

    def offset_angle(self, angle, distance):
        """
        Offsets the text by a given distance in a specified direction.

        Args:
            angle:  number - The direction to move the text.
            distance:  number - The distance to move the text.

        Thi sfunction is equivalent to:

        `offset(distance*math.cos(angle), distance*math.sin(angle))`

        Returns:
            self
        """
        self._offset = V.polar(distance, angle)
        return self

    def offset_towards(self, point, distance):
        """
        Offsets the text by a given distance towards a particular point

        Args:
            point:  number - The target point
            distance:  number - The distance to move the text.

        Displaces the text by an amount distance towards the point. If distance is negative, the text will
        be moved in the opposite direction, ie away from the point.

        Returns:
            self
        """
        direction = V(point) - V(self.position)
        unit = direction.unit
        self._offset = (distance*unit.x, distance*unit.y)
        return self



def text(ctx, txt, x, y, font=None, size=None, weight=None, slant=None, color=None, alignx=LEFT, aligny=BASELINE, flip=False):
    """
    Deprecated, use `Text` class instead
    """
    shape = Text(ctx).of(txt, (x, y)).align(alignx, aligny)
    if font:
        shape = shape.font(font, weight, slant)
    if size:
        shape = shape.size(size)
    if flip:
        shape = shape.flip()

    if color:
        ctx.set_source_rgba(*color)

    shape.add()
    ctx.fill()


class Line(Shape):
    """
    The Line class draws a line.

    There is also a line function that just creates a line as a new path.

    There are three different types of line:

    * A `SEGMENT` is a line drawn from the start point to the end point. It has finite length. This is the default.
    * A `RAY` is a line drawn from the start point that passes through the end point then continues on forever. It is
    sometimes called a half line.
    * A `LINE` is a line that passes through the start and end points but continues forever in both directions.
    """
    def __init__(self, ctx):
        super().__init__(ctx)
        self.start = (0, 0)
        self.end = (0, 0)
        self.extent_type = SEGMENT
        self.infinity = 1000

    def _get_start(self):
        # Get the effective start position for a full LINE
        # If this is a segment, ray or zero length line just return the normal start point
        if self.extent_type == SEGMENT or self.extent_type == RAY or self.start == self.end:
            return self.start
        # Get the line angle and extend backward to infinity
        angle = math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
        return self.start[0] - math.cos(angle)*self.infinity, self.start[1] - math.sin(angle)*self.infinity

    def _get_end(self):
        # Get the effective end position for a full LINE or RAY
        # If this is a segment, zero length line just return the normal start point
        if self.extent_type == SEGMENT or self.start == self.end:
            return self.end
        # Get the line angle and extend backward to infinity
        angle = math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
        return self.start[0] + math.cos(angle)*self.infinity, self.start[1] + math.sin(angle)*self.infinity

    def add(self):
        self._do_path_()
        if not self.extend:
            self.ctx.move_to(*self._get_start())
        self.ctx.line_to(*self._get_end())
        if self.final_close:
            self.ctx.close_path()
        return self

    def of_start_end(self, start, end):
        """
        Creates a line based on the start and end points.

        Args:
            start:  (number, number) - A tuple of two numbers, giving the (x, y) position of the start of the line.
            end:  (number, number) - A tuple of two numbers, giving the (x, y) position of the end of the line.

        Returns:
            self
        """
        self.start = start
        self.end = end
        return self

    def of_end(self, end):
        """
        Creates a line based on the end point. The start paint defaults to (0, 0). This is typically used when creating
        complex paths where we might want to extend an existing path by adding a line to it.

        Args:
            end:  (number, number) - A tuple of two numbers, giving the (x, y) position of the end of the line.

        Returns:
            self
        """
        self.start = (0, 0)
        self.end = end
        return self

    def as_line(self, infinity=None):
        """
        Sets the line mode to LINE

        Args:
            infinity:  number - a large number such that a line of length `infinity` is any direction will always be outside the
                drawing area. Default 1000, which is fine for most cases.

        Returns:
            self
        """
        self.extent_type = LINE
        if infinity:
            self.infinity = infinity
        return self

    def as_ray(self, infinity=None):
        """
        Sets the line mode to RAY

        Args:
            infinity:  number - a large number such that a line of length `infinity` is any direction will always be outside the
                drawing area. Default 1000, which is fine for most cases.

        Returns:
            self
        """
        self.extent_type = RAY
        if infinity:
            self.infinity = infinity
        return self

    def as_segment(self, infinity=None):
        """
        Sets the line mode to SEGMENT

        Args:
            infinity:  number - a large number such that a line of length `infinity` is any direction will always be outside the
                drawing area. Default 1000, which is fine for most cases.

        Returns:
            self
        """
        self.extent_type = SEGMENT
        if infinity:
            self.infinity = infinity
        return self

    def as_type(self, extent_type, infinity=None):
        """
        Sets the line mode to the supplied mode

        Args:
            extent_type:  number - can be `drawing.SEGMENT`, `drawing.LINE` or `drawing.RAY`
            infinity:  number - a large number such that a line of length `infinity` is any direction will always be outside the
        drawing area. Default 1000, which is fine for most cases.

        Returns:
            self
        """
        self.extent_type = extent_type
        if infinity:
            self.infinity = infinity
        return self


def line(ctx, start, end):
    """
    Deprecated, use `Line` class instead
    """
    Line(ctx).of_start_end(start, end).add()


class Bezier(Shape):
    """
    The Bezier class draws a bezier curve.
    """

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
        """
        Creates a bezier curve based on the control points.
        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point b.
            c:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point c.
            d:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point d.

        Returns:
            self
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        return self

    def of_bcd(self, b, c, d):
        """
        Creates a bezier curve based on the control points, but with control point a set to (0, 0).  This is typically used when creating
        complex paths where we might want to extend an existing path by adding a bezier curve to it.

        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point b.
            c:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point c.
            d:  (number, number) - A tuple of two numbers, giving the (x, y) position of control point d.

        Returns:
            self
        """
        self.a = (0, 0)
        self.b = b
        self.c = c
        self.d = d
        return self


class Polygon(Shape):
    """
    The `Polygon` class draws a polygon.

    A polygon is defined by a list of points. The polygon is formed by joining the points with straight lines.

    It is also possible to use bezier curves rather than straight lines to join the points. A shape can be formed from any combination of straight lines and curves.

    There is also a polygon function that just creates a polygon as a new path.
    """

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
        """
        Creates a polygon based on a list of points.

        To define a simple polygon with straight sides, points should just be a list of points, like this:

       `[(300, 100), (300, 150), (400, 200), (450, 100)]`

        This will create a polygon with 4 vertices, at the points (300, 100), (300, 150), (400, 200), and (450, 100).

        Alternatively, it is possible to specify that some of the sides are bezier curves rather than straight lines, like this:

        `[(1, 4.5), (1, 2.5), (2, 3, 3, 4, 4, 2.5), (4, 4.5)]`

        In this case, the third item is 6 elements long. This means that the second and third points are connected by a bezier curve (rather than a straight line) with values:

        `(1, 2.5), (2, 3), (3, 4), (4, 2.5)`

        The polygon will be closed by default. To create an open polygon, call the open method.

        Args:
            points:  sequence of number tuples - A sequence of line or curve specifiers.

        Returns:
            self
        """
        self.points = points
        return self

    def open(self, open_polygon=True):
        """
        Creates an open polygon, rather than a closed polygon.

        Calling this method will cause the final polygon to be open - the last point will not be connected
        to the first point. To create a closed polygon, simply don't call this method.

        Args:
            open_polygon:  optional boolean - specifies if the shape should be open. Normally call `open()` with no
        parameter tio create an open polygon.

        Returns:
            self
        """
        self.closed = not open_polygon
        return self


def polygon(ctx, points, closed=True):
    """
    Deprecated, use `Polygon` class instead
    """
    shape = Polygon(ctx).of_points(points)
    if not closed:
        shape.open()
    shape.add()


class Circle(Shape):
    """
    The Circle class draws circles, arcs, sectors and segments.
    """

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
        """
        Creates a circle based on the centre point and radius.

        Args:
            center:  (number, number) - A tuple of two numbers, giving the (x, y) position of the centre of the circle.
            radius:  number - The radius of the circle

        Returns:
            self
        """
        self.center = center
        self.radius = radius
        return self

    def as_arc(self, start_angle, end_angle):
        """
        Modifies a circle, to show only an arc. An arc is part of the circumference of the circle.

        Args:
            start_angle:  number - The start angle of the arc
            end_angle:  number - The end angle of the arc

        This is used as a modifier with of_center_radius, to draw just an arc. To draw an arc use:

        `Circle(ctx).of_center_radius((0, 0), 1).as_arc(0, 1).stroke(Color('black'), 0.1)`

        Angles are measured in radians. Angle zero lies along the positive x-axis, and the angle increases
        in the clockwise direction - note that this is opposite to the normal mathematical convention,
        where angle increases in the counterclockwise direction. The difference is due to the fact that y
        increases as you move down the image in generativepy.

        If you are using a flipped coordinate system (see the setup function in the drawing module),
        the angle increases in the counterclockwise direction.

        Since an arc is a line, you should normally use the stroke method to draw it. If you attempt to
        fill the arc, it will fill it as if it was a segment.

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.arc
        return self

    def as_sector(self, start_angle, end_angle):
        """
        Modifies a circle, to show only a sector. A sector is a "pizza slice", like you would use
        in a pie chart.

        Args:
            start_angle:  number - The start angle of the sector
            end_angle:  number - The end angle of the sector

        This function works in a similar way to the as_arc function, but it includes the area
        of the sector. You can fill or stroke the area.

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.sector
        return self

    def as_segment(self, start_angle, end_angle):
        """
        Modifies a circle, to show only a segment. A segment is the part of the circle that is cut off by a chord.

        Args:
            start_angle:  number - The start angle of the segment
            end_angle:  number - The end angle of the segment

        This function works in a similar way to the as_arc function, but it includes the area
        of the segment. You can fill or stroke the area.

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.segment
        return self

def circle(ctx, center, radius):
    """
    Deprecated, use `Circle` class instead
    """
    Circle(ctx).of_center_radius(center, radius).add()


class RegularPolygon(Shape):
    """
    The RegularPolygon class draws a regular polygon. A regular polygon is defined by its:

    * Centre.
    * Number of sides.
    * Radius (the distance from the centre to any one of its vertices).

    You can also draw a regular polygon using the Polygon class, by calculating the position of each vertex.
    The RegularPolygon class is more convenient because it performs the calculations automatically, and also
    provides some useful properties of the shape.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.closed = True
        self.centre = (0, 0)
        self.numsides = 3
        self.radius = 1
        self.points = None

    def add(self):
        self._do_path_()
        centre_angle = math.pi*2/self.numsides
        angle = math.pi/2 - centre_angle/2
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

    def of_centre_sides_radius(self, centre, numsides, radius, angle=0):
        """
        Creates a regular polygon based on its parameters.

        Creates a regular polygon, centred at centre, with numsides sides. radius controls the distance of
        each vertex from the centre, and therefore indirectly controls the size.

        By default, the shape is oriented so that the bottom side is horizontal. If angle is set to a non-zero
        value, the shape will be rotated about its centre by angle radians in a clockwise direction.

        Args:
            center:  (number, number) - A tuple of two numbers, giving the (x, y) position of the centre
                    of the polygon.
            numsides:  number - The number of sides of the polygon.
            radius:  number - The distance from the centre to any one of its vertices.
            angle:  number - Angle to rotate the shape (defaults to zero).

        Returns:
            self
        """
        self.centre = centre
        self.numsides = numsides
        self.radius = radius
        centre_angle = math.pi*2/self.numsides
        angle = math.pi/2 - centre_angle/2 + angle
        p = []
        for i in range(self.numsides):
            p.append((self.centre[0]+self.radius*math.cos(angle),
                      self.centre[1] + self.radius * math.sin(angle)))
            angle += centre_angle
        self.points = tuple(p)
        return self

    def open(self, open_polygon=True):
        """
        Creates an open polygon, rather than a closed polygon.

        Calling this method will cause the final polygon to be open - the last point will not be connected
        to the first point. To create a closed polygon, simply don't call this method.

        Args:
            open_polygon:  optional boolean - specifies if the shape should be open. Normally call `open()` with no
                parameter tio create an open polygon.

        Returns:
            self
        """
        self.closed = not open_polygon
        return self

    @property
    def side_len(self):
        """
        The side_len property gives the length of each side of the polygon. This is a readonly property
        calculated from the radius and numsides.
        """
        return 2*self.radius*math.sin(math.pi/self.numsides)

    @property
    def outer_radius(self):
        """
        The outer_radius property gives the radius of a circle, with the same centre as the polygon,
        that would pass through the vertices of the polygon. In other words, it is the smallest circle
        that completely encloses the polygon. This is a readonly property equal to the radius but it is
        included as a property for convenience.
        """
        return self.radius

    @property
    def interior_angle(self):
        """
        The interior_angle property gives the interior of the polygon. This is a readonly property
        calculated from numsides.
        """
        return (self.numsides-2)*math.pi/self.numsides

    @property
    def exterior_angle(self):
        """
        The exterior_angle property gives the exterior of the polygon. This is a readonly property
        calculated from numsides.
        """
        return 2*math.pi/self.numsides

    @property
    def inner_radius(self):
        """
        The inner_radius property gives the radius of a circle, with the same centre as the polygon,
        that would just touch the sides of the polygon. In other words, it is the largest circle that
        fits inside the polygon. This is a readonly property calculated from the radius and numsides.
        """
        return self.radius*math.cos(math.pi/self.numsides)

    @property
    def vertices(self):
        """
        The vertices property is a tuple containing the positions of the vertices of the polygon. Each
        vertex is stored as a tuple (x, y), so vertices is a tuple of tuples. This is a readonly property
        calculated from the centre, radius, and numsides.
        """
        return self.points


class Ellipse(Shape):
    """
    The Ellipse class draws ellipses, and elliptical arcs, sectors and segments.

    An ellipse is similar to a circle, but it has two radii, one in the x direction and one in the y direction.
    """
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
        """
        Creates a ellipse based on the centre point and the two radii.

        Args:
            center:  (number, number) - A tuple of two numbers, giving the (x, y) position of the centre of the ellipse.
            radius_x:  number - The x radius of the ellipse.
            radius_y:  number - The y radius of the ellipse.

        Returns:
            self
        """
        self.center = center
        self.radius_x = radius_x
        self.radius_y = radius_y
        return self

    def as_arc(self, start_angle, end_angle):
        """
        Modifies an ellipse, to show only an arc. An arc is part of the circumference of the ellipse.

        This is used as a modifier with of_center_radius, to draw just an arc. To draw an arc use:

        `Ellipse(ctx).of_center_radius((0, 0), 1).as_arc(0, 1).stroke(Color('black'), 0.1)`

        Angles are measured in radians. Angle zero lies along the positive x-axis, and the angle increases
        in the clockwise direction - note that this is opposite to the normal mathematical convention,
        where angle increases in the counterclockwise direction. The difference is due to the fact that y
        increases as you move down the image in generativepy.

        If you are using a flipped coordinate system (see the setup function in the drawing module),
        the angle increases in the counterclockwise direction.

        Since an arc is a line, you should normally use the stroke method to draw it. If you attempt to
        fill the arc, it will fill it as if it was a segment.

        Args:
            start_angle:  number - The start angle of the arc
            end_angle:  number - The end angle of the arc

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.arc
        return self

    def as_sector(self, start_angle, end_angle):
        """
        Modifies an ellipse, to show only a sector. A sector is a "pizza slice", like you would use
        in a pie chart.

        This function works in a similar way to the as_arc function, but it includes the area
        of the sector. You can fill or stroke the area.

        Args:
            start_angle:  number - The start angle of the sector
            end_angle:  number - The end angle of the sector

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.sector
        return self

    def as_segment(self, start_angle, end_angle):
        """
        Modifies an ellipse, to show only a segment. A segment is the part of the circle that is cut off by a chord.

        This function works in a similar way to the as_arc function, but it includes the area
        of the segment. You can fill or stroke the area.

        Args:
            start_angle:  number - The start angle of the segment
            end_angle:  number - The end angle of the segment

        Returns:
            self
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.type = Circle.segment
        return self

def ellipse(ctx, center, radius_x, radius_y):
    """
    Deprecated, use `Ellipse` class instead
    """
    Ellipse(ctx).of_center_radius(center, radius_x, radius_y).add()


class Marker(Shape):
    """
    Handles general line markers, such as arrows, ticks, dots etc.

    Markers are separate objects that can be added on top of existing line objects. Typically a marker is created
    like this:

    `Marker(ctx).of_XXX(...).as_XXX(...).fill(...).stroke(...)`

    The of_XXX determines the position of the marker, for example `of_points` positions the marker somewhere on a line between 2 points.

    The as_XXX determines the type of marker, for example `as_dot` creates a dot marker.

    Depending on the type of marker, it can then be filled, stroked, or both, as required.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.centre = None          #Calculated centre of marker
        self.parallel = None        #Unit vector pointing from start to end
        self.perpendicular = None   #Unit vector perpendicular to self.parallel
        self.draw_function = None
        self.type = None
        self.size = None
        self.count = None
        self.gap = None

    def of_points(self, start, end, position=0.5):
        """
        Specifies a marker on a straight line.

        The `start` and `end` of the line are specified as points. The centre of the marker can be positioned anywhere
        on the line using the `position` parameter. For example, 0 places the marker at the start, 1 places the marker at the end,
        0.25 places the marker a quarters of the from the start to the end.

        Args:
            start: 2-tuple - the position of the start of the line.
            end: 2-tuple - the position of the end of the line.
            position: number - the position of the centre of the marker along the line

        Returns:
            self
        """
        start = V(start)
        end = V(end)
        self.centre = start.lerp(end, position)
        self.parallel = (end - start).unit
        self.perpendicular = (-self.parallel[1], self.parallel[0])
        return self

    def of_circle(self, circle_centre, circle_radius, angle, clockwise=True):
        """
        Specifies a marker on a circle.

        The circle is specified by its centre and radius. The position of the marker is determined by the angle value.

        Args:
            circle_centre: 2-tuple - the position of the centre of the circle.
            circle_radius: number - the radius of the circle.
            angle: number - angle of the centre of the marker along the line, clockwise, started from +ve x direction, in radians
            clockwise: bool - true if arrow points clockwise, false for counterclockwise. Only applies to markers that have a direction.

        Returns:
            self
        """
        circle_centre = V(circle_centre)
        radius_vector = V.polar(circle_radius, angle)
        self.centre = circle_centre + radius_vector
        self.perpendicular = radius_vector.unit
        self.parallel = V(-self.perpendicular[1], self.perpendicular[0]) if clockwise else V(self.perpendicular[1], -self.perpendicular[0])
        return self

    def as_dot(self, size):
        """
        Creates a round dot marker of the required radius.

        For a simple dot marker, simply fill the shape with the required colour.

        For a different effect, you can fill and stroke the shape in different colours. For a "hollow" circle
        marker, fill the shape with the background colour and stroke it with the same colour and thickness as
        the line it is attached to.

        Args:
            size: number - the radius of the marker.

        Returns:
            self
        """
        self.type = "dot"
        self.size = size
        self.draw_function = self._draw_dot
        return self

    def as_tick(self, size, count=1, gap=2):
        """
        Creates a tick marker of the required size.

        The tick marker is a short line crossing the parent line at a right angle. In geometry it is often
        used to indicate that two lines have equal length.

        Setting `count` to 2 or 3 creates double ot triple markers that can be used iof multiple sets of equal
        lines exist. `gap` value controls the gap between the tick marks.

        Args:
            size: number - the length of the marker.
            count: number - the number of lines (1, 2, or 3).
            gap: number - the gap between the lines if `count` > 1.

        Returns:
            self
        """
        self.type = "tick"
        self.size = size
        self.count = count
        self.gap = gap
        self.draw_function = self._draw_tick
        return self

    def as_parallel(self, size, count=1, gap=2):
        """
        Creates a parallel marker of the required size.

        The tick marker is a small crossing the parent line at a right angle. In geometry it is often
        used to indicate that two lines are parallel.

        Setting `count` to 2 or 3 creates double ot triple markers that can be used iof multiple sets of parallel
        lines exist. `gap` value controls the gap between the tick marks.

        Args:
            size: number - the length of the marker.
            count: number - the number of lines (1, 2, or 3).
            gap: number - the gap between the lines if `count` > 1.

        Returns:
            self
        """
        self.type = "parallel"
        self.size = size
        self.count = count
        self.gap = gap
        self.draw_function = self._draw_parallel
        return self

    def _draw_dot(self):
        """
        Drawing function for dot shape. Used internally to the class.
        """
        self.ctx.arc(self.centre[0], self.centre[1], self.size, 0, 2 * math.pi)
        if self.final_close:
            self.ctx.close_path()

    def _draw_tick(self):
        """
        Drawing function for tick shape. Used internally in this method.
        """
        def _do_line(a, b):
            self.ctx.move_to(*a)
            self.ctx.line_to(*b)

        self.ctx.new_path()
        if self.count == 1:
            pos = (self.centre[0], self.centre[1])
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))
        elif self.count == 2:
            pos = (self.centre[0] - self.parallel[0] * self.gap / 2, self.centre[1] - self.parallel[1] * self.gap / 2)
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))
            pos = (self.centre[0] + self.parallel[0] * self.gap / 2, self.centre[1] + self.parallel[1] * self.gap / 2)
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))
        elif self.count == 3:
            pos = (self.centre[0] - self.parallel[0] * self.gap, self.centre[1] - self.parallel[1] * self.gap)
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))
            pos = (self.centre[0], self.centre[1])
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))
            pos = (self.centre[0] + self.parallel[0] * self.gap, self.centre[1] + self.parallel[1] * self.gap)
            _do_line((pos[0] + self.perpendicular[0] * self.size / 2, pos[1] + self.perpendicular[1] * self.size / 2),
                          (pos[0] - self.perpendicular[0] * self.size / 2, pos[1] - self.perpendicular[1] * self.size / 2))

    def _draw_parallel(self):
        """
        Drawing function for tick shape. Used internally in this method.
        """
        def _do_line(a, b, c):
            self.ctx.move_to(*b)
            self.ctx.line_to(*a)
            self.ctx.line_to(*c)

        self.ctx.new_path()
        if self.count == 1:
            pos = (self.centre[0], self.centre[1])
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))
        if self.count == 2:
            pos = (self.centre[0] - self.parallel[0] * self.gap / 2, self.centre[1] - self.parallel[1] * self.gap / 2)
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))
            pos = (self.centre[0] + self.parallel[0] * self.gap / 2, self.centre[1] + self.parallel[1] * self.gap / 2)
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))
        if self.count == 3:
            pos = (self.centre[0] - self.parallel[0] * self.gap, self.centre[1] - self.parallel[1] * self.gap)
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))
            pos = (self.centre[0], self.centre[1])
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))
            pos = (self.centre[0] + self.parallel[0] * self.gap, self.centre[1] + self.parallel[1] * self.gap)
            _do_line(pos, (pos[0] + (-self.parallel[0] + self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] + self.perpendicular[1]) * self.size / 2),
                     (pos[0] + (-self.parallel[0] - self.perpendicular[0]) * self.size / 2, pos[1] + (-self.parallel[1] - self.perpendicular[1]) * self.size / 2))

    def add(self):
        self._do_path_()
        self.draw_function()
        return self


class AngleMarker(Shape):
    """
    The AngleMarker class is a special Shape that draws an angle marker.

    An AngleMarker can have 1, 2 or 3 arcs. The 2 and 3 arc forms are often used to indicate that two angles are
    equal. You can also draw a right angle marker, as shown.

    The AngleMarker only draws the arcs, it doesn't draw the lines that make up the angle. These would normally be
    drawn using a Line object, Polygon object, or similar.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.a = (0, 0)
        self.b = (0, 0)
        self.c = (0, 0)
        self.radius = 8
        self.count = 1
        self.gap = 2
        self.right_angle = False

    def add(self):
        self._do_path_()
        ang1 = math.atan2(self.a[1] - self.b[1], self.a[0] - self.b[0])
        ang2 = math.atan2(self.c[1] - self.b[1], self.c[0] - self.b[0])
        if self.right_angle:
            self.radius /= 1.4
            v = (math.cos(ang1), math.sin(ang1))
            pv = (math.cos(ang2), math.sin(ang2))
            polygon(self.ctx, [(self.b[0] + v[0] * self.radius, self.b[1] + v[1] * self.radius),
                               (self.b[0] + (v[0] + pv[0]) * self.radius, self.b[1] + (v[1] + pv[1]) * self.radius),
                               (self.b[0] + pv[0] * self.radius, self.b[1] + pv[1] * self.radius)], False)
        elif self.count == 2:
            self.ctx.arc(self.b[0], self.b[1], self.radius - self.gap / 2, ang1, ang2)
            self.ctx.new_sub_path()
            self.ctx.arc(self.b[0], self.b[1], self.radius + self.gap / 2, ang1, ang2)
        elif self.count == 3:
            self.ctx.arc(self.b[0], self.b[1], self.radius - self.gap, ang1, ang2)
            self.ctx.new_sub_path()
            self.ctx.arc(self.b[0], self.b[1], self.radius, ang1, ang2)
            self.ctx.new_sub_path()
            self.ctx.arc(self.b[0], self.b[1], self.radius + self.gap, ang1, ang2)
        else:
            self.ctx.arc(self.b[0], self.b[1], self.radius, ang1, ang2)
        return self

    def of_points(self, a, b, c):
        """
        Creates a marker based on 3 points.

        This will draw an angle marker for the angle formed by abc. The angle will be start at the line **ab**
        and be drawn in a clockwise direction to the line **cb**, with point b as the centre of the angle.

        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of point a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of point b.
            c:  (number, number) - A tuple of two numbers, giving the (x, y) position of point c.

        Returns:
            self
        """
        self.a = a
        self.b = b
        self.c = c
        return self

    def with_radius(self, radius):
        """
        Sets the radius of the arc. Default 8

        Args:
            radius:  number - Radius of arc in user units.

        Returns:
            self
        """
        self.radius = radius
        return self

    def with_count(self, count):
        """
        Sets the number of arcs in the marker. Default 1. permitted values are 1, 2 or 3.

        Args:
            count:  number - Number of arcs

        Returns:
            self
        """
        self.count = count
        return self

    def with_gap(self, gap):
        """
        Sets the gap between the arcs if `count` > 1.

        Sets the spacing of the arcs. This is only relevant if there is more than one arc (ie if count > 1), otherwise
        it is ignored.The default is 2.

        For double of triple arcs, the set of arcs is centred on the requested radius. So for example if radius is
        8 and gap is 2, and 3 arcs are specified, the arcs will have radii of 6, 8, and 10.

        Args:
            gap:  number - Gap between arcs in user units.

        Returns:
            self
        """
        self.gap = gap
        return self

    def as_right_angle(self, right_angle=True):
        """
        Marks the angle as a right angle.

        Normally you should call this method, with no parameter, to draw a right angle. To draw a normal angle marker don't call
        this function at all. The parameter is not needed unless you specifically want to use a flag to control the marker.

        Note that if a right angle is selected, the marker will attempt to draw a right angle symbol even if the angle isn't
        actually 90 degrees. This will create a strange effect. Only choose the right angle option if the angle is actually
        close to 90 degrees.

        Args:
            right_angle:  bool - Draws the angle as a right angle.

        Returns:
            self
        """
        self.right_angle = right_angle
        return self


class TickMarker(Shape):
    """
    Deprecated - use the `Marker` class instead.

    The TickMarker class is a special Shape that draws a tick mark (a small line) across an existing line.

    An TickMarker can have 1, 2 or 3 ticks. It is normally used to indicate that two or more lines are the same length.

    The TickMarker only draws the ticks, it doesn't draw the line itself. That would normally be
    drawn using a Line object, Polygon object, or similar.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.a = (0, 0)
        self.b = (0, 0)
        self.length = 4
        self.count = 1
        self.gap = 1

    def add(self):
        self._do_path_()
        pmid = ((self.a[0] + self.b[0]) / 2, (self.a[1] + self.b[1]) / 2)
        # self.length of line
        l = math.sqrt((self.a[0] - self.b[0]) * (self.a[0] - self.b[0]) + (self.a[1] - self.b[1]) * (self.a[1] - self.b[1]))
        # Unit vector along line
        # Draw a tick on a line - deprecated, use TickMarker class instead
        vector = ((self.b[0] - self.a[0]) / l, (self.b[1] - self.a[1]) / l)
        # Unit vector perpendicular to line
        pvector = (-vector[1], vector[0])

        self.ctx.new_path()
        if self.count == 1:
            pos = (pmid[0], pmid[1])
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
        elif self.count == 2:
            pos = (pmid[0] - vector[0] * self.gap / 2, pmid[1] - vector[1] * self.gap / 2)
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
            pos = (pmid[0] + vector[0] * self.gap / 2, pmid[1] + vector[1] * self.gap / 2)
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
        elif self.count == 3:
            pos = (pmid[0] - vector[0] * self.gap, pmid[1] - vector[1] * self.gap)
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
            pos = (pmid[0], pmid[1])
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
            pos = (pmid[0] + vector[0] * self.gap, pmid[1] + vector[1] * self.gap)
            self._do_line((pos[0] + pvector[0] * self.length / 2, pos[1] + pvector[1] * self.length / 2),
                          (pos[0] - pvector[0] * self.length / 2, pos[1] - pvector[1] * self.length / 2))
        return self

    def of_start_end(self, a, b):
        """
        Creates a marker based on 2 points.

        This will draw a mark for the line formed by ab. The mark will be half way between a and b.

        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of point a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of point b.

        Returns:
            self
        """
        self.a = a
        self.b = b
        return self

    def with_length(self, length):
        """
        Sets the length of the marker. Default 4

        Args:
            length:  number - Length of the marker in user units.

        Returns:
            self
        """
        self.length = length
        return self

    def with_count(self, count):
        """
        Sets the number of marks. Default 1. Permitted values are 1, 2 or 3.

        Args:
            * count:  number - Number of marks

        Returns:
            self
        """
        self.count = count
        return self

    def with_gap(self, gap):
        """
        Sets the gap between the marks if `count` > 1.

        Sets the spacing of the marks. This is only relevant if there is more than one arc (ie if count > 1), otherwise
        it is ignored.The default is 2.

        Args:
            gap:  number - Gap between marks in user units.

        Returns:
            self
        """
        self.gap = gap
        return self

    def _do_line(self, a, b):
        self.ctx.move_to(*a)
        self.ctx.line_to(*b)


class ParallelMarker(Shape):
    """
    Deprecated - use the `Marker` class instead.

    The ParallelMarker class is a special Shape that draws an arrow mark across an existing line.

    An ParallelMarker can have 1, 2 or 3 arrows. It is normally used to indicate that two or more lines are the parallel.

    The ParallelMarker only draws the arrows, it doesn't draw the line itself. That would normally be
    drawn using a Line object, Polygon object, or similar.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.a = (0, 0)
        self.b = (0, 0)
        self.length = 4
        self.count = 1
        self.gap = 1

    def add(self):
        self._do_path_()
        # Midpoint of line
        pmid = ((self.a[0] + self.b[0]) / 2, (self.a[1] + self.b[1]) / 2)
        # self.length of line
        l = math.sqrt((self.a[0] - self.b[0]) * (self.a[0] - self.b[0]) + (self.a[1] - self.b[1]) * (self.a[1] - self.b[1]))
        # Unit vector along line
        vector = ((self.b[0] - self.a[0]) / l, (self.b[1] - self.a[1]) / l)
        # Unit vector perpendicular to line
        pvector = (-vector[1], vector[0])

        self.ctx.new_path()
        if self.count == 1:
            pos = (pmid[0], pmid[1])
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
        elif self.count == 2:
            pos = (pmid[0] - vector[0] * self.gap / 2, pmid[1] - vector[1] * self.gap / 2)
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
            pos = (pmid[0] + vector[0] * self.gap / 2, pmid[1] + vector[1] * self.gap / 2)
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
        elif self.count == 3:
            pos = (pmid[0] - vector[0] * self.gap, pmid[1] - vector[1] * self.gap)
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
            pos = (pmid[0], pmid[1])
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
            pos = (pmid[0] + vector[0] * self.gap, pmid[1] + vector[1] * self.gap)
            self._do_draw(pos[0], pos[1], (-vector[0] + pvector[0]) * self.length / 2, (-vector[1] + pvector[1]) * self.length / 2,
                          (-vector[0] - pvector[0]) * self.length / 2, (-vector[1] - pvector[1]) * self.length / 2)
        return self

    def of_start_end(self, a, b):
        """
        Creates a marker based on 2 points.

        This will draw a mark for the line formed by ab. The mark will be half way between a and b.

        Args:
            a:  (number, number) - A tuple of two numbers, giving the (x, y) position of point a.
            b:  (number, number) - A tuple of two numbers, giving the (x, y) position of point b.

        Returns:
            self
        """
        self.a = a
        self.b = b
        return self

    def with_length(self, length):
        """
        Sets the length of the marker. Default 4

        Args:
            length:  number - Length of the marker in user units.

        Returns:
            self
        """
        self.length = length
        return self

    def with_count(self, count):
        """
        Sets the number of marks. Default 1. Permitted values are 1, 2 or 3.

        Args:
            * count:  number - Number of marks

        Returns:
            self
        """
        self.count = count
        return self

    def with_gap(self, gap):
        """
        Sets the gap between the marks if `count` > 1.

        Sets the spacing of the marks. This is only relevant if there is more than one arc (ie if count > 1), otherwise
        it is ignored.The default is 2.

        Args:
            gap:  number - Gap between marks in user units.

        Returns:
            self
        """
        self.gap = gap
        return self

    def _do_draw(self, x, y, ox1, oy1, ox2, oy2):
        self.ctx.move_to(x, y)
        self.ctx.line_to(x + ox1, y + oy1)
        self.ctx.move_to(x, y)
        self.ctx.line_to(x + ox2, y + oy2)



def angle_marker(ctx, a, b, c, count=1, radius=8, gap=2, right_angle=False):
    """
    Deprecated - use the `Marker` class instead.
    """
    AngleMarker(ctx).of_points(a, b, c).with_count(count).with_radius(radius).with_gap(gap).as_right_angle(right_angle).add()

def tick(ctx, a, b, count=1, length=4, gap=1):
    """
    Deprecated - use the `Marker` class instead.
    """
    TickMarker(ctx).of_start_end(a, b).with_count(count).with_length(length).with_gap(gap).add()

def paratick(ctx, a, b, count=1, length=4, gap=1):
    """
    Deprecated - use the `Marker` class instead.
    """
    ParallelMarker(ctx).of_start_end(a, b).with_count(count).with_length(length).with_gap(gap).add()

def arrowhead(ctx, a, b, length=4):

    def draw(x, y, ox1, oy1, ox2, oy2):
        ctx.move_to(x + ox1, y + oy1)
        ctx.line_to(x, y)
        ctx.line_to(x + ox2, y + oy2)

    # Length of line
    l = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / l, (b[1] - a[1]) / l)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    ctx.new_path()
    draw(b[0], b[1], (-vector[0] + pvector[0]) * length / 2, (-vector[1] + pvector[1]) * length / 2,
         (-vector[0] - pvector[0]) * length / 2, (-vector[1] - pvector[1]) * length / 2)

class Image():
    """
    The Image class renders an image on a drawing context.

    This is intended for very simple display of images:

    * The image must be available as a PNG file.
    * The full image will be rendered as a rectangle, the same size as the original image.
    * The image can optionally be scaled by a factor.

    The rendered image size in user space units will match the pixel size of the original PNG image.

    The image can be transformed using standard PyCairo context calls, so you can rotate, mirror, stretch or shear the image.
    You can also apply a clip path prior to rendering the image, to change its shape. Transparent PNG images are supported.

    `Image` is not derived from `Shape`, so it doesn't inherit any of its methods.
    """

    def __init__(self, ctx):
        """
        Args:

        * ctx: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.ctx = ctx
        self.image = None
        self.position = (0, 0)
        self.scale_factor = 1

    @staticmethod
    def load_image(filename):
        """
        Load and image into an image surface. This is a static helper method that can be used to preload an image for the
        `of_file_position` function, if the same image is being rendered multiple times.

        Args:
            filename: str - Path of file containing image.

        Returns:
            Pycairo ImageSurface object containing the image.
        """
        return cairo.ImageSurface.create_from_png(filename)

    def of_file_position(self, image, position):
        """
        Specifies an image file and a position.

        By default, the image will be rendered with its top left corner at `position`. If user space is mirrored or
        rotated, it may appear differently on the page.

        There are two ways to pass an image into this function:

        * `image` can specify the filepath to a PNG file.
        * `image` can specify a Pycairo ImageSurface containing an image.

        The first method is usually used. However, if you need to render the same image many times, this method
        can be quite slow because it reads the file every time. In that case, you can use the `load_image` mathod to
        preload an image into an ImageSurface, and then pass that into this function.

        Args:
            image: str or Pycairo ImageSurface - The iamge.
            position:  (number, number) - A tuple of two numbers, giving the required (x, y) position the image.

        Returns:
            self
        """
        self.image = image
        self.position = position
        return self

    def scale(self, scale_factor):
        """
        Sets the image scale factor.

        Scales the image by a factor. For example, a factor of 2 will make the image appear twice as big on the page.
        If this function is not called, a scale factor of 1 is used by default.

        This scale factor is applied prior to any scaling of the userspace.

        Args:
            scale_factor: number - The image scale factor.

        Returns:
            self
        """
        self.scale_factor = scale_factor
        return self

    def paint(self):
        """
        Renders the image.

        Returns:
            self
        """
        image = cairo.ImageSurface.create_from_png(self.image) if isinstance(self.image, str) else self.image
        self.ctx.save()
        self.ctx.translate(*self.position)
        self.ctx.scale(self.scale_factor, self.scale_factor)
        pattern = cairo.SurfacePattern(image)
        self.ctx.set_source(pattern)
        self.ctx.rectangle(0, 0, image.get_width(), image.get_height())
        self.ctx.fill()
        self.ctx.restore()
        return self

class Turtle():
    """
    The Turtle class implements a simple turtle graphics system.

    A turtle graphics system uses a graphics cursor that can draw lines as it moves around.

    The cursor has an (x, y) position, and also a direction it is pointing in (the heading). You can tell the turtle to
    move forward by a certain distance, or to turn through a certain angle to the left or right. By issuing a series of
    instructions, you can draw various shapes.

    To allow for recursive drawing (eg to create fractal images) turtle graphics can push the current state onto a stack.
    At some later stage it can pop its previous state (position and heading) and continue from there.

    The turtle can also move to different place without drawing anything.

    It is possible to change the colour, thickness and dash style of the lines the turtle draws.

    More than one turtle can be active at the same time, simply by creating more than one turtle object.
    """

    def __init__(self, ctx):
        """
        Args:

        * ctx: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.ctx = ctx
        self.heading = 0
        self.x = 0
        self.y = 0
        self.color = itertools.cycle((Color(0),))
        self.line_width = 1
        self.dash = []
        self.cap = SQUARE
        self.stack = []

    def push(self):
        """
        Pushes the current turtle state (heading, position, and line style) onto a stack.

        Returns:
            self
        """
        state = self.heading, self.x, self.y, self.color, self.line_width, self.dash, self.cap
        self.stack.append(state)
        return self

    def pop(self):
        """
        Pops the current turtle state (heading, position, and line style) from a stack.

        Returns:
            self
        """
        state = self.stack.pop()
        self.heading, self.x, self.y, self.color, self.line_width, self.dash, self.cap = state
        return self

    def forward(self, distance):
        """
        Moves the turtle forward, in its current heading direction, and draw a line in the current style.

        Args:
            distance: number - The distance to move.

        Returns:
            self
        """
        p1 = self.x, self.y
        self.x += distance*math.cos(self.heading)
        self.y += distance*math.sin(self.heading)
        Line(self.ctx).of_start_end(p1, (self.x, self.y)) \
            .stroke(next(self.color), line_width=self.line_width, dash=self.dash, cap=self.cap)
        return self

    def move(self, distance):
        """
        Moves the turtle forward, in its current heading direction without drawing a line.

        Args:
            distance: number - The distance to move.

        Returns:
            self
        """
        self.x += distance*math.cos(self.heading)
        self.y += distance*math.sin(self.heading)
        return self

    def move_to(self, x, y):
        """
        Moves the turtle to a new position without drawing a line.

        Args:
            x: number - x position to move to
            y: number - y position to move to

        Returns:
            self
        """
        self.x = x
        self.y = y
        return self

    def left(self, angle):
        """
        Change the current heading by moving to the left (ie counterclockwise)

        Args:
            angle: number - Angles to move through

        Returns:
            self
        """
        self.heading -= angle
        return self

    def right(self, angle):
        """
        Change the current heading by moving to the right (ie clockwise)

        Args:
            angle: number - Angles to move through

        Returns:
            self
        """
        self.heading += angle
        return self

    def set_heading(self, angle):
        """
        Change the current heading to a new angle

        Args:
            angle: number - New heading angle.

        Returns:
            self
        """
        self.heading = angle
        return self

    def set_style(self, color=Color(0), line_width=1, dash=None, cap=SQUARE):
        """
        Set the line style.

        The parameters are as described for the `StrokeParams` object, except that the `color` parameter can accept a sequence.

        Args:
            color: `Color` or sequence of `Color` objects - The `Color` to use for the line, None for default. If a sequence of colours is provided, each
                new `forward` call will cycle through the colors in sequence.
            line_width: width of stroke line. None for default
            dash: sequence, dash patter of line. None for default
            cap: line end style, None for default.

        Returns:
            self
        """
        if isinstance(color, Color):
            # Single color, create a 1 element tuple and cycle over it
            self.color = itertools.cycle((color,))
        else:
            # Sequence of colors, cycle over colours
            self.color = itertools.cycle(color)
        self.line_width = line_width
        if not dash:
            self.dash = []
        else:
            self.dash = dash
        self.cap = cap
        return self

class Transform():
    """
    The Transform class transforms the user space, affecting all subsequent drawing operations. Several
    transformations are provided:

    * `translate` shifts user space in the x and y directions, so that object will drawn in a new position.
    * `scale` scales user space, so that objects will be drawn larger or smaller. It is possible to scale x and y by
      different amounts, and to centre the scaling on any point.
    * `rotate` rotates user space, so that object will be drawn rotated. It is possible to rotate the space around any point.
    * `matrix` applies a general transformation matrix. This can be used to apply any affine transformation.

    Flipping and shearing can also be applied with the above operators, as described below.

    Multiple transforms can be applied at the same time, for example it is possible to rotate and scale at the same time.

    Transforms affect every aspect of the drawing, including:

    * Shape objects.
    * Image objects.
    * Line thickness and dash pattern.
    * Patterns (eg gradients).

    The Transform object is a context manager, intended to be used in a `with` block. The `with` block determines when the transform
    will apply. The transformn applies to anythuing drwan within the with block. On leaving the wih block, the transfromno longer applies.
    """

    def __init__(self, ctx):
        """
        Args:

        * ctx: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.ctx = ctx
        self.ctx.save()
        self.active = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.ctx.restore()
            self.active = False
        else:
            raise RuntimeError('Transform exit called twice')

    def scale(self, sx, sy, centre=(0, 0)):
        """
        Scales user space.

        This scales user space. Anything drawn in the new user space will change size by a factor of `sx` in the x
        direction and `sy` in the y direction. `centre` is the fixed point. By default it is the origin.

        Args:
            sx: number - Scale in the x direction.
            sy: number - Scale in the x direction.
            centre: (number, number) - Centre of scaling

        Returns:
            self
        """
        self.ctx.translate(centre[0], centre[1])
        self.ctx.scale(sx, sy)
        self.ctx.translate(-centre[0], -centre[1])
        return self

    def rotate(self, angle, centre=(0, 0)):
        """
        Rotates user space.

        This rotates user space. Anything drawn in the new user space will rotated around centre. `centre is the fixed point. By default it is the origin.

        Args:
            angle: number - Rotation angle, clockwise, in radians.
            centre`: (number, number) - Centre of scaling

        Returns:
            self
        """
        self.ctx.translate(centre[0], centre[1])
        self.ctx.rotate(angle)
        self.ctx.translate(-centre[0], -centre[1])
        return self

    def translate(self, tx, ty):
        """
        Translates user space.

        This translates user space. Anything drawn in the new user space will be shifted by `(tx, ty)`.

        Args:
            tx: number - Translate in the x direction.
            ty: number - Translate in the x direction.

        Returns:
            self
        """
        self.ctx.translate(tx, ty)
        return self

    def matrix(self, m):
        """
        Applies a transformation matrix to user space.

        Args:
            m: tuple of 6 numbers - Transform matrix

        Returns:
            self
        """
        # Convert the generativepy.math.matrix to a cairo.Matrix
        new_matrix = cairo.Matrix(m[0], m[1], m[3], m[4], m[2], m[5])
        old_matrix = self.ctx.get_matrix()
        self.ctx.set_matrix(new_matrix*old_matrix)
        return self
