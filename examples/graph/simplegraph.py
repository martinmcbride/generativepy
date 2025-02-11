from generativepy import graph
from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.graph import Axes, Plot

'''
Create a simple graph
'''

def draw(ctx, width, height, frame_no, frame_count):

    setup(ctx, width, height, background=Color(1))

    # Creates a set of axes.
    # Use the default size of 10 units, but offset the start toplace the origin inthe centre
    axes = Axes(ctx, (50, 50), 500, 500).of_start((-5, -5))
    axes.draw()

    # Add various curves
    axes.clip()
    Plot(axes).of_function(lambda x: x * x).stroke(pattern=Color('red'))
    Plot(axes).of_xy_function(lambda x: 1.5 ** x).stroke(pattern=Color('green'))
    Plot(axes).of_polar_function(lambda x: 2 * x).stroke(pattern=Color('blue'))
    axes.unclip()

make_image("/tmp/simplegraph.png", draw, 500, 500)
