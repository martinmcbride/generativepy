from generativepy import drawing


def draw(canvas):
    # Example, replace with your own code
    canvas.noStroke()
    canvas.fill((1, .5, 0, 1))
    canvas.rect(0.5, 0.7, 2, 1)
    canvas.fill((0, 0, 1, 0.5))
    canvas.ellipse(1, 1, 0.5, 1.5)


drawing.makeImage("/tmp/vector-alpha.png", draw, pixelSize=(300, 200),
                  width=3, background=(1, 1, 1, 0), channels=4)
