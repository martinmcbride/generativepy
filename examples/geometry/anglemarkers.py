from generativepy import drawing, geometry

def draw(canvas):
    canvas.fill(drawing.Color(.5, .5, 1))
    canvas.stroke(drawing.Color(0, 0, 1))
    canvas.strokeWeight(canvas.page2user(0.5))
    a = (1, 1)
    b = (3, 1)
    c = (4, 4)
    d = (1, 4)

    canvas.polygon([a, b, c, d])
    canvas.noFill()
    geometry.angleMarker(canvas, b, a, d)
    geometry.angleMarker(canvas, c, b, a, 2)
    geometry.angleMarker(canvas, d, c, b, 3)
    geometry.angleMarker(canvas, a, d, c, rightangle=True)
    geometry.tick(canvas, a, b)
    geometry.tick(canvas, b, c, 3)
    geometry.tick(canvas, c, d, 2)
    geometry.tick(canvas, a, d, 3)


drawing.makeImage("/tmp/anglemarkers.png", draw, pixelSize=(500, 500), width=6, background=drawing.Color(1, 1, 1), orientation=drawing.OR_MATH)
