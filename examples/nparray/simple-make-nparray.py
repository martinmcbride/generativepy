from generativepy.nparray import make_nparray
from generativepy.utils import temp_file

'''
make_nparray example
'''

def paint(array, pixel_width, pixel_height, frame_no, frame_count):
    array[10:150,60:300] = [255, 128, 0]

make_nparray(temp_file("simple-make-nparray.png"), paint, 500, 300)
