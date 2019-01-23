from generativepy.drawing import makeImage, Color


def draw(canvas):
    canvas.image('circles.png', 10, 10)


makeImage("/tmp/image.png", draw, pixelSize=(300, 200), background=Color(1, 0, 1))
