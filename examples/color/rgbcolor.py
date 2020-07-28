from generativepy.drawing import make_image
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    for i in range(200):
        for j in range(200):
            ctx.set_source_rgba(*Color(i/200, j/200, 0).rgba)
            ctx.rectangle(i + 50, j + 50, 1, 1)
            ctx.fill()

    for i in range(200):
        for j in range(200):
            ctx.set_source_rgba(*Color(i/200, 0, j/200).rgba)
            ctx.rectangle(i + 50, j + 300, 1, 1)
            ctx.fill()

    for i in range(200):
        for j in range(200):
            ctx.set_source_rgba(*Color(0, i/200, j/200).rgba)
            ctx.rectangle(i + 50, j + 550, 1, 1)
            ctx.fill()


make_image("/tmp/rgbcolor.png", draw, 300, 800)
