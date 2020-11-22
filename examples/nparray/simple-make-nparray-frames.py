from generativepy.nparray import make_nparray_frames
from generativepy.movie import save_frames
from generativepy.utils import temp_file

'''
make_nparray_frames example
'''

def paint(array, pixel_width, pixel_height, frame_no, frame_count):
    array[10+frame_no*30:150+frame_no*30, 60:300] = [255, 128, 0]


frames = make_nparray_frames(paint, 500, 300, 4)
save_frames(temp_file("simple-make-nparray-frames.png"), frames)