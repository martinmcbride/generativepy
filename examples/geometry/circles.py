from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Circle, circle

'''
Create circles using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # The circle function is a convenience function that adds a circle as a new the path.
    # You can fill or stroke it as you wish.
    circle(ctx, (1, 1), 0.7)
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    # Circle objects can be filled, stroked, filled and stroked.
    Circle(ctx).of_center_radius((2.5, 1), 0.7).fill(Color(0, 0, 1)).stroke(Color(0), 0.05)
    Circle(ctx).of_center_radius((4, 1), 0.7).as_arc(0, 1).stroke(Color(0, 0.5, 0), 0.05)

    Circle(ctx).of_center_radius((1, 2.5), 0.7).as_sector(1, 3).stroke(Color('orange'), 0.05)
    Circle(ctx).of_center_radius((2.5, 2.5), 0.7).as_sector(2, 4.5).fill(Color('cadetblue'))
    Circle(ctx).of_center_radius((4, 2.5), 0.7).as_sector(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

    Circle(ctx).of_center_radius((1, 4), 0.7).as_segment(1, 3).stroke(Color('orange'), 0.05)
    Circle(ctx).of_center_radius((2.5, 4), 0.7).as_segment(2, 4.5).fill(Color('cadetblue'))
    Circle(ctx).of_center_radius((4, 4), 0.7).as_segment(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

make_image("/tmp/geometry-circles.png", draw, 500, 500)
