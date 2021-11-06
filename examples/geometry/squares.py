from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Square, square

'''
Create squares using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # The square function is a convenience function that adds a square as a new the path.
    # You can fill or stroke it as you wish.
    square(ctx, (1, 1), 1)
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    # Square objects can be filled, stroked, filled and stroked.
    Square(ctx).of_corner_size((3, 1), 1).fill(Color(0, .5, 0))
    Square(ctx).of_corner_size((1, 3), 1).stroke(Color(0, .5, 0), 0.1)
    Square(ctx).of_corner_size((3, 3), 1).fill(Color(0, 0, 1)).stroke(Color(0), 0.2)

make_image("/tmp/geometry-squares.png", draw, 500, 500)
