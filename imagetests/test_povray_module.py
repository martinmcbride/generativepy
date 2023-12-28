import math
import unittest
from vapory import Texture, Pigment, Finish, Box

from generativepy.povray import (
    Camera3D,
    scene,
    standard_lights,
    make_povray_image,
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
    camera = Camera3D().polar_position(distance, theta, elevation).get()
    texture = Texture(Pigment("color", [0, 0, 1]), Finish("phong", 1))
    box = Box([-1, -1, -1], [1, 1, 1], texture)

    return scene(
        camera,
        standard_lights(),
        [box],
    )


class TestBitmapModule(unittest.TestCase):
    def test_povray_scene(self):
        def creator(file):
            make_povray_image(file, draw_block, 500, 500)

        self.assertTrue(run_image_test("test_povray_scene.png", creator))
