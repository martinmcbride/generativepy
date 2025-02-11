from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle
from generativepy.drawing import ROUND, BEVEL, BUTT

'''
Create rectangles using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))


    # Rectangle objects can be filled, stroked, filled and stroked.
    Rectangle(ctx).of_corner_size((0.5, 1), 1, 1.2).stroke(Color(0, .5, 0), 0.1, dash=[0.25])
    Rectangle(ctx).of_corner_size((2, 1), 1, 1.2).stroke(Color(0, .5, 0), 0.1, dash=[0.25], cap=BUTT)
    Rectangle(ctx).of_corner_size((3.5, 1), 1.2, 1).stroke(Color(0, .5, 0), 0.1, dash=[0.25], cap=ROUND)
    Rectangle(ctx).of_corner_size((0.5, 3), 1, 1.2).stroke(Color(0, .5, 0), 0.1, join=ROUND)
    Rectangle(ctx).of_corner_size((2, 3), 1, 1.2).stroke(Color(0, .5, 0), 0.1, join=BEVEL)
    Rectangle(ctx).of_corner_size((3.5, 3), 1.2, 1).stroke(Color(0, .5, 0), 0.1, miter_limit=1)

make_image("/tmp/geometry-line-styles.png", draw, 500, 500)
