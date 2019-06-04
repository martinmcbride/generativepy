from generativepy import drawing, graph
from generativepy.color import Color

def draw(canvas):
    axes = graph.Axes(canvas)
    axes.draw()
    graph.plotCurve(axes, lambda x: x**2)
    graph.plotYXCurve(axes, lambda x: x**2, lineColor=Color(0, 0, 1))
    graph.plotPolarCurve(axes, lambda x: 6, lineColor=Color(0, 0.5, 0), range=(0, 1))


drawing.makeImage("/tmp/plot-graph.png", draw, pixelSize=(500, 500), startX=-1, startY=-1, width=12, background=drawing.Color(1, 1, 1), orientation=drawing.OR_MATH)
