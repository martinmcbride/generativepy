from generativepy.drawing import make_image, setup
from generativepy.geometry import text
from generativepy.color import Color

'''
Create a very simple image
'''

def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):

    setup(ctx, pixel_width, pixel_height, width=5, background=Color(0.4))

    ctx.set_source_rgba(*Color(0.5, 0, 0))
    ctx.rectangle(0.5, 0.5, 2.5, 1.5)
    ctx.fill()

    ctx.set_source_rgba(*Color(0, 0.75, 0, 0.5))
    ctx.rectangle(2, 0.25, 2.5, 1)
    ctx.fill()

    text(ctx, "Simple Image", 1, 3, size=0.5, color=Color('cadetblue'), font='Arial')


make_image("/tmp/simpleimage.png", draw, 500, 400)
