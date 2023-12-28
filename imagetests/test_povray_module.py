import math
import unittest
from vapory import Texture, Pigment, Finish, Box, Sphere

from generativepy.povray import (
    Camera3d,
    Scene3d,
    Lights3d,
    make_povray_image,
    get_color,
)
from image_test_helper import run_image_test
from generativepy.color import Color

"""
Test each function of the povray module
"""


def draw_block(pixel_width, pixel_height, frame_no, frame_count):
    theta = math.radians(20)
    elevation = math.radians(-40)
    distance = 5
    camera = Camera3d().polar_position(distance, theta, elevation).get()
    lights = Lights3d().standard(Color(1)).get()
    texture = Texture(Pigment("color", get_color(Color("blue"))), Finish("phong", 1))
    # box = Box([-1, -1, -1], [1, 1, 1], texture)
    box = Sphere([0, 0, 0], 1, texture)

    return Scene3d().camera(camera).add(lights).add([box]).get()


class TestPovrayModule(unittest.TestCase):
    def test_povray_scene(self):
        def creator(file):
            make_povray_image(file, draw_block, 500, 500)

        self.assertTrue(run_image_test("test_povray_scene.png", creator))
