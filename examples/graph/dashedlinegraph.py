from generativepy.drawing import make_image, setup, ROUND, BUTT
from generativepy.color import Color
from generativepy.graph import Axes, Plot

'''
Create a simple graph with dashed lines
'''

def draw(ctx, width, height, frame_no, frame_count):

    setup(ctx, width, height, background=Color(1))

    # Creates a set of axes.
    # Use the default size of 10 units, but offset the start toplace the origin inthe centre
    axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
    axes.draw()

    axes.clip()
    Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'), line_width=3, dash=[5])
    Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'), line_width=5, dash=[10, 10, 20, 10],
                                                         cap=ROUND)
    Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'), line_width=4, dash=[5], cap=BUTT)
    axes.unclip()


make_image("/tmp/dashedlinegraph.png", draw, 600, 600)
