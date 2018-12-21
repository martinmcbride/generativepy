from generativepy import canvas


def draw(canvas):
    # Example, replace with your own code
    canvas.stroke((0.5, 0.5, 0))
    canvas.strokeWeight(0.05)
    points = ((0, 1.5),
              (1, -1),
              (-1.5, 0),
              (1, 1),
              (0, -1.5),
              (-1, 1),
              (1.5, 0),
              (-1, -1))
    canvas.polygon(points)


canvas.makeImage("/tmp/vector-origin.png", draw, pixelSize=(400, 400),
                       width=4, color=(1, 1, 1), startX=-2, startY=-2)
