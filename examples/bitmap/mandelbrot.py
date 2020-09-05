from generativepy.bitmap import make_bitmap, Scaler
from generativepy.color import Color
from PIL import ImageDraw

'''
Draw a Mandelbrot fractal
'''

def mandelbrot(c):
    z, n = 0, 0
    while abs(z) <= 2:
        if n > 100:
            return 0
        z = z*z + c
        n += 1
    return n

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    scaler = Scaler(pixel_width, pixel_height, width=3, height=2, startx=-2, starty=-1)
    draw = ImageDraw.Draw(image)

    a = 1.4
    b = 0.3
    x, y = 0, 0
    for i in range(pixel_width):
        for j in range(pixel_height):
            c = complex(*scaler.device_to_user(i, j))
            if not mandelbrot(c):
                draw.point((i, j), fill=Color("black").as_rgbstr())


make_bitmap("/tmp/mandelbrot.png", paint, 600, 400)