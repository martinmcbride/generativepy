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
    geometry.paratick(canvas, a, b)
    geometry.paratick(canvas, b, c, 3)
    geometry.paratick(canvas, c, d, 2)
    geometry.paratick(canvas, a, d, 3)


drawing.makeImage("/tmp/paramarkers.png", draw, pixelSize=(500, 500), width=6, background=drawing.Color(1, 1, 1), orientation=drawing.OR_MATH)
