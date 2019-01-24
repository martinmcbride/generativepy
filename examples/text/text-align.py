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
    draw_text(canvas, "Left", 250, 50)
    canvas.textAlign(drawing.CENTER)
    draw_text(canvas, "Center", 250, 100)
    canvas.textAlign(drawing.RIGHT)
    draw_text(canvas, "Right", 250, 150)
    canvas.textAlign(drawing.LEFT, drawing.BOTTOM)
    draw_text(canvas, "gBottom", 250, 250)
    canvas.textAlign(drawing.LEFT, drawing.CENTER)
    draw_text(canvas, "gMiddle", 250, 350)
    canvas.textAlign(drawing.LEFT, drawing.TOP)
    draw_text(canvas, "gTop", 250, 450)

drawing.makeImage("/tmp/text-align.png", draw, pixelSize=(500, 500), background=drawing.Color(1, 1, 1))
