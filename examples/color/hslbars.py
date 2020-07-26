from generativepy import drawing
from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(i / 200, 1, 0.5).rgba)
        ctx.rectangle(i + 50, 50, 1, 50)
        ctx.fill()

    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(0.25, i/200, 0.5).rgba)
        ctx.rectangle(i + 50, 150, 1, 50)
        ctx.fill()

    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(0.25, 1, i/200).rgba)
        ctx.rectangle(i + 50, 250, 1, 50)
        ctx.fill()


makeImage("/tmp/hslbars.png", draw, 300, 350)
