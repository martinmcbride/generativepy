from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Rectangle, Line, Circle
import math

'''
Create polygons using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=300, background=Color(1))

    # Fill then stroke a rectangle
    ctx.save()
    ctx.translate(0, 0)
    Rectangle(ctx).of_corner_size((20, 20), 60, 60).fill(Color('red')).stroke(Color('blue'), 10)
    ctx.restore()

    # Stroke then fill a rectangle
    ctx.save()
    ctx.translate(100, 0)
    Rectangle(ctx).of_corner_size((20, 20), 60, 60).stroke(Color('blue'), 10).fill(Color('red'))
    ctx.restore()

    # Path with two rectangles
    ctx.save()
    ctx.translate(200, 0)
    Rectangle(ctx).of_corner_size((20, 20), 60, 60).add()
    Rectangle(ctx).of_corner_size((30, 30), 60, 60).as_sub_path().fill(Color('red')).stroke(Color('blue'), 5)
    ctx.restore()

    # Path from several lines
    ctx.save()
    ctx.translate(0, 100)
    Line(ctx).of_start_end((20, 20), (60, 30)).add()
    Line(ctx).of_end((60, 60)).extend_path().add()
    Line(ctx).of_end((30, 50)).extend_path().fill(Color('red')).stroke(Color('blue'), 5)
    ctx.restore()

    # Path from several lines, closed
    ctx.save()
    ctx.translate(100, 100)
    Line(ctx).of_start_end((20, 20), (60, 30)).add()
    Line(ctx).of_end((60, 60)).extend_path().add()
    Line(ctx).of_end((30, 50)).extend_path(close=True).fill(Color('red')).stroke(Color('blue'), 5)
    ctx.restore()

    # roundrect open
    ctx.save()
    ctx.translate(0, 200)
    Circle(ctx).of_center_radius((20, 20), 10).as_arc(math.pi, math.pi*3/2).add()
    Circle(ctx).of_center_radius((60, 20), 10).as_arc(math.pi*3/2, 0).extend_path().add()
    Circle(ctx).of_center_radius((60, 60), 10).as_arc(0, math.pi/2).extend_path().add()
    Circle(ctx).of_center_radius((20, 60), 10).as_arc(math.pi/2, math.pi).extend_path().fill(Color('red')).stroke(Color('blue'), 5)
    ctx.restore()

    # roundrect closed
    ctx.save()
    ctx.translate(100, 200)
    Circle(ctx).of_center_radius((20, 20), 10).as_arc(math.pi, math.pi*3/2).add()
    Circle(ctx).of_center_radius((60, 20), 10).as_arc(math.pi*3/2, 0).extend_path().add()
    Circle(ctx).of_center_radius((60, 60), 10).as_arc(0, math.pi/2).extend_path().add()
    Circle(ctx).of_center_radius((20, 60), 10).as_arc(math.pi/2, math.pi).extend_path(close=True).fill(Color('red')).stroke(Color('blue'), 5)
    ctx.restore()



make_image("/tmp/geometry-complex-paths.png", draw, 600, 600)
