from generativepy import drawing, equation

def draw(canvas):
    img = equation.getEquationImage('x^2')
    canvas.image(img, 100, 100)


drawing.makeImage("/tmp/equation.png", draw, pixelSize=(500, 500), background=drawing.Color(1, 1, 1))
