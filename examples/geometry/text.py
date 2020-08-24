from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Text, Circle

'''
Create text using the geometry module.
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=5, background=Color(0.8))

    Text(ctx).of("Left", (0.5, 0.5)).font("Times").size(0.2).align_left().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (0.5, 0.7)).font("Times").size(0.2).align_left().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (0.5, 0.9)).font("Times").size(0.2).align_left().align_baseline().fill(Color('blue'))

    Text(ctx).of("Centre", (2.5, 0.5)).font("Times").size(0.2).align_center().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (2.5, 0.7)).font("Times").size(0.2).align_center().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (2.5, 0.9)).font("Times").size(0.2).align_center().align_baseline().fill(Color('blue'))

    Text(ctx).of("Right", (4.5, 0.5)).font("Times").size(0.2).align_right().align_baseline().fill(Color('blue'))
    Text(ctx).of("Aligned", (4.5, 0.7)).font("Times").size(0.2).align_right().align_baseline().fill(Color('red'))
    Text(ctx).of("Text", (4.5, 0.9)).font("Times").size(0.2).align_right().align_baseline().fill(Color('blue'))

    Circle(ctx).of_center_radius((1.9, 2), 0.02).fill(Color(0, 0, 1))
    Text(ctx).of("gTop", (2, 2)).font("Times").size(0.2).align_left().align_top().fill(Color('black'))

    Circle(ctx).of_center_radius((1.9, 2.5), 0.02).fill(Color(0, 0, 1))
    Text(ctx).of("gMid", (2, 2.5)).font("Times").size(0.2).align_left().align_middle().fill(Color('black'))

    Circle(ctx).of_center_radius((1.9, 3), 0.02).fill(Color(0, 0, 1))
    Text(ctx).of("gBase", (2, 3)).font("Times").size(0.2).align_left().align_baseline().fill(Color('black'))

    Circle(ctx).of_center_radius((1.9, 3.5), 0.02).fill(Color(0, 0, 1))
    Text(ctx).of("gBottom", (2, 3.5)).font("Times").size(0.2).align_left().align_bottom().fill(Color('black'))

make_image("/tmp/geometry-text.png", draw, 500, 500)
