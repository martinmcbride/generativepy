from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import line, polygon, angle_marker, tick, paratick, arrowhead

'''
Illustrations of markers for project documentations
'''

def angle_illustration():
    def draw(ctx, width, height, frame_no, frame_count):
        setup(ctx, width, height, background=Color(1))

        ctx.set_source_rgba(*Color('black'))
        ctx.set_line_width(3)

        ## Draw lines with angles
        a = (100, 50)
        b = (50, 250)
        c = (150, 250)
        polygon(ctx, (a, b, c), closed=False)
        ctx.stroke()
        angle_marker(ctx, a, b, c, radius=24)
        ctx.stroke()

        a = (250, 50)
        b = (200, 250)
        c = (300, 250)
        polygon(ctx, (a, b, c), closed=False)
        ctx.stroke()
        angle_marker(ctx, a, b, c, 2, radius=24, gap=6)
        ctx.stroke()

        a = (400, 50)
        b = (350, 250)
        c = (450, 250)
        polygon(ctx, (a, b, c), closed=False)
        ctx.stroke()
        angle_marker(ctx, a, b, c, 3, radius=24, gap=6)
        ctx.stroke()

        a = (500, 50)
        b = (500, 250)
        c = (600, 250)
        polygon(ctx, (a, b, c), closed=False)
        ctx.stroke()
        angle_marker(ctx, a, b, c, radius=24, gap=6, right_angle=True)
        ctx.stroke()

    make_image("/tmp/angle-illustration.png", draw, 650, 300)

def tick_illustration():
    def draw(ctx, width, height, frame_no, frame_count):
        setup(ctx, width, height, background=Color(1))

        ctx.set_source_rgba(*Color('black'))
        ctx.set_line_width(3)

        ## Draw lines with ticks
        a = (50, 50)
        b = (150, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        tick(ctx, a, b, length=12, gap=6)
        ctx.stroke()

        a = (200, 50)
        b = (300, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        tick(ctx, a, b, 2, length=12, gap=6)
        ctx.stroke()

        a = (350, 50)
        b = (450, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        tick(ctx, a, b, 3, length=12, gap=6)
        ctx.stroke()

    make_image("/tmp/tick-illustration.png", draw, 500, 300)

def paratick_illustration():
    def draw(ctx, width, height, frame_no, frame_count):
        setup(ctx, width, height, background=Color(1))

        ctx.set_source_rgba(*Color('black'))
        ctx.set_line_width(3)

        ## Draw lines with paraticks
        a = (50, 50)
        b = (150, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        paratick(ctx, a, b, length=12, gap=6)
        ctx.stroke()

        a = (200, 50)
        b = (300, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        paratick(ctx, a, b, 2, length=12, gap=6)
        ctx.stroke()

        a = (350, 50)
        b = (450, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        paratick(ctx, a, b, 3, length=12, gap=6)
        ctx.stroke()

    make_image("/tmp/paratick-illustration.png", draw, 500, 300)

def arrowhead_illustration():
    def draw(ctx, width, height, frame_no, frame_count):
        setup(ctx, width, height, background=Color(1))

        ctx.set_source_rgba(*Color('black'))
        ctx.set_line_width(3)

        ## Draw lines with arrowhead
        a = (50, 50)
        b = (150, 250)
        polygon(ctx, (a, b), closed=False)
        ctx.stroke()
        arrowhead(ctx, a, b, length=12)
        ctx.stroke()

    make_image("/tmp/arrowhead-illustration.png", draw, 200, 300)

angle_illustration()
tick_illustration()
paratick_illustration()
arrowhead_illustration()
