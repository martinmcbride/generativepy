from generativepy.drawing import make_image
from generativepy.color import Color

'''
Create various coloured rectangles, using rgb amd rgba colours.

The rectangles are drawn using the Pycairo rectangle function.
'''

def draw(ctx, width, height, frame_no, frame_count):
    # Set the background to white, using the paint function.
    # Color(1) creates a grey value of 1 (ie white)
    # A Color object behaves like a 4-tuple (r, g, b, a), therefore *Color unpacks a colour into the
    # r, g, b, a values that set_source_rgba() requires.
    ctx.set_source_rgba(*Color(1))
    ctx.paint()

    # Set the colour to rgb(0.5, 0, 0), dark red. The alpha channel is automatically set to 1.
    # Even though we have set an rgb colour, the Color object still internally holds r, g, b, a so the
    # Color object still unpacks into 4 elements.
    ctx.set_source_rgba(*Color(0.5, 0, 0))
    ctx.rectangle(50, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0, 0, 0.5))
    ctx.rectangle(200, 50, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.8, 0.8, 0))
    ctx.rectangle(350, 50, 100, 100)
    ctx.fill()

    # Color(0.5).rgb creates a mid grey colour, then extracts its rgb property (0.5, 0.5, 0.5)
    # When we unpack this we get 3 parameters, which is what set_source_rgb requires.
    # We could have done:
    #
    #     ctx.set_source_rgba(*Color(0.5))
    #
    # This is just an example of how to retrieve 3 colour values if you need to
    ctx.set_source_rgb(*Color(0.5).rgb)
    ctx.rectangle(50, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.25))
    ctx.rectangle(200, 200, 100, 100)
    ctx.fill()

    ctx.set_source_rgba(*Color(0.8, 0.8, 0))
    ctx.rectangle(330, 180, 100, 100)
    ctx.fill()

    # Here we create a rectangle with a colour Color(1, 0, 1, 0.4).
    # That is magenta with a 0.4 alpha value (40% opacity, ie 60% transparent).
    # This overlaps the previous rectangle, and you can see the background through it.
    ctx.set_source_rgba(*Color(1, 0, 1, 0.4))
    ctx.rectangle(370, 220, 100, 100)
    ctx.fill()

# Create an image using the make_image function. THis calls our draw function to do the drawing.
make_image("/tmp/color.png", draw, 500, 350)
