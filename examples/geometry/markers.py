from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import line, polygon, angle_marker, tick, paratick, arrowhead

'''
Create markers using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, background=Color(0.8))

    ctx.set_source_rgba(*Color(0, 0, 0.5))
    ctx.set_line_width(3)

    ## Draw lines with ticks, paraticks and arrowheads
    a = (50, 50)
    b = (50, 150)
    line(ctx, a, b)
    ctx.stroke()
    tick(ctx, a, b, length=12, gap=6)
    ctx.stroke()
    arrowhead(ctx, a, b, length=24)
    ctx.stroke()

    a = (100, 50)
    b = (150, 150)
    line(ctx, a, b)
    ctx.stroke()
    tick(ctx, a, b, 2, length=12, gap=6)
    ctx.stroke()

    a = (250, 50)
    b = (200, 150)
    line(ctx, a, b)
    ctx.stroke()
    tick(ctx, a, b, 3, length=12, gap=6)
    ctx.stroke()

    a = (350, 50)
    b = (350, 150)
    line(ctx, a, b)
    ctx.stroke()
    paratick(ctx, a, b, length=12, gap=6)
    ctx.stroke()

    a = (400, 50)
    b = (450, 150)
    line(ctx, a, b)
    ctx.stroke()
    paratick(ctx, a, b, 2, length=12, gap=6)
    ctx.stroke()

    a = (550, 150)
    b = (500, 50)
    line(ctx, a, b)
    ctx.stroke()
    paratick(ctx, a, b, 3, length=12, gap=6)
    ctx.stroke()

    ## Draw lines with angles
    a = (50, 250)
    b = (50, 450)
    c = (150, 450)
    polygon(ctx, (a, b, c), closed=False)
    ctx.stroke()
    angle_marker(ctx, a, b, c, radius=24, gap=6, right_angle=True)
    ctx.stroke()

    a = (250, 250)
    b = (200, 450)
    c = (300, 450)
    polygon(ctx, (a, b, c), closed=False)
    ctx.stroke()
    angle_marker(ctx, a, b, c, 3, radius=24, gap=6)
    ctx.stroke()

    a = (300, 250)
    b = (400, 300)
    c = (500, 300)
    polygon(ctx, (a, b, c), closed=False)
    ctx.stroke()
    angle_marker(ctx, c, b, a, radius=24, gap=6)
    ctx.stroke()

    a = (300, 350)
    b = (400, 400)
    c = (500, 400)
    polygon(ctx, (a, b, c), closed=False)
    ctx.stroke()
    angle_marker(ctx, a, b, c, 2, radius=24, gap=6)
    ctx.stroke()

make_image("/tmp/geometry-markers.png", draw, 600, 500)
