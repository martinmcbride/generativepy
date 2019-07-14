from generativepy.drawing import makeImage
from generativepy.color import Color, Gradient


def draw(canvas):
    gradient = Gradient().add(100, Color(1, 0, 0)).add(200, Color(0, 1, 0)).add(350, Color(0, 0, 1))
    for i in range(50, 450):
        canvas.stroke(gradient.getColor(i))
        canvas.line(i, 50, i, 150)


makeImage("/tmp/rgbgradient.png", draw, pixelSize=(500, 200), background=Color(1))
