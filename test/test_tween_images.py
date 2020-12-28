import unittest
from generativepy.drawing import setup
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.tween import Tween
import generativepy.tween
from generativepy.geometry import Polygon, Square

class TestTweenImages(unittest.TestCase):

    def test_easing_graphs(self):
        '''
        Plot the easing functions as graphs on an image
        '''

        def plot_easing_function(ctx, x, y, fn):
            tw = Tween(0).ease(-100, 100, fn)
            poly = [(i, tw[i]) for i in range(100)]
            ctx.save()
            ctx.translate(x, y)
            Square(ctx).of_corner_size((0, -100), 100).stroke(Color(0.5), 2)
            Polygon(ctx).of_points(poly).open().stroke(Color('red'), 2)
            ctx.restore()

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))
            plot_easing_function(ctx, 10, 120, generativepy.tween.ease_linear())
            plot_easing_function(ctx, 10, 230, generativepy.tween.ease_in_harm())
            plot_easing_function(ctx, 120, 230, generativepy.tween.ease_out_harm())
            plot_easing_function(ctx, 230, 230, generativepy.tween.ease_in_out_harm())
            plot_easing_function(ctx, 340, 230, generativepy.tween.ease_in_back())
            plot_easing_function(ctx, 450, 230, generativepy.tween.ease_out_back())
            plot_easing_function(ctx, 560, 230, generativepy.tween.ease_in_out_back())
            plot_easing_function(ctx, 10, 450, generativepy.tween.ease_in_elastic())
            plot_easing_function(ctx, 120, 450, generativepy.tween.ease_out_elastic())
            plot_easing_function(ctx, 230, 450, generativepy.tween.ease_in_out_elastic())
            plot_easing_function(ctx, 340, 450, generativepy.tween.ease_in_bounce())
            plot_easing_function(ctx, 450, 450, generativepy.tween.ease_out_bounce())
            plot_easing_function(ctx, 560, 450, generativepy.tween.ease_in_out_bounce())

        self.assertTrue(run_image_test('test_easing_graphs.png', draw, 700, 600))