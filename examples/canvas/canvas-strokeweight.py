from generativepy.drawing import makeImage, Color


def draw(canvas):
    canvas.stroke(Color(0, 0, 0))
    canvas.strokeWeight(1)
    canvas.line(50, 50, 250, 50)

    canvas.strokeWeight(5)
    canvas.line(50, 150, 250, 150)

    canvas.strokeWeight(10)
    canvas.line(50, 250, 250, 250)


makeImage("/tmp/canvas-strokeweight.png", draw, pixelSize=(300, 300), background=Color(1))
