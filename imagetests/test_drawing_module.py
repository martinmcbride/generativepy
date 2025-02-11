import unittest
from generativepy.drawing import setup, make_image, make_image_frame
from generativepy.movie import save_frame
from generativepy.geometry import Rectangle
from image_test_helper import run_image_test
from generativepy.color import Color

"""
Test each function of the drawing module, with 3 and 4 channel output
"""


def draw_rgb(ctx, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a rectangle on an RGB background
    :param ctx:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    setup(ctx, pixel_width, pixel_height, width=4, background=Color(0.8))
    Rectangle(ctx).of_corner_size((0.5, 1), 3, 1.5).fill(Color(0, .5, 0))


def draw_rgba(ctx, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a rectangle on an RGBA background
    :param ctx:
    :param pixel_width:
    :param pixel_height:
    :param frame_no:
    :param frame_count:
    :return:
    """
    setup(ctx, pixel_width, pixel_height, width=4, background=Color(0.8, 0.5))
    Rectangle(ctx).of_corner_size((0.5, 1), 3, 1.5).fill(Color(0, .5, 0))


class TestDrawingModule(unittest.TestCase):

    def test_drawing_make_image_rgb(self):
        def creator(file):
            make_image(file, draw_rgb, 400, 400, channels=3)

        self.assertTrue(run_image_test('test_drawing_make_image_rgb.png', creator))

    def test_drawing_make_image_rgba(self):
        def creator(file):
            make_image(file, draw_rgba, 400, 400, channels=4)

        self.assertTrue(run_image_test('test_drawing_make_image_rgba.png', creator))

    def test_drawing_make_frame_rgb(self):
        def creator(file):
            frame = make_image_frame(draw_rgb, 400, 400, channels=3)
            save_frame(file, frame)

        self.assertTrue(run_image_test('test_drawing_make_frame_rgb.png', creator))

    def test_drawing_make_frame_rgba(self):
        def creator(file):
            frame = make_image_frame(draw_rgba, 400, 400, channels=4)
            save_frame(file, frame)

        self.assertTrue(run_image_test('test_drawing_make_frame_rgba.png', creator))

