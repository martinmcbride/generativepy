from generativepy import drawing


def draw(canvas):
    # Example, replace with your own code
    canvas.noStroke()
    canvas.fill((1, .5, 0))
    canvas.rect(0.5, 0.7, 2, 1)


drawing.makeImage("/tmp/vector.png", draw, pixelSize=(300, 200),
                 width=3, color=(1, 1, 1))
