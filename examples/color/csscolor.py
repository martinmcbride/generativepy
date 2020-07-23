from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).get_rgba())
    ctx.paint()

    ctx.set_source_rgba(*Color('salmon').get_rgba())
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('firebrick').get_rgba())
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('fuchsia').get_rgba())
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('deepskyblue').get_rgba())
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('hotpink').get_rgba())
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgb(*Color('lawngreen').get_rgb())
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('navy', 0.5).get_rgba())
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()


makeImage("/tmp/csscolor.png", draw, 500, 350)
