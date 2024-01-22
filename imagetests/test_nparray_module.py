import unittest
from generativepy.nparray import make_nparray, make_nparray_frame, overlay_nparrays
from generativepy.drawing import setup, make_image_frame
from generativepy.geometry import Rectangle
from generativepy.color import Color
from generativepy.movie import save_frame
from image_test_helper import run_image_test
import numpy as np

"""
Test each function of the nparray module, with 1, 3 and 4 channel output
"""


def draw4(array, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a transparent blue rectangle on a brown background
    :param array:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    array[:, :] = [128, 64, 0, 255]
    array[50:350, 100:500] = [0, 128, 196, 64]


def draw3(array, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a blue rectangle on a brown background
    :param array:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    array[:, :] = [128, 64, 0]
    array[50:350, 100:500] = [0, 128, 196]


def draw1(array, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a dark grey rectangle on a light greay background
    :param array:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    array[:, :] = [196]
    array[50:350, 100:500] = [64]


def draw3_nofill(array, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a blue rectangle with no background
    :param array:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    array[50:350, 100:500] = [0, 128, 196]


class TestNparrayModule(unittest.TestCase):
    def test_make_nparray_rgba(self):
        def creator(file):
            make_nparray(file, draw4, 600, 400, channels=4)

        self.assertTrue(run_image_test("test_make_nparray_rgba.png", creator))

    def test_make_nparray_rgb(self):
        def creator(file):
            make_nparray(file, draw3, 600, 400, channels=3)

        self.assertTrue(run_image_test("test_make_nparray_rgb.png", creator))

    def test_make_nparray_gray(self):
        def creator(file):
            make_nparray(file, draw1, 600, 400, channels=1)

        self.assertTrue(run_image_test("test_make_nparray_gray.png", creator))

    def test_make_bitmap_frame_rgba(self):
        def creator(file):
            frame = make_nparray_frame(draw4, 600, 400, channels=4)
            save_frame(file, frame)

        self.assertTrue(run_image_test("test_make_nparray_frame_rgba.png", creator))

    def test_make_nparray_frame_rgb(self):
        def creator(file):
            frame = make_nparray_frame(draw3, 600, 400, channels=3)
            save_frame(file, frame)

        self.assertTrue(run_image_test("test_make_nparray_frame_rgb.png", creator))

    def test_make_nparray_frame_gray(self):
        def creator(file):
            frame = make_nparray_frame(draw1, 600, 400, channels=1)
            save_frame(file, frame)

        self.assertTrue(run_image_test("test_make_nparray_frame_gray.png", creator))

    def test_make_nparray_frame_with_output_rgb(self):
        def creator(file):
            out = np.full((400, 600, 3), 128, dtype=np.uint)
            out[25:100, 50:550] = [0, 0, 0]
            frame = make_nparray_frame(draw3_nofill, 600, 400, out=out)
            save_frame(file, frame)

        self.assertTrue(
            run_image_test("test_make_nparray_frame_with_output_rgb.png", creator)
        )

    def test_overlay_nparrays(self):
        def draw1(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))
            Rectangle(ctx).of_corner_size((50, 50), 200, 100).fill(Color(0, 0.5, 0))

        def draw2(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))
            Rectangle(ctx).of_corner_size((300, 200), 100, 150).fill(Color(1, 0, 0.5))

        def creator(file):
            out = np.full((300, 600, 3), 128, dtype=np.uint)
            out[25:100, 50:550] = [0, 0, 0]
            frame1 = make_image_frame(draw1, 500, 400)
            frame2 = make_image_frame(draw2, 500, 400)
            frame = overlay_nparrays(frame1, frame2)
            save_frame(file, frame)

        self.assertTrue(run_image_test("test_overlay_nparrays.png", creator))
