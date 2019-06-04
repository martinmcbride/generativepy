from generativepy import drawing, movie
from generativepy.color import Color


def draw(canvas):
    ##Draw guide lines

    canvas.stroke(Color(1, 0, 0))
    canvas.strokeWeight(0.2)
    canvas.fill(drawing.Color(0, 1, 0))
    canvas.rect(1, 1, 1.5, 1)
    canvas.fill(drawing.Color(0, 0, 1))
    canvas.rect(3, 3, 1.5, 1)


frame = movie.makeFrame(draw, pixelSize=(500, 500),
                  width=5, background=Color(1, 1, 1))
movie.saveFrame('/tmp/frame.png', frame)
