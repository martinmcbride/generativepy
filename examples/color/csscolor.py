from generativepy.drawing import make_image
from generativepy.color import Color

'''
In this example, similar to color.py, we set colours using CSS names.

See the color module for a list of colours, or look up "CSS named colours" on the web.
'''

def draw(ctx, width, height, frame_no, frame_count):
    # Set the background to 'white', using the paint function.
    # Color('white') creates a colour with r, g, and b set to 1. Since s#no alpha is specified, alpha is
    # set to 1 by default.
    # A Color object behaves like a 4-tuple (r, g, b, a), therefore *Color unpacks a colour into the
    # r, g, b, a values that set_source_rgba() requires.
    ctx.set_source_rgba(*Color('white'))
    ctx.paint()

    ctx.set_source_rgba(*Color('salmon'))
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('firebrick'))
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('fuchsia'))
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('deepskyblue'))
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color('hotpink'))
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    # *Color('lawngreen').rgb gets the rgb values of the 'lawngreen colour.
    # When we unpack this we get 3 parameters, which is what set_source_rgb requires.
    # We could have done:
    #
    #     ctx.set_source_rgba(*Color('lawngreen))
    #
    # This is just an example of how to retrieve 3 colour values if you need to
    ctx.set_source_rgb(*Color('lawngreen').rgb)
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    # Here we create a rectangle with a colour Color('navy', 0.4).
    # That is 'navy' with a 0.4 alpha value (40% opacity, ie 60% transparent).
    # This overlaps the previous rectangle, and you can see the background through it.
    ctx.set_source_rgba(*Color('navy', 0.4))
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()


make_image("/tmp/csscolor.png", draw, 500, 350)
