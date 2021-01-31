from generativepy import graph
from generativepy.drawing import make_image, setup, ROUND, BUTT
from generativepy.color import Color
from generativepy.graph import Axes

'''
Create a simple graph with dashed lines
'''

def draw(ctx, width, height, frame_no, frame_count):

    setup(ctx, width, height, width=12, startx=-6, starty=-6, background=Color(1), flip=True)

    # Creates a set of axes.
    # Use the default size of 10 units, but offset the start toplace the origin inthe centre
    axes = Axes(ctx, start=(-5, -5))
    axes.draw()

    # Add various curves
    graph.plot_curve(axes, lambda x: x*x, line_width=2, dash=[5])
    graph.plot_xy_curve(axes, lambda x: 1.5**x, line_color=Color(0, 0, 0.5), line_width=2, dash=[5, 5, 10, 5], cap=ROUND)
    graph.plot_polar_curve(axes, lambda x: 2*x, line_color=Color(0, 0.5, 0), line_width=2, dash=[5], cap=BUTT)


make_image("/tmp/dashedlinegraph.png", draw, 600, 600)
