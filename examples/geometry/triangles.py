from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import triangle, Triangle

'''
Create triangles using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=500, background=Color(0.8))

    # The triangle function is a convenience function that adds a triangle as a new path.
    # You can fill or stroke it as you wish.
    triangle(ctx, (100, 100), (150, 50), (200, 150))
    ctx.set_source_rgba(*Color(1, 0, 0))
    ctx.fill()

    Triangle(ctx).of_corners((300, 100), (300, 150), (400, 200)).stroke(Color('orange'), 10)

make_image("/tmp/geometry-triangle.png", draw, 500, 500)
