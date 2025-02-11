from generativepy.bitmap import make_bitmap, Scaler
from generativepy.color import Color
from PIL import ImageDraw

'''
Draw a Henon attractor
'''

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, height=2, startx=-1.5, starty=-1)
    draw = ImageDraw.Draw(image)

    a = 1.4
    b = 0.3
    x, y = 0, 0
    for i in range(10000):
        draw.point(scaler.user_to_device(x, y), fill=Color("black").as_rgbstr())
        x, y = 1 - a*x*x + y, b*x


make_bitmap("/tmp/henon.png", paint, 500, 500)