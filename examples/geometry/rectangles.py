from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, rectangle

'''
Create rectangles using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # The rectangle function is a convenience function that adds a rectangle as a new the path.
    # You can fill or stroke it as you wish.
    rectangle(ctx, (1, 1), 1, 1.2)
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    # Rectangle objects can be filled, stroked, filled and stroked.
    Rectangle(ctx).of_corner_size((3, 1), 1, 1.2).fill(Color(0, .5, 0))
    Rectangle(ctx).of_corner_size((1, 3), 1.2, 1).stroke(Color(0, .5, 0), 0.1)
    Rectangle(ctx).of_corner_size((3, 3), 1.2, 1).fill(Color(0, 0, 1)).stroke(Color(0), 0.2)

make_image("/tmp/geometry-rectangles.png", draw, 500, 500)
