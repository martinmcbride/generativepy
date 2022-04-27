from generativepy.drawing import make_image, setup
from generativepy.color import Color
from generativepy.geometry import Image, Text
from generativepy.formulas import rasterise_formula

'''
Create some formulae
'''

def draw(ctx, width, height, frame_no, frame_count):
    setup(ctx, width, height, width=800, background=Color(0.8))

    image1, size1 = rasterise_formula("cosh-formula", r"\cosh{x} = \frac{e^{x}+e^{-x}}{2}", Color("dodgerblue"))
    image2, size2 = rasterise_formula("quadratic", r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}", Color("crimson"), dpi=400)
    Image(ctx).of_file_position(image1, (50, 50)).paint()
    Text(ctx).of("Size1 = " + str(size1), (50, 500)).size(20).fill(Color(0))
    Image(ctx).of_file_position(image2, (50, 300)).paint()
    Text(ctx).of("Size2 = " + str(size2), (250, 500)).size(20).fill(Color(0))

make_image("/tmp/maths-formula.png", draw, 800, 600)
