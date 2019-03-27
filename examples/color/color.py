from generativepy.drawing import makeImage, Color


def draw(canvas):
    canvas.noStroke()
    canvas.fill(Color(0.5, 0, 0))
    canvas.rect(50, 50, 100, 100)
    canvas.fill(Color(0, 0, 0.5))
    canvas.rect(200, 50, 100, 100)
    canvas.fill(Color(0.8, 0.8, 0))
    canvas.rect(350, 50, 100, 100)

    canvas.fill(Color(0.5))
    canvas.rect(50, 200, 100, 100)
    canvas.fill(Color(0.25))
    canvas.rect(200, 200, 100, 100)

    canvas.colorRange(255)
    canvas.fill(Color(200, 200, 0))
    canvas.rect(330, 180, 100, 100)
    canvas.fill(Color(255, 0, 255, 128))
    canvas.rect(370, 220, 100, 100)


makeImage("/tmp/color.png", draw, pixelSize=(500, 350), background=Color(1))
