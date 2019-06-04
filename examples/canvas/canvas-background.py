from generativepy.drawing import makeImage
from generativepy.color import Color


def draw(canvas):
    canvas.background(Color(0, 0, 0.2))


makeImage("/tmp/canvas-background.png", draw, pixelSize=(300, 200))
