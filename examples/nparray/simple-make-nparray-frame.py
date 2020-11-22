from generativepy.nparray import make_nparray_frame
from generativepy.movie import save_frame
from generativepy.utils import temp_file

'''
make_nparray_frame example
'''

def paint(array, pixel_width, pixel_height, frame_no, frame_count):
    array[10:150,60:300] = [255, 128, 0]


frame = make_nparray_frame(paint, 500, 300)
save_frame(temp_file("simple-make-nparray-frame.png"), frame)