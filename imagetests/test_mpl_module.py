import math
import unittest

from generativepy.matplotlib import make_mpl_image, Plot3dZofXY
from imagetests.image_test_helper import run_image_test


class TestMPLImages(unittest.TestCase):
    def test_3d_graph_simple(self):
        def draw(plt, width, height, frame_no, frame_count):
            (Plot3dZofXY(plt, width, height).of(lambda x, y: math.cos(math.sqrt(x*x + y*y))).of_start((-5, -5, -2.5))
             .of_extent((10, 10, 5)).with_divisions((2, 2, 1)).with_view_rot(15, -60).render())

        def creator(file):
            make_mpl_image(file, draw, 500, 400)

        self.assertTrue(run_image_test("test_mpl_simple.png", creator))

