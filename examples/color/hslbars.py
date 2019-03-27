from generativepy import drawing
from generativepy.drawing import makeImage, Color


def draw(canvas):
    canvas.colorMode(drawing.HSL)
    for i in range(200):
        for j in range(50):
            canvas.stroke(Color(i/200, 1, 0.5))
            canvas.point(i + 50, j + 50)

    for i in range(200):
        for j in range(50):
            canvas.stroke(Color(0.25, i/200, 0.5))
            canvas.point(i + 50, j + 150)

    for i in range(200):
        for j in range(50):
            canvas.stroke(Color(0.25, 1, i/200))
            canvas.point(i + 50, j + 250)


makeImage("/tmp/hslbars.png", draw, pixelSize=(300, 350), background=Color(1))
