import math
import unittest
from vapory import Texture, Pigment, Finish, Box, Sphere

from generativepy.povray import (
    Camera3d,
    Scene3d,
    Lights3d,
    make_povray_image,
    get_color,
    Axes3d,
    Plot3dZofXY,
)
from image_test_helper import run_image_test
from generativepy.color import Color

"""
Test each function of the povray module
"""


class TestPovrayModule(unittest.TestCase):
    def test_povray_scene(self):
        def draw(pixel_width, pixel_height, frame_no, frame_count):
            theta = math.radians(20)
            elevation = math.radians(-40)
            distance = 5
            camera = Camera3d().polar_position(distance, theta, elevation).get()
            lights = Lights3d().standard(Color(1)).get()
            texture = Texture(
                Pigment("color", get_color(Color("blue"))), Finish("phong", 1)
            )
            box = Sphere([0, 0, 0], 1, texture)

            return Scene3d().camera(camera).add(lights).add([box]).get()

        def creator(file):
            make_povray_image(file, draw, 500, 500)

        self.assertTrue(run_image_test("test_povray_scene.png", creator))

    def test_povray_axes(self):
        def draw(pixel_width, pixel_height, frame_no, frame_count):
            camera = Camera3d().standard_plot().get()
            lights = Lights3d().standard_plot().get()
            axes = Axes3d().get()
            return Scene3d().camera(camera).add(lights).add([axes]).get()

        def creator(file):
            make_povray_image(file, draw, 500, 500)

        self.assertTrue(run_image_test("test_povray_axes.png", creator))

    def test_povray_non_default_axes(self):
        def draw(pixel_width, pixel_height, frame_no, frame_count):
            camera = Camera3d().standard_plot().get()
            lights = Lights3d().standard_plot().get()
            axes = (
                Axes3d()
                .division_linestyle(Color("magenta", 0.01))
                .of_start((1, -2, 1))
                .of_extent((10, 6, 2))
                .with_divisions((2, 1, 0.2))
                .get()
            )
            return Scene3d().camera(camera).add(lights).add([axes]).get()

        def creator(file):
            make_povray_image(file, draw, 500, 500)

        self.assertTrue(run_image_test("test_povray_non_default_axes.png", creator))

    def test_povray_Plot3dZofXY(self):
        def draw(pixel_width, pixel_height, frame_no, frame_count):
            camera = Camera3d().standard_plot().get()
            lights = Lights3d().standard_plot().get()
            axes = Axes3d()
            plot = (
                Plot3dZofXY(axes)
                .function(lambda x, y: -x)
                .get()
            )
            return Scene3d().camera(camera).add(lights).add([axes.get(), plot]).get()

        def creator(file):
            make_povray_image(file, draw, 500, 500)

        self.assertTrue(
            run_image_test("test_povray_test_povray_Plot3dZofXY.png", creator)
        )

    def test_povray_Plot3dZofXY_non_default(self):
        def draw(pixel_width, pixel_height, frame_no, frame_count):
            camera = Camera3d().standard_plot().get()
            lights = Lights3d().standard_plot().get()
            axes = Axes3d().of_start((-2, -4, -1)).of_extent((4, 8, 3)).with_divisions((0.5, 1, 0.5))
            plot = (
                Plot3dZofXY(axes)
                .function(lambda x, y: math.cos(x)*math.cos(y))
                .grid_linestyle(Color(0), 0.01)
                .fill(Color("dodgerblue"))
                .get()
            )
            return Scene3d().camera(camera).add(lights).add([axes.get(), plot]).get()

        def creator(file):
            make_povray_image(file, draw, 500, 500)

        self.assertTrue(
            run_image_test("test_povray_Plot3dZofXY_non_default.png", creator)
        )
