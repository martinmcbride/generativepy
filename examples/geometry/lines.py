from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Line, line

'''
Create lines using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # The line function is a convenience function that adds a line as a new path.
    # You can fill or stroke it as you wish.
    line(ctx, (1, 1), (2, 3))
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.set_line_width(0.1)
    ctx.stroke()

    # Line objects can only be stroked as they do not contain an area.
    Line(ctx).of_start_end((3, 1), (4, 4)).stroke(Color('fuchsia'), 0.2)

make_image("/tmp/geometry-lines.png", draw, 500, 500)
