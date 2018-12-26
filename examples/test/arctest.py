from generativepy import drawing


def draw(canvas):
    ##Draw guide lines
    canvas.stroke([0, 0, 0])
    canvas.strokeWeight(0.02)
    for i in range(1, 5):
        canvas.line(0, i, 5, i)
        canvas.line(i, 0, i, 5)
    canvas.stroke(drawing.Color(0, 1, 0.5))
    canvas.fill((1, .5, 0))
    canvas.ellipseMode(drawing.CORNER)
    canvas.arc(1, 1, 1.5, 1, 0, 1.57, drawing.OPEN)
    canvas.ellipseMode(drawing.CORNERS)
    canvas.arc(3, 1, 4.5, 2, 0, 1.57, drawing.CHORD)
    canvas.ellipseMode(drawing.CENTER)
    canvas.arc(2, 3, 1.5, 1, 0, 1.57, drawing.PIE)
    canvas.ellipseMode(drawing.RADIUS)
    canvas.arc(4, 3, .75, .5, 0, 1.57, drawing.OPEN)


drawing.makeImage("/tmp/arctest.png", draw, pixelSize=(500, 500),
                  width=5, background=(1, 1, 1))
