from generativepy.bitmap import make_bitmap_frames
from generativepy.movie import save_frames
from generativepy.color import Color
from PIL import ImageDraw
from generativepy.utils import temp_file

'''
Create a simple bitmap image
'''

def paint(image, pixel_width, pixel_height, frame_no, frame_count):
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 10+frame_no*30, 300, 150+frame_no*30), fill=Color("tomato").as_rgbstr())


frames = make_bitmap_frames(paint, 500, 300, 4)
save_frames(temp_file("simple-make-bitmap-frames.png"), frames)