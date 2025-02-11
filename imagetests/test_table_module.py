import unittest

from generativepy.geometry import Text

from generativepy.drawing import setup, make_image, CENTER, MIDDLE
from generativepy.table import Table
from image_test_helper import run_image_test
from generativepy.color import Color

"""
Test the table module.
"""


class TestTableImages(unittest.TestCase):

    def test_table(self):
        """
        Draw 2 tables, one with default styling and one with custom colours and line width.
        Add some text to some of the cells
        :return:
        """
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            # Creates a table with default settings
            table = Table(ctx, (50, 50)).of_rows_cols([50]*4, [100]*3)
            table.draw()
            Text(ctx).of("A", table.get(0, 0)).size(20).align(CENTER, MIDDLE).fill(Color(0))
            Text(ctx).of("B", table.get(2, 1)).size(20).align(CENTER, MIDDLE).fill(Color(0))
            Text(ctx).of("C", table.get(3, 2)).size(20).align(CENTER, MIDDLE).fill(Color(0))

            # Creates a table with a different style
            table = Table(ctx, (400, 100)).of_rows_cols([80]*3, [30]*4).background(Color("palegreen")).linestyle(Color("dodgerblue"), 4)
            table.draw()
            Text(ctx).of("a", table.get(1, 2)).size(20).align(CENTER, MIDDLE).fill(Color(0))
            Text(ctx).of("b", table.get(2, 3)).size(20).align(CENTER, MIDDLE).fill(Color(0))
            Text(ctx).of("c", table.get(0, 1)).size(20).align(CENTER, MIDDLE).fill(Color(0))


        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_table.png', creator))

