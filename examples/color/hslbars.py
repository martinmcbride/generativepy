from generativepy.drawing import make_image
from generativepy.color import Color

'''
Create colour bars to show the effect of varying h, s, l
'''

def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(0))
    ctx.paint()

    # Vary hue, with s = 1, l = 0.5.
    # The hue is the position on the colour circle:
    #  - hue 0 is pure red
    #  - as hue increases the colour moves through yellow towards green
    #  - hue 0.33 is pure green
    #  - as hue increases the colour moves through cyan towards blue
    #  - hue 0.66 is pure blue
    #  - as hue increases the colour moves through magenta towards red
    #  - as the hue approaches 1, the colour goes back to pure red.
    # This is a circular parameter, th eci#ycle starts again at 1
    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(i / 200, 1, 0.5))
        ctx.rectangle(2*i + 100, 100, 2, 100)
        ctx.fill()

    # Vary saturation, with h = 0.33 (green), l = 0.5.
    # With saturation 1, the colour is pure (fully saturated).
    # Reducing the saturation makes the colour more "grey".
    # When the saturation is 0, the colour is totally grey. All hues look identical ar zero saturation,
    # they all become the same grey (the shade og grey depends on the lightness value)
    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(0.33, i/200, 0.5))
        ctx.rectangle(2*i + 100, 300, 2, 100)
        ctx.fill()

    # Vary lightness, with h = 0.33 (green), s = 1.
    # Changing the lightness creates lighter or darker versions of the same colour,
    # rather like looking at the same object in a brighter or darker room.
    # When lightness is 0, all colours are black. When lightness is 1, all colours are white.
    for i in range(200):
        ctx.set_source_rgba(*Color.of_hsl(0.33, 1, i/200))
        ctx.rectangle(2*i + 100, 500, 2, 100)
        ctx.fill()


make_image("/tmp/hslbars.png", draw, 600, 700)
