import unittest
from generativepy.drawing import setup
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.geometry import Text

class TestTextOffsetImages(unittest.TestCase):

    def test_text_offset(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))

            Text(ctx).of('A', (200, 200)).size(40).fill(Color(0))
            Text(ctx).of('B', (200, 200)).offset(100, 20).size(40).fill(Color(0))
            Text(ctx).of('C', (200, 200)).offset_angle(1, 150).size(40).fill(Color(0))
            Text(ctx).of('D', (200, 200)).offset_towards((100, 150), 50).size(40).fill(Color(0))


        self.assertTrue(run_image_test('test_text_offset.png', draw, 400, 400))