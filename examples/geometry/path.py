from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Polygon, Text, Path

'''
Demonstrate paths in  the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    # Get a polygon path object
    path1 = Polygon(ctx).of_points([(0, 0), (1, 1), (0.5, 2), (0.5, 1)]).path()

    # Get a text path object
    path2 = Text(ctx).of("Path text", (0, 0)).font("Times").size(0.2).align_left().align_top().path()

    # Apply the polygon in various places
    ctx.save()
    ctx.translate(0.5, 1)
    Path(ctx).of(path1).stroke(Color('darkgreen'), 0.1)
    ctx.restore()

    ctx.save()
    ctx.translate(1, 2.5)
    Path(ctx).of(path1).fill(Color('blue'))
    ctx.restore()

    ctx.save()
    ctx.translate(2.5, 0.5)
    ctx.scale(2, 2)
    Path(ctx).of(path1).fill(Color('orange')).stroke(Color('black'), 0.05)
    ctx.restore()

    # Apply the text in various places
    ctx.save()
    ctx.translate(0, 0)
    Path(ctx).of(path2).fill(Color('black'))
    ctx.restore()

    ctx.save()
    ctx.translate(2, 3)
    Path(ctx).of(path2).stroke(Color('red'), 0.01)
    ctx.restore()

    ctx.save()
    ctx.translate(2, 4)
    ctx.scale(2, 2)
    Path(ctx).of(path2).fill(Color('yellow')).stroke(Color('black'), 0.01)
    ctx.restore()


make_image("/tmp/geometry-path.png", draw, 500, 500)
