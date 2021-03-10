import unittest
from generativepy.drawing import setup
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.geometry import Image

class TestDrawingImageImages(unittest.TestCase):

    def test_geometry_image(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))
            Image(ctx).of_file_position('cat.png', (50, 50)).paint()
            Image(ctx).of_file_position('cat.png', (300, 50)).scale(0.5).paint()
            Image(ctx).of_file_position('cat.png', (50, 300)).scale(1.5).paint()
            Image(ctx).of_file_position('formula.png', (50, 600)).paint()
            Image(ctx).of_file_position('formula.png', (350, 200)).scale(0.5).paint()

        self.assertTrue(run_image_test('test_geometry_image.png', draw, 800, 800))
