from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Circle, Square, Text

'''
Create bezier curve using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # Create a circular clip region and draw some squares in it
    ctx.save()
    Circle(ctx).of_center_radius((1.9, 1.9), 1).clip()
    Square(ctx).of_corner_size((1, 1), .8).fill(Color('red'))
    Square(ctx).of_corner_size((1, 2), .8).fill(Color('green'))
    Square(ctx).of_corner_size((2, 1), .8).fill(Color('blue'))
    Square(ctx).of_corner_size((2, 2), .8).fill(Color('black'))
    ctx.restore()

    ctx.save()
    Text(ctx).of("ABC", (1.5, 3.5)).font("Times").size(1.5).align_left().align_top().clip()
    circles = [(2, 3.8, 'orange'), (2, 4.5, 'cyan'), (3, 3.8, 'green'),
               (3, 4.5, 'purple'), (4, 3.8, 'yellow'), (4, 4.5, 'blue')]
    for x, y, color in circles:
        Circle(ctx).of_center_radius((x, y), 0.7).fill(Color(color))
    ctx.restore()


make_image("/tmp/geometry-clip.png", draw, 500, 500)
