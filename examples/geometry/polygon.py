from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import polygon, Polygon

'''
Create polygons using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=500, background=Color(0.8))

    # The polygon function is a convenience function that adds a polygon as a new path.
    # You can fill or stroke it as you wish.
    polygon(ctx, ((100, 100), (150, 50), (200, 150), (200, 200)))
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    Polygon(ctx).of_points([(300, 100), (300, 150), (400, 200), (450, 100)]).open().stroke(Color('orange'), 10)

make_image("/tmp/geometry-polygon.png", draw, 500, 500)
