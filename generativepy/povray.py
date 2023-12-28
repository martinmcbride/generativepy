# Author:  Martin McBride
# Created: 2023-12-02
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.color import Color
from vapory import Camera, LightSource, Background, Scene
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

