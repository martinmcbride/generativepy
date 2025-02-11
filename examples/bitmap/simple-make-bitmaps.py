from generativepy.bitmap import make_bitmaps
from generativepy.color import Color
from PIL import ImageDraw
from generativepy.utils import temp_file

'''
make_bitmaps example
'''

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 10+frame_no*30, 300, 150+frame_no*30), fill=Color("tomato").as_rgbstr())


make_bitmaps(temp_file("simple-make-bitmaps.png"), paint, 500, 400, 4)
