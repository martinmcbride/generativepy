# Author:  Martin McBride
# Created: 2023-12-02
# Copyright (C) 2022, Martin McBride
# License: MIT
import numpy as np

from generativepy.color import Color
from generativepy.math import Vector as V
from vapory import Camera, LightSource, Background, Scene, Texture, Pigment, Finish, Cylinder, Union, Text
import math

def get_color(color):
    return color[0], color[1], color[2], 1 - color[3]

class Camera3d:

    def __init__(self):
        self.x = 5
        self.y = 0
        self.z = 0
        self.lookat = (0, 0, 0)

    def position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self

    def polar_position(self, distance, angle, elevation):
        self.x = distance * math.cos(angle)
        self.y = distance * math.sin(angle)
        self.z = distance * math.sin(elevation)
        return self

    def standard_plot(self):
        self.x = 5
        self.y = 1
        self.z = -5
        return self

    def get(self):
        return Camera(
            "location",
            [self.x, self.y, self.z],
            "look_at",
            self.lookat
        )


class Lights3d:

    def __init__(self):
        self.lights = ()

    def standard(self, color=Color(1)):
        self.lights = (
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, 5]),
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, -5])
        )
        return self

    def standard_plot(self, color=Color(1)):
        self.lights = (
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, 5]),
            LightSource([0, 0, 0], "color", get_color(color), "translate", [5, 5, -5])
        )
        return self

    def get(self):
        return self.lights

class Scene3d:

    def __init__(self):
        self.camera_item = None
        self.background_color = Color(1)
        self.content = []

    def camera(self, camera):
        self.camera_item = camera
        return self

    def background(self, color):
        self.background_color = Color(1)
        return self

    def add(self, items):
        self.content.extend(items)
        return self

    def get(self):
        return Scene(self.camera_item, [Background("color", get_color(self.background_color))] + self.content)


