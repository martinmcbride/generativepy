from generativepy import drawing


def draw(canvas):
    # Example, replace with your own code
    canvas.background(drawing.Color(1, 0, 0))
    canvas.noStroke()
    canvas.fill((1, .5, 0))
    canvas.rect(0.5, 0.7, 2, 1)


drawing.makeImage("/tmp/vector.png", draw, pixelSize=(300, 200),
                  width=3, background=(1, 1, 1))
