from generativepy.nparray import make_nparrays
from generativepy.utils import temp_file

'''
make_nparrays example
'''

def paint(array, pixel_width, pixel_height, frame_no, frame_count):
    array[10+frame_no*30:150+frame_no*30, 60:300] = [255, 128, 0]

make_nparrays(temp_file("simple-make-nparrays.png"), paint, 500, 400, 4)
