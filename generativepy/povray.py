# Author:  Martin McBride
# Created: 2023-12-02
# Copyright (C) 2022, Martin McBride
# License: MIT
"""
povray module uses the Povray application to render 3D images.

It uses the Vapory Python library to allow scenes to be described in Python.

This module also provides 3d axes, function plotting, and default camera and light configurations.
"""
import numpy as np

from generativepy.color import Color
from generativepy.math import Vector as V
from vapory import Camera, LightSource, Background, Scene, Texture, Pigment, Finish, Cylinder, Union, Text
import math

def get_color(color):
    """
    Convert a generativepy `Color` object into a Povray color.

    A Povray is a list of 4 values, however the alpha component works differently. In generativepy alpha 1 is fully opaque and
    0 is fully transparent. In Povray alpha 0 is fully opaque and 1 is fully transparent.

    Args:
        color: `Color` object - the color.

    Returns:
        A Povray color as a 4-tuple
    """
    return color[0], color[1], color[2], 1 - color[3]

class Camera3d:
    """
    Creates a Povray camera, at a particlular location, looking at the origin
    """

    def __init__(self):
        self.x = 5
        self.y = 0
        self.z = 0
        self.lookat = (0, 0, 0)

    def position(self, x, y, z):
        """
        Set the position in x, y, z space

        Args:
            x: number - the x position of the camera.
            y: number - the y position of the camera.
            z: number - the y position of the camera.

        Returns:
            self
        """
        self.x = x
        self.y = y
        self.z = z
        return self

    def polar_position(self, distance, angle, elevation):
        """
        Set the position in polar coordinates

        Args:
            distance: number - the distance of the camera from the origin.
            angle: number - the horizontal angle of the camera.
            elevation: number - the elevation angle of the camera.

        Returns:
            self
        """
        self.x = distance * math.cos(angle)
        self.y = distance * math.sin(angle)
        self.z = distance * math.sin(elevation)
        return self

    def standard_plot(self):
        """
        Set the position to view a standard plot

        Returns:
            self
        """
        self.x = 5
        self.y = 1
        self.z = -5
        return self

    def get(self):
        """
        Gets the configured Camera object

        Returns:
            A Vapory Camera object
        """
        return Camera(
            "location",
            [self.x, self.y, self.z],
            "look_at",
            self.lookat
        )


class Lights3d:
    """
    Creates a set of lights for the scene.
    """
    def __init__(self):
        self.lights = ()

    def standard(self, color=Color(1)):
        """
        Adds two lights at fixed positions, suitable for a typical scene.
        Args:
            color: `Color` object - the light colour, default white.

        Returns:
            self
        """
        self.lights = (
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, 5]),
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, -5])
        )
        return self

    def standard_plot(self, color=Color(1)):
        """
        Adds two lights at fixed positions, suitable for a standard 3D plot.
        Args:
            color: `Color` object - the light colour, default white.

        Returns:
            self
        """
        self.lights = (
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, 5]),
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, -5])
        )
        return self

    def get(self):
        """
        Gets the configured Light objects

        Returns:
            A tuple of Vapory Light objects
        """
        return self.lights

class Scene3d:
    """
    Creates a 3D Vapory scene, adding a camera, lights, and a collection of objects.
    """

    def __init__(self):
        self.camera_item = None
        self.background_color = Color(1)
        self.content = []

    def camera(self, camera):
        """
        Add a camera.

        Args:
            camera: Vapory camera object - the camera.

        Returns:
            self
        """
        self.camera_item = camera
        return self

    def background(self, color):
        self.background_color = Color(1)
        return self

    def add(self, items):
        """
        Add a set of items. Items can include 3D models and lights.

        Args:
            items: tuple of Vapory items - the scene items.

        Returns:
            self
        """
        self.content.extend(items)
        return self

    def get(self):
        """
        Gets the configured Scene object

        Returns:
            A Vapory Scene object
        """
        return Scene(self.camera_item, [Background("color", get_color(self.background_color))] + self.content)


