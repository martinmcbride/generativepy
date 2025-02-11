from generativepy.bitmap import make_bitmap
from generativepy.color import Color
from PIL import ImageDraw
from generativepy.utils import temp_file

'''
Create a simple bitmap image
'''

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 10, 300, 150), fill=Color("tomato").as_rgbstr())


make_bitmap(temp_file("simple-make-bitmap.png"), paint, 500, 300)
