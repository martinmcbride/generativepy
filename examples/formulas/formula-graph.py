from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.graph import Axes, Plot
from generativepy.geometry import Image
from generativepy.formulas import rasterise_formula

import math


'''
Create a simple graph
'''

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, background=Color(1))

    # Creates a set of axes.
    # Use the default size of 10 units, but offset the start to place the origin in the centre
    axes = Axes(ctx, (50, 100), 400, 400).of_start((-5, -5))
    axes.draw()

    # Add a curve
    axes.clip()
    Plot(axes).of_function(lambda x: 4*math.sin(x)).stroke(pattern=Color('darkred'))
    axes.unclip()

    # Add formula
    image, size = rasterise_formula("formula-graph-1", r"y = 4\sin{x}", Color("darkblue"), dpi=400)
    Image(ctx).of_file_position(image, (100, 30)).paint()

make_image("/tmp/formula-graph.png", draw, 500, 550)
