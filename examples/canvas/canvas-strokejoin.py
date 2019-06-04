from generativepy import drawing
from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(canvas):
    canvas.stroke(Color(0, 0, 0))
    canvas.strokeWeight(15)
    canvas.strokeJoin(drawing.MITER)
    canvas.polygon([(50, 100), (250, 100), (80, 20)], False)

    canvas.strokeJoin(drawing.BEVEL)
    canvas.polygon([(50, 250), (250, 250), (80, 170)], False)

    canvas.strokeJoin(drawing.ROUND)
    canvas.polygon([(50, 400), (250, 400), (80, 320)], False)


makeImage("/tmp/canvas-strokejoin.png", draw, pixelSize=(300, 450), background=Color(1))
