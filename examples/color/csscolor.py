from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    ctx.set_source_rgba(*Color('salmon').rgba)
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('firebrick').rgba)
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('fuchsia').rgba)
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('deepskyblue').rgba)
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('hotpink').rgba)
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgb(*Color('lawngreen').rgb)
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('navy', 0.5).rgba)
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()


makeImage("/tmp/csscolor.png", draw, 500, 350)
