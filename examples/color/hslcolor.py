from generativepy import drawing
from generativepy.drawing import makeImage, Color


def draw(canvas):
    drawing.colorMode(drawing.HSL)
    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(i/200, j/200, 0.5))
            canvas.point(i + 50, j + 50)

    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(i/200, 0.5, j/200))
            canvas.point(i + 50, j + 300)

    for i in range(200):
        for j in range(200):
            canvas.stroke(Color(0.5, i/200, j/200))
            canvas.point(i + 50, j + 550)


makeImage("/tmp/hslcolor.png", draw, pixelSize=(300, 800), background=Color(1))
