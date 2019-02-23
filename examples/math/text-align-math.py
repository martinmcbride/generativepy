from generativepy import drawing

def draw_text(canvas, txt, x, y):
    canvas.fill(drawing.Color(1, 0, 0))
    canvas.noStroke()
    canvas.ellipseMode(drawing.RADIUS)
    canvas.ellipse(x, y, 5, 5)
    canvas.fill(drawing.Color(0, 0, 0))
    canvas.text(txt, x, y)

def draw(canvas):
    canvas.textSize(30)
    draw_text(canvas, "Left", 250, 500-50)
    canvas.textAlign(drawing.CENTER)
    draw_text(canvas, "Center", 250, 500-100)
    canvas.textAlign(drawing.RIGHT)
    draw_text(canvas, "Right", 250, 500-150)
    canvas.textAlign(drawing.LEFT, drawing.BOTTOM)
    draw_text(canvas, "gBottom", 250, 500-250)
    canvas.textAlign(drawing.LEFT, drawing.CENTER)
    draw_text(canvas, "gMiddle", 250, 500-350)
    canvas.textAlign(drawing.LEFT, drawing.TOP)
    draw_text(canvas, "gTop", 250, 500-450)

drawing.makeImage("/tmp/text-align-math.png", draw, pixelSize=(500, 500), background=drawing.Color(1, 1, 1), orientation=drawing.OR_MATH)
