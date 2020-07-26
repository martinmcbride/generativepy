from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    ctx.set_source_rgba(*Color(0.5, 0, 0).rgba)
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0, 0, 0.5).rgba)
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.8, 0.8, 0).rgba)
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.5).rgba)
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.25).rgba)
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgb(*Color(0.8, 0.8, 0).rgb)
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(1, 0, 1, 0.5).rgba)
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()

makeImage("/tmp/color.png", draw, 500, 350)
