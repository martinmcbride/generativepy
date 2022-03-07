from generativepy.drawing import make_image, setup, ROUND
from generativepy.color import Color
from generativepy.geometry import Turtle
import math

'''
Demonstrate paths in  the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, background=Color(0.8))

    turtle = Turtle(ctx)
    turtle.move_to(100, 100).forward(50).left(math.pi / 2).forward(50).left(math.pi / 4).forward(50)

    turtle = Turtle(ctx)
    turtle.move_to(200, 300).set_style(Color('green'), line_width=5, dash=[10]) \
        .push().forward(100).pop() \
        .push().left(3 * math.pi / 4).forward(100).pop() \
        .right(3 * math.pi / 4).forward(100)

    turtle = Turtle(ctx)
    turtle.move_to(350, 100).right(math.pi / 2).set_style(Color('red'), line_width=5, dash=[10], cap=ROUND).forward(100)
    turtle.set_style(Color('blue'), line_width=2, dash=[]).forward(100)
    turtle.set_style(Color('black'), line_width=4, dash=[15]).forward(100)

make_image("turtle.png", draw, 500, 500)
