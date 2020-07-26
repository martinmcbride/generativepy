from generativepy.movie import makeFrames, saveFrames
from generativepy.color import Color


def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    ctx.set_source_rgba(*Color(0.5, 0, 0).rgba)
    ctx.rectangle(50+20*frame_no, 50+10*frame_no, 100, 100)
    ctx.fill()

frames = makeFrames(draw, 500, 350, 20)
saveFrames("/tmp/movie", frames)
