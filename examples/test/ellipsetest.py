from generativepy import drawing


def draw(canvas):
    ##Draw guide lines
    canvas.stroke(drawing.Color(0, 0, 0))
    canvas.strokeWeight(0.02)
    for i in range(1, 5):
        canvas.line(0, i, 5, i)
        canvas.line(i, 0, i, 5)
    canvas.noStroke()
    canvas.fill(drawing.Color(1, .5, 0))
    canvas.ellipseMode(drawing.CORNER)
    canvas.ellipse(1, 1, 1.5, 1)
    canvas.ellipseMode(drawing.CORNERS)
    canvas.ellipse(3, 1, 4.5, 2)
    canvas.ellipseMode(drawing.CENTER)
    canvas.ellipse(2, 3, 1.5, 1)
    canvas.ellipseMode(drawing.RADIUS)
    canvas.ellipse(4, 3, .75, .5)


drawing.makeImage("/tmp/ellipsetest.png", draw, pixelSize=(500, 500),
                  width=5, background=drawing.Color(1, 1, 1))
