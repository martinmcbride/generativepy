from generativepy import drawing

def draw(canvas):
    # Red lines should be very thick (1 and 2 units wide in user space)
    # Blue lines should be thinner and same as each other (1% of page size)
    canvas.strokeCap(drawing.SQUARE)
    canvas.stroke(drawing.Color(1, 0, 0))
    canvas.strokeWeight(1)
    canvas.line(2, 1, 2, 3)
    canvas.stroke(drawing.Color(0, 0, 1))
    canvas.strokeWeight(canvas.page2user(1))
    canvas.line(4, 1, 4, 3)
    canvas.scale(2)
    canvas.stroke(drawing.Color(0.5, 0, 0))
    canvas.strokeWeight(1)
    canvas.line(1, 1.5, 1, 2.5)
    canvas.stroke(drawing.Color(0, 0, 0.5))
    canvas.strokeWeight(canvas.page2user(1))
    canvas.line(2, 1.5, 2, 2.5)

drawing.makeImage("/tmp/math-line-width.png", draw, pixelSize=(500, 500), width=6, background=drawing.Color(1, 1, 1), orientation=drawing.OR_MATH)
