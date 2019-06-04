from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(canvas):
    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(i/200, j/200, 0))
            canvas.point(i + 50, j + 50)

    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(i/200, 0, j/200))
            canvas.point(i + 50, j + 300)

    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(0, i/200, j/200))
            canvas.point(i + 50, j + 550)


makeImage("/tmp/rgbcolor.png", draw, pixelSize=(300, 800), background=Color(1))
