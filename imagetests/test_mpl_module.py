import math
import unittest

from generativepy.matplotlib import make_mpl_image, Plot3dZofXY
from imagetests.image_test_helper import run_image_test


class TestMPLImages(unittest.TestCase):
    def test_3d_graph_simple(self):
        def draw(plt, width, height, frame_no, frame_count):
            Plot3dZofXY(plt).of(lambda x, y: math.sqrt(x*x + y*y)).render()

        def creator(file):
            make_mpl_image(file, draw, 600, 600)

        self.assertTrue(run_image_test("test_mpl_simple.png", creator))

