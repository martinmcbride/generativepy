import unittest
from image_test_helper import run_image3d_test

class TestDrawing3dImages(unittest.TestCase):

    def test_simple_drawing3d(self):
        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            pass

        self.assertTrue(run_image3d_test('test_simple_drawing3d.png', draw, 700, 600))
