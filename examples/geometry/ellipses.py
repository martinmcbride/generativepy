from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Ellipse, ellipse

'''
Create ellipses using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # The ellipse function is a convenience function that adds a ellipse as a new the path.
    # You can fill or stroke it as you wish.
    ellipse(ctx, (1, 1), 0.7, 1.1)
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    # Ellipse objects can be filled, stroked, filled and stroked.
    Ellipse(ctx).of_center_radius((2.5, 1), 0.7, 0.3).fill(Color(0, 0, 1)).stroke(Color(0), 0.05)
    Ellipse(ctx).of_center_radius((4, 1), 0.7, 0.3).as_arc(0, 1).stroke(Color(0, 0.5, 0), 0.05)

    Ellipse(ctx).of_center_radius((1, 2.5), 0.7, 0.3).as_sector(1, 3).stroke(Color('orange'), 0.05)
    Ellipse(ctx).of_center_radius((2.5, 2.5), 0.7, 0.3).as_sector(2, 4.5).fill(Color('cadetblue'))
    Ellipse(ctx).of_center_radius((4, 2.5), 0.7, 0.3).as_sector(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

    Ellipse(ctx).of_center_radius((1, 4), 0.7, 0.3).as_segment(1, 3).stroke(Color('orange'), 0.05)
    Ellipse(ctx).of_center_radius((2.5, 4), 0.7, 0.3).as_segment(2, 4.5).fill(Color('cadetblue'))
    Ellipse(ctx).of_center_radius((4, 4), 0.7, 0.3).as_segment(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

make_image("/tmp/geometry-ellipses.png", draw, 500, 500)
