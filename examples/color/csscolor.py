from generativepy.drawing import makeImage
from generativepy.color import Color, HSL


def draw(canvas):
    canvas.noStroke()
    canvas.colorMode(HSL)
    canvas.colorRange(255)
    canvas.fill(Color('salmon'))
    canvas.rect(50, 50, 100, 100)
    canvas.fill(Color('firebrick'))
    canvas.rect(200, 50, 100, 100)
    canvas.fill(Color('fuchsia'))
    canvas.rect(350, 50, 100, 100)

    canvas.fill(Color('deepskyblue'))
    canvas.rect(50, 200, 100, 100)
    canvas.fill(Color('hotpink'))
    canvas.rect(200, 200, 100, 100)

    canvas.colorRange(255)
    canvas.fill(Color('lawngreen'))
    canvas.rect(330, 180, 100, 100)
    canvas.fill(Color('navy', 128))
    canvas.rect(370, 220, 100, 100)


makeImage("/tmp/csscolor.png", draw, pixelSize=(500, 350), background=Color(1))
