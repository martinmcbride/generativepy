from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Bezier, Polygon

'''
Create bezier curve using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # Bezier objects can only be stroked as they do not contain an area.
    Bezier(ctx).of_abcd((1, 1.5), (3, 0.5), (2, 2.5), (4, 1.5)).stroke(Color('darkgreen'), 0.1)

    # Create a polygon with a bezier side
    Polygon(ctx).of_points([(1, 4.5), (1, 2.5), (2, 3, 3, 4, 4, 2.5), (4, 4.5)]).fill(Color('red')).stroke(Color('blue'), 0.05)

make_image("/tmp/geometry-bezier.png", draw, 500, 500)
