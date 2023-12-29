# Author:  Martin McBride
# Created: 2023-12-02
# Copyright (C) 2022, Martin McBride
# License: MIT
import numpy as np

from generativepy.color import Color
from vapory import Camera, LightSource, Background, Scene, Texture, Pigment, Finish, Cylinder, Union
import math

def get_color(color):
    return color[0], color[1], color[2]

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
        self.start = [-2, -2, -2]
        self.end = [2, 2, 2]
        self.axis_thickness = 0.03
        self.axis_colors = [Color("red"), Color("green"), Color("blue")]

    def _make_axis(self, axis, color=[1, 0, 0]):
        texture = Texture(Pigment("color", color), Finish("phong", 1))
        startxyz = [0] * 3
        endxyz= [0] * 3
        startxyz[axis] = self.start[axis]
        endxyz[axis] = self.end[axis]
        return Cylinder(startxyz, endxyz, self.axis_thickness, texture)

    def _make_axes(self):
        axes = [self._make_axis(i, get_color(self.axis_colors[i])) for i in range(3)]
        return Union(
            axes[0],
            axes[1],
            axes[2],
            "rotate",
            [-90, 0, 0],
            "translate",
            [0, -1, 0],
        )

    def get(self):
        return self._make_axes()


class Plot3dZofXY:

    def __init__(self):
        self.start = [-2, -2]
        self.end = [2, 2]
        self.steps = 20
        self.func = lambda x, y: 1+0.5*math.cos(2*x + 2*y)

    def function(self, f):
        self.func = f

    def get(self):
        # t1 = "triangle {<-1, -1, -1>, <-1, 1, 0>, <1, -1, 0>}"
        # t2 = "triangle {<1, 1, 0.5>, <-1, 1, 0>, <1, -1, 0>}"
        # s = r"mesh {" + t1 + t2 + " texture {pigment { color rgb<0, 0, 1> } finish { phong 1 } } }"
        # return s
        x = np.linspace(self.start[0], self.end[0], self.steps)
        y = np.linspace(self.start[1], self.end[1], self.steps)
        xx, yy = np.meshgrid(x, y)
        vf = np.vectorize(self.func)
        ff = vf(xx, yy)
        squares = ["mesh {\n"]
        for i in range(self.steps - 1):
            for j in range(self.steps - 1):
                squares.append("triangle {" f"<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j]}, {yy[i, j]}, {ff[i, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
                squares.append("triangle {" f"<{xx[i+1, j+1]}, {yy[i+1, j+1]}, {ff[i+1, j+1]}>,<{xx[i+1, j]}, {yy[i+1, j]}, {ff[i+1, j]}>,<{xx[i, j+1]}, {yy[i, j+1]}, {ff[i, j+1]}>"+ "}\n")
        squares.append("texture {pigment { color rgb<0.9, 0, 0> } finish { ambient 0.2 diffuse 0.7 } } rotate <-90, 0, 0> translate<0, -1, 0>}")
        return " ".join(squares)


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
    print(scene)
    scene.render(outfile + '.png', width=width, height=height)

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

