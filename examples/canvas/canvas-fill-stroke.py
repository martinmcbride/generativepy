from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(canvas):
    canvas.stroke(Color(1, 0, 0))
    canvas.noFill()
    canvas.rect(50, 50, 100, 100)

    canvas.noStroke()
    canvas.fill(Color(0, 0.5, 0))
    canvas.rect(200, 50, 100, 100)

    canvas.stroke(Color(0, 0, 0.5))
    canvas.fill(Color(1, 1, 0))
    canvas.rect(350, 50, 100, 100)


makeImage("/tmp/canvas-fill-stroke.png", draw, pixelSize=(500, 200), background=Color(1))
