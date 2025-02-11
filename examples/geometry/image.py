from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Image

'''
Draw an image
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=500, background=Color(0.8))

    Image(ctx).of_file_position('cat.png', (50, 50)).paint()
    Image(ctx).of_file_position('cat.png', (300, 50)).scale(0.5).paint()

make_image("/tmp/geometry-image.png", draw, 400, 200)