class Axes3d:

    def __init__(self):
        self.position = [-2]*3
        self.size = [4]*3
        self.start = [-2]*3
        self.end = None
        self.extent = [4]*3
        self.divisions = [0.5]*3
        self.div_positions = None
        self.axis_thickness = 0.02
        self.color = Color("blue").light1
        self.texture = None
        self.division_formatters = [None]*3

    def of_start(self, start):
        self.start = tuple(start)
        return self

    def of_extent(self, extent):
        self.extent = tuple(extent)
        return self

    def with_divisions(self, divisions):
        self.divisions = tuple(divisions)
        return self

    def with_division_formatters(self, formatters):
        self.division_formatters = tuple(formatters)
        return self

    def transform_from_graph(self, point):
        '''
        Convert point in graph coordinates to a corresponding point in Povray coordinates.

        **Parameters**
        
        * `point`, 3-tuple - the point in graph coordinates.

        **Returns**

        Transformed point as a 3-tumple
        '''
        x = ((point[0] - self.start[0]) * self.size[0] / (self.end[0] - self.start[0])) + self.position[0]
        y = ((point[1] - self.start[1]) * self.size[1] / (self.end[1] - self.start[1])) + self.position[1]
        z = ((point[2] - self.start[2]) * self.size[2] / (self.end[2] - self.start[2])) + self.position[2]
        return x, y, z


    def division_linestyle(self, pattern=Color(0), line_width=None):
        self.color = pattern
        if line_width is not None:
            self.axis_thickness = line_width
        return self

    def _make_xy_planes(self):
        items = []

        xstart = [p for p in self.div_positions[0]]
        xend = xstart
        ystart = [self.start[1] for p in self.div_positions[0]]
        yend = [self.end[1] for p in self.div_positions[0]]
        zstart = [self.start[2] for p in self.div_positions[0]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[0]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self.start[0] for p in self.div_positions[1]]
        xend = [self.end[0] for p in self.div_positions[1]]
        ystart = [p for p in self.div_positions[1]]
        yend = ystart
        zstart = [self.start[2] for p in self.div_positions[1]]
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
        ystart = [self.start[1] for p in self.div_positions[0]]
        yend = ystart
        zstart = [self.start[2] for p in self.div_positions[0]]
        zend = [self.end[2] for p in self.div_positions[0]]
        for i, _ in enumerate(self.div_positions[0]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self.start[0] for p in self.div_positions[2]]
        xend = [self.end[0] for p in self.div_positions[2]]
        ystart = [self.start[1] for p in self.div_positions[2]]
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

        xstart = [self.start[0] for p in self.div_positions[2]]
        xend = xstart
        ystart = [self.start[1] for p in self.div_positions[2]]
        yend = [self.end[1] for p in self.div_positions[2]]
        zstart = [p for p in self.div_positions[2]]
        zend = zstart
        for i, _ in enumerate(self.div_positions[2]):
            start = self.transform_from_graph((xstart[i], ystart[i], zstart[i]))
            end = self.transform_from_graph((xend[i], yend[i], zend[i]))
            items.append(Cylinder(start, end, self.axis_thickness, self.texture))

        xstart = [self.start[0] for p in self.div_positions[1]]
        xend = xstart
        ystart = [p for p in self.div_positions[1]]
        yend = ystart
        zstart = [self.start[2] for p in self.div_positions[1]]
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

    def _format_div(self, value, div, formatter):
        """
        Formats a division value into a string.
        If the division spacing is an integer, the string will be an integer (no dp).
        If the division spacing is float, the string will be a float with a suitable number of decimal places

        **Parameters**

        * `value`: value to be formatted
        * `div`: division spacing
        * `formatter`: formatting function, accepts vale and div, returns a formatted value string

        **Returns**

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
             f'"{text}"', # Povray requires "" around text
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
        )

    def _get_divs(self, start, end, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= end:
            divs.append(n)
            n += div
        return divs

    def get(self):
        self.texture = Texture(Pigment("color", get_color(self.color)), Finish("ambient", get_color(Color("blue").light1)))
        self.end = [ex + s for ex, s in zip(self.extent, self.start)]
        self.div_positions = [self._get_divs(self.start[i], self.end[i], self.divisions[i]) for i in range(3)]
        return self._make_axes()


class Plot3dZofXY:

    def __init__(self):
        self.start = [-2, -2]
        self.end = [2, 2]
        self.steps = 40
        self.grid_factor = 5
        self.func = lambda x, y: math.cos(math.sqrt((x**2 + y**2))*2)
        self.color = Color("blue")
        self.line_color = Color("black")
        self.line_thickness = 0.03

    def function(self, f):
        self.func = f

    def get(self):
        x = np.linspace(self.start[0], self.end[0], self.steps)
        y = np.linspace(self.start[1], self.end[1], self.steps)
        xx, yy = np.meshgrid(x, y)
        vf = np.vectorize(self.func)
        ff = vf(xx, yy)

        mesh = ["mesh {\n"]
        for i in range(self.steps - 1):
            for j in range(self.steps - 1):
                mesh.append("triangle {" f"<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
                mesh.append("triangle {" f"<{xx[i+1, j+1]}, {yy[i+1, j+1]}, {ff[i+1, j+1]}>,<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
        texture = Texture(Pigment("color", get_color(self.color)), Finish("phong", 1))
        mesh.append(str(texture))
        mesh.append("rotate <-90, 0, 0> translate<0, -1, 0>}")
        squares = " ".join(mesh)

        grid = ["union {\n"]
        for i in range(self.steps - 1):
            for j in range(self.steps - 1):
                if not j % self.grid_factor:
                    grid.append("cylinder {" f"<{xx[i + 1, j]}, {yy[i + 1, j]}, {ff[i + 1, j]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,{self.line_thickness}"+ "}\n")
                if not i % self.grid_factor:
                    grid.append("cylinder {" f"<{xx[i, j + 1]}, {yy[i, j + 1]}, {ff[i, j + 1]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,{self.line_thickness}"+ "}\n")
        texture = Texture(Pigment("color", get_color(self.line_color)), Finish("phong", 1))
        grid.append(str(texture))
        grid.append("rotate <-90, 0, 0> translate<0, -1, 0>}")
        lines = " ".join(grid)

        return " ".join(("union {", squares, lines, "}"))


def make_povray_image(outfile, draw, width, height):
    """
    Used to create a single PNG image of a 3D povray scene.

    **Parameters**

    * `outfile`: str - The path and filename for the output PNG file. The '.png' extension is optional, it will be added
    if it isn't present.
    * `draw`: function - A drawing function object, see below.
    * `width`: int - The width of the image that will be created, in pixels.
    * `height`: int - The height of the image that will be created, in pixels.

    **Returns**

    None

    **Usage**
    
    `make_image` creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the
    context. It then stores the image as a PNG file.

    The draw function must have the signature described for `example_draw_function`.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    scene = draw(width, height, 0, 1)
    scene.render(outfile + '.png', width=width, height=height, antialiasing=0.001)

def example_povray_draw_function(pixel_width, pixel_height, frame_no, frame_count):
    """
    This is an example draw function for use with `make_povray_image` and similar functions. It is a dummy function used to document the required parameters.

    **Parameters**

    * `pixel_width`: int - The width of the image in pixels.
    * `pixel_height`: int - The height of the image in pixels.
    * `frame_no`: int - the number of the current frame. For single images this will always be 0. For animations this
                        paint function will be called `frame_count` times (once for each frame) with `frame_no` incrementing
                        by 1 each time (ie it counts from 0 to `frame_count` - 1.
    * `frame_count`: int - The total number of frames being created.For single images this will always be 0. For animations
                           this will be set to the total number of frames in the animation.

    **Returns**

    The completed povray scene object
    """
    pass

