from generativepy.drawing import make_image
from generativepy.color import Color

'''
In this example, similar to color.py, we set colours using hsl values.

hsl defines colours in terms of their hue, saturation and lightness
'''

def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1))
    ctx.paint()

    # We use Color.of_hsl() to create an HSL colour.
    # A hue of 0 gives pure red. We then set the saturation ot 0.5, which greys the colour
    # out a little, and lightness to 0.5 which creates a slightly dark red.
    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5))
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    # Same as before, but a hue of 0.33 gives the equivalent green colour
    ctx.set_source_rgba(*Color.of_hsl(0.33, 0.5, 0.5))
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    # Same as before, but a hue of 0.66 gives the equivalent blue colour
    ctx.set_source_rgba(*Color.of_hsl(0.66, 0.5, 0.5))
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.25, 0.5))
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.25))
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5))
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    # Here we create a rectangle with a colour Color.of_hsla(0.5, 0.5, 0.5, 0.3).
    # That is blue-green with a 0.3 alpha value (30% opacity, ie 70% transparent).
    # This overlaps the previous rectangle, and you can see the background through it.
    ctx.set_source_rgba(*Color.of_hsla(0.5, 0.5, 0.5, 0.3))
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()

make_image("/tmp/hslcolor.png", draw, 500, 350)
