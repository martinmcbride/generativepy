from generativepy import drawing
from generativepy.drawing import makeImage, Color


def draw(canvas):
    canvas.stroke(Color(0, 0, 0))
    canvas.strokeWeight(20)
    canvas.strokeCap(drawing.ROUND)
    canvas.line(50, 50, 250, 50)

    canvas.strokeCap(drawing.SQUARE)
    canvas.line(50, 150, 250, 150)

    canvas.strokeCap(drawing.PROJECT)
    canvas.line(50, 250, 250, 250)


makeImage("/tmp/canvas-strokecap.png", draw, pixelSize=(300, 300), background=Color(1))
