from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).get_rgba())
    ctx.paint()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5).get_rgba())
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0.33, 0.5, 0.5).get_rgba())
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0.66, 0.5, 0.5).get_rgba())
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.25, 0.5).get_rgba())
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.25).get_rgba())
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5).get_rgba())
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsla(0.5, 0.5, 0.5, 0.5).get_rgba())
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()

makeImage("/tmp/hslcolor.png", draw, 500, 350)
