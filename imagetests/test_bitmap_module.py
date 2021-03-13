import unittest
from generativepy.bitmap import make_bitmap, make_bitmap_frame
from generativepy.movie import save_frame
from image_test_helper import run_image_test
from generativepy.color import Color
from PIL import ImageDraw

"""
Test each function of the bitmap module, with 3 and 4 channel output
"""


def draw(image, pixel_width, pixel_height, frame_no, frame_count):
    """
    Draw a rectangle on the bitmap
    :param image: 
    :param pixel_width: 
    :param pixel_height: 
    :param frame_no: 
    :param frame_count: 
    :return: 
    """
    imagedraw = ImageDraw.Draw(image)
    imagedraw.rectangle((60, 10, 300, 150), fill=Color("tomato").as_rgbstr())


class TestBitmapModule(unittest.TestCase):

    def test_make_bitmap_gray(self):
        def creator(file):
            make_bitmap(file, draw, 400, 400, channels=1)

        self.assertTrue(run_image_test('test_make_bitmap_gray.png', creator))

    def test_make_bitmap_rgb(self):
        def creator(file):
            make_bitmap(file, draw, 400, 400, channels=3)

        self.assertTrue(run_image_test('test_make_bitmap_rgb.png', creator))

    def test_make_bitmap_rgba(self):
        def creator(file):
            make_bitmap(file, draw, 400, 400, channels=4)

        self.assertTrue(run_image_test('test_make_bitmap_rgba.png', creator))

    def test_make_bitmap_frame_gray(self):
        def creator(file):
            frame = make_bitmap_frame(draw, 400, 400, channels=1)
            save_frame(file, frame)

        self.assertTrue(run_image_test('test_make_bitmap_frame_gray.png', creator))

    def test_make_bitmap_frame_rgb(self):
        def creator(file):
            frame = make_bitmap_frame(draw, 400, 400, channels=3)
            save_frame(file, frame)

        self.assertTrue(run_image_test('test_make_bitmap_frame_rgb.png', creator))

    def test_make_bitmap_frame_rgba(self):
        def creator(file):
            frame = make_bitmap_frame(draw, 400, 400, channels=4)
            save_frame(file, frame)

        self.assertTrue(run_image_test('test_make_bitmap_frame_rgba.png', creator))