class Axes3d:
    """
    Represents a set of 3D axes, including labels.
    """

    def __init__(self):
        self.position = (-2,)*3
        self.size = (4,)*3
        self._start = (-2,) * 3
        self.end = None
        self._extent = (4,) * 3
        self.divisions = (0.5,)*3
        self.div_positions = None
        self.axis_thickness = 0.02
        self.color = Color("blue").light1
        self.texture = None
        self.division_formatters = (None,)*3

    @property
    def start(self):
        """Start of x, y, z range"""
        return self._start

    @property
    def extent(self):
        """Extent of x, y, z range"""
        return self._extent

    def of_start(self, start):
        """
        The start coordinates.

        Args:
            start: tuple(number, number, number) - start value of x, y, z axes

        Returns:
            self
        """
        self._start = tuple(start)
        return self

    def of_extent(self, extent):
        """
        The coordinate extents.

        Args:
            extent: tuple(number, number, number) - length of x, y, z axes

        Returns:
            self
        """
        self._extent = tuple(extent)
        return self

    def with_divisions(self, divisions):
        """
        The division spacing for each axis.

        Args:
            divisions: tuple(number, number, number) - division spacing of x, y, z axes

        Returns:
            self
        """
        self.divisions = tuple(divisions)
        return self

    def with_division_formatters(self, formatters):
        """
        The division label formatters for each axis.

        A formatter is a function that accepts 2 values:

        * `value`: number - the division value
        * `div`: number - the division spacing

        Args:
            formatters: tuple(function, function, function) - formatter functions for x, y, z axes.

        Returns:
            self
        """
        self.division_formatters = tuple(formatters)
        return self

    def transform_from_graph(self, point):
        """
        Transform a point from graph space to Povray space.

        Args:
            point: 3-tuple, the point in graph coordinates.

        Returns:
            Transformed point as a 3-tuple
        """
        x = ((point[0] - self._start[0]) * self.size[0] / (self.end[0] - self._start[0])) + self.position[0]
        y = ((point[1] - self._start[1]) * self.size[1] / (self.end[1] - self._start[1])) + self.position[1]
        z = ((point[2] - self._start[2]) * self.size[2] / (self.end[2] - self._start[2])) + self.position[2]
        return x, y, z

    def division_linestyle(self, pattern=Color(0), line_width=None):
        """
        Sets the linestyle for axis division lines

        Args:
            pattern: `Color` object  - line colour.
            line_width: number - width of line in Povray units.

        Returns:
            self
        """
        self.color = pattern
        if line_width is not None:
            self.axis_thickness = line_width
        return self

    def _make_xy_planes(self):
        items = []

        xstart = [p for p in self.div_positions[0]]
        xend = xstart
        ystart = [self._start[1] for p in self.div_positions[0]]
        yend = [self.end[1] for p in self.div_positions[0]]
        zstart = [self._start[2] for p in self.div_positions[0]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[0]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self._start[0] for p in self.div_positions[1]]
        xend = [self.end[0] for p in self.div_positions[1]]
        ystart = [p for p in self.div_positions[1]]
        yend = ystart
        zstart = [self._start[2] for p in self.div_positions[1]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[1]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        return items

    def _make_xz_planes(self):
        items = []

        xstart = [p for p in self.div_positions[0]]
        xend = xstart
        ystart = [self._start[1] for p in self.div_positions[0]]
        yend = ystart
        zstart = [self._start[2] for p in self.div_positions[0]]
        zend = [self.end[2] for p in self.div_positions[0]]
        for i, _ in enumerate(self.div_positions[0]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self._start[0] for p in self.div_positions[2]]
        xend = [self.end[0] for p in self.div_positions[2]]
        ystart = [self._start[1] for p in self.div_positions[2]]
        yend = ystart
        zstart = [p for p in self.div_positions[2]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[2]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        return items

    def _make_yz_planes(self):
        items = []

        xstart = [self._start[0] for p in self.div_positions[2]]
        xend = xstart
        ystart = [self._start[1] for p in self.div_positions[2]]
        yend = [self.end[1] for p in self.div_positions[2]]
        zstart = [p for p in self.div_positions[2]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[2]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self._start[0] for p in self.div_positions[1]]
        xend = xstart
        ystart = [p for p in self.div_positions[1]]
        yend = ystart
        zstart = [self._start[2] for p in self.div_positions[1]]
        zend = [self.end[2] for p in self.div_positions[1]]
        for i, _ in enumerate(self.div_positions[1]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        return items

    def _make_axis_box(self):
        sx, sy, sz = self.position
        ex, ey, ez = [e + s for e, s in zip(self.size, self.position)]
        items = [
            Cylinder((sx, sy, sz), (ex, sy, sz), self.axis_thickness, self.texture),
            Cylinder((sx, sy, sz), (sx, ey, sz), self.axis_thickness, self.texture),
            Cylinder((sx, sy, sz), (sx, sy, ez), self.axis_thickness, self.texture),
            Cylinder((ex, sy, sz), (ex, ey, sz), self.axis_thickness, self.texture),
            Cylinder((ex, sy, sz), (ex, sy, ez), self.axis_thickness, self.texture),
            Cylinder((sx, ey, sz), (ex, ey, sz), self.axis_thickness, self.texture),
            Cylinder((sx, ey, sz), (sx, ey, ez), self.axis_thickness, self.texture),
            Cylinder((sx, sy, ez), (ex, sy, ez), self.axis_thickness, self.texture),
            Cylinder((sx, sy, ez), (sx, ey, ez), self.axis_thickness, self.texture),
        ]

        return items

    def _format_div(self, value, div, formatter=None):
        """
        Formats a division value into a string.
        If a formatter is supplied it will be used to convert the value top a string.
        If the division spacing is an integer, the string will be an integer (no dp).
        If the division spacing is float, the string will be rounded to 3 decimal places

        Args:
            value: number - value to be formatted
            div: number - division spacing
            formatter: formatting function - accepts vale and div, returns a formatted value string

        Returns:
            String representation of the value
        """
        if formatter:
            return formatter(value, div)

        if isinstance(value, int):
            return str(value)
        return str(round(value*1000)/1000)

    def _make_text_item(self, text, pos, offset, rotation=(90, 0, 0)):
        text = Text(
        "ttf",
             '"/usr/share/fonts/truetype/msttcorefonts/ariali.ttf"',
             f'"{text}"',  # Povray requires "" around text
             0.1,
             0,
            self.texture,
            "rotate",
            rotation,
            "translate",
            offset,
            "scale",
            0.2,
        )
        return Union(text, "translate",
            pos,)

    def _make_labels(self):
        items = []

        for p in self.div_positions[0]:
            s = self._format_div(p, self.divisions[0], self.division_formatters[0])
            p = self.transform_from_graph((p, 0, 0))[0]
            if -1.8 < p < 1.8:
                items.append(self._make_text_item(s, (p, 2.3, -2), (-0.5, 0, -1), (90, 0, -90)))
        for p in self.div_positions[1]:
            s = self._format_div(p, self.divisions[1], self.division_formatters[1])
            p = self.transform_from_graph((0, p, 0))[1]
            if -1.8 < p < 1.8:
                items.append(self._make_text_item(s, (2, p, -2), (0, 0, -1)))
        for p in self.div_positions[2]:
            s = self._format_div(p, self.divisions[2], self.division_formatters[1])
            p = self.transform_from_graph((0, 0, p))[2]
            if -1.8 < p < 1.8:
                items.append(self._make_text_item(s, (2, -2, p), (0.5, 0, 0)))

        return items

    def _make_axes(self):
        return Union(
            *self._make_xy_planes(),
            *self._make_xz_planes(),
            *self._make_yz_planes(),
            *self._make_axis_box(),
            *self._make_labels(),
            "rotate",
            [-90, 0, 0],
            "translate",
            [0, 0.5, 0],
            "no_shadow"
        )

    def _get_divs(self, start, end, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= end:
            divs.append(n)
            n += div
        return divs

    def get(self):
        """
        Gets the axes object

        Returns:
            A Vapory Union object thtat draws the axes
        """
        self.texture = Texture(Pigment("color", get_color(self.color)), Finish("ambient", 1, "diffuse", 0))
        self.end = [ex + s for ex, s in zip(self._extent, self._start)]
        self.div_positions = [self._get_divs(self._start[i], self.end[i], self.divisions[i]) for i in range(3)]
        return self._make_axes()


class Plot3dZofXY:

    def __init__(self, axes):
        self.axes = axes
        self.start = (axes.start[0], axes.start[1])
        self.end = (axes.extent[0] + axes.start[0], axes.extent[1] + axes.start[1])
        self.steps = 40
        self.grid_factor = 5
        self.func = lambda x, y: math.cos(math.sqrt((x**2 + y**2))*2)
        self.color = Color("lightgreen")
        self.line_color = Color("green")
        self.line_thickness = 0.02

    def function(self, f):
        self.func = f
        return self

    def grid_linestyle(self, pattern=Color(0), line_width=None):
        """
        Sets the linestyle for plot mesh lines

        Args:
            pattern: `Color` object - line colour.
            line_width: number 0 width of line in Povray units.

        Returns:
            self
        """
        self.line_color = pattern
        if line_width is not None:
            self.line_thickness = line_width
        return self

    def fill(self, pattern=Color(0)):
        """
        Sets the fill for the plot

        Args:
            pattern: - `Color` object, fill colour.

        Returns:
            self
        """
        self.color = pattern
        return self

    def _convert_points(self, x, y, z):
        self.axes.end = [ex + s for ex, s in zip(self.axes.extent, self.axes.start)]
        x = ((x - self.axes._start[0]) * self.axes.size[0] / (self.axes.end[0] - self.axes._start[0])) + self.axes.position[0]
        y = ((y - self.axes._start[1]) * self.axes.size[1] / (self.axes.end[1] - self.axes._start[1])) + self.axes.position[1]
        z = ((z - self.axes._start[2]) * self.axes.size[2] / (self.axes.end[2] - self.axes._start[2])) + self.axes.position[2]
        return x, y, z

    def get(self):
        """
        Gets the plot object

        Returns:
            A Vapory Union object that draws the plot
        """
        x = np.linspace(self.start[0], self.end[0], self.steps)
        y = np.linspace(self.start[1], self.end[1], self.steps)
        xx, yy = np.meshgrid(x, y)
        vf = np.vectorize(self.func)
        ff = vf(xx, yy)

        vf = np.vectorize(self._convert_points)
        xx, yy, ff = vf(xx, yy, ff)

        mesh = ["mesh {\n"]
        for i in range(self.steps - 1):
            for j in range(self.steps - 1):
                mesh.append("triangle {" f"<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
                mesh.append("triangle {" f"<{xx[i+1, j+1]}, {yy[i+1, j+1]}, {ff[i+1, j+1]}>,<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
        texture = Texture(Pigment("color", get_color(self.color)), Finish("ambient", 0.5, "diffuse", 0.5))
        mesh.append(str(texture))
        mesh.append("rotate <-90, 0, 0> translate<0, 0.5, 0>}")
        squares = " ".join(mesh)

        grid = ["union {\n"]
        for i in range(self.steps - 1):
            for j in range(self.steps - 1):
                if not j % self.grid_factor:
                    grid.append("cylinder {" f"<{xx[i + 1, j]}, {yy[i + 1, j]}, {ff[i + 1, j]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,{self.line_thickness}"+ "}\n")
                if not i % self.grid_factor:
                    grid.append("cylinder {" f"<{xx[i, j + 1]}, {yy[i, j + 1]}, {ff[i, j + 1]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,{self.line_thickness}"+ "}\n")
        texture = Texture(Pigment("color", get_color(self.line_color)), Finish("ambient", 1))
        grid.append(str(texture))
        grid.append("rotate <-90, 0, 0> translate<0, 0.5, 0>}")
        lines = " ".join(grid)

        return " ".join(("union {", squares, lines, "}"))


def make_povray_image(outfile, draw, width, height):
    """
    Used to create a single PNG image of a 3D povray scene.

    `make_povray_image` calls the user supplied `draw` function to create a povray scene. It then renders
     the image to a PNG file.

    The draw function must have the signature described for `example_draw_function`.

    Args:
        outfile: str - The path and filename for the output PNG file. The '.png' extension is optional,
        it will be added if it isn't present.
        draw: function - A drawing function object, see below.
        width: int - The width of the image that will be created, in pixels.
        height: int - The height of the image that will be created, in pixels.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    scene = draw(width, height, 0, 1)
    scene.render(outfile + '.png', width=width, height=height, antialiasing=0.001)


def make_povray_frame(draw, width, height):
    """
    Used to create a single povray image as a frame. A frame is a NumPy array with shape (pixel_height, pixel_width, 3). Povray images
    are always RGB images.

    `make_povray_frame` calls the user supplied `draw` function to create a povray scene. It then renders
     the image to a NumPy array (a "frame").

    The draw function must have the signature described for `example_draw_function`.

    Args:
        draw: function - A drawing function object, see below.
        width: int - The width of the image that will be created, in pixels.
        height: int - The height of the image that will be created, in pixels.

    Returns:
        A frame.
    """
    scene = draw(width, height, 0, 1)
    rgbdata = scene.render(width=width, height=height, antialiasing=0.001)
    rgbadata = np.full((width, height, 4), 255)
    rgbadata[:, :, :-1] = rgbdata
    return rgbadata


def make_povray_frames(draw, width, height, count):
    """
    Used to sequence of povray images as a frame. A frame is a NumPy array with shape (pixel_height, pixel_width, 3). Povray images
    are always RGB images.

    `make_povray_frames` repetedly calls the user supplied `draw` function to create a series of povray scenes. On each call to `draw`, the
    `frame_no` parameter. It runs from 0 ro `count` -1.

    Each image is rendered to a NumPy array (a "frame").

    The draw function must have the signature described for `example_draw_function`.

    Args:
        draw: function - A drawing function object, see below.
        width: int - The width of the image that will be created, in pixels.
        height: int - The height of the image that will be created, in pixels.
        count: int - The number of frames to create.

    Yield:
        A lazy iterator returning a sequncve of frames. The number of frames is determined by the `count` parameter.
    """
    for i in range(count):
        scene = draw(width, height, i, count)
        rgbdata = scene.render(width=width, height=height, antialiasing=0.001)
        rgbadata = np.full((width, height, 4), 255)
        rgbadata[:, :, :-1] = rgbdata
        yield rgbadata


def example_povray_draw_function(pixel_width, pixel_height, frame_no, frame_count):
    """
    This is an example draw function for use with `make_povray_image` and similar functions. It is a dummy
    function used to document the required parameters.

    Args:
        pixel_width: int - The width of the image in pixels.
        pixel_height: int - The height of the image in pixels
        frame_no: int - the number of the current frame. For single images this will always be 0. For animations this
                        paint function will be called `frame_count` times (once for each frame) with `frame_no` incrementing
                        by 1 each time (ie it counts from 0 to `frame_count` - 1.
        frame_count: int - The total number of frames being created.For single images this will always be 0. For animations
                           this will be set to the total number of frames in the animation.


    Returns:
        The completed povray scene object
    """
    pass

