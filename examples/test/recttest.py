from generativepy import drawing


def draw(canvas):
    ##Draw guide lines
    canvas.stroke([0, 0, 0])
    canvas.strokeWeight(0.02)
    for i in range(1, 5):
        canvas.line(0, i, 5, i)
        canvas.line(i, 0, i, 5)
    canvas.noStroke()
    canvas.fill((1, .5, 0))
    canvas.rectMode(drawing.CORNER)
    canvas.rect(1, 1, 1.5, 1)
    canvas.rectMode(drawing.CORNERS)
    canvas.rect(3, 1, 4.5, 2)
    canvas.rectMode(drawing.CENTER)
    canvas.rect(2, 3, 1.5, 1)
    canvas.rectMode(drawing.RADIUS)
    canvas.rect(4, 3, .75, .5)


drawing.makeImage("/tmp/recttest.png", draw, pixelSize=(500, 500),
                  width=5, background=(1, 1, 1))
