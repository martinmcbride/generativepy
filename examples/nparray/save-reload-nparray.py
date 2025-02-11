from generativepy.nparray import make_nparray_frame, save_nparray, load_nparray
from generativepy.utils import temp_file
from generativepy.movie import save_frame

'''
saving and loading nparray example
'''

def paint(array, pixel_width, pixel_height, frame_no, frame_count):
    array[10:150,60:300] = [255, 255, 0]

frame = make_nparray_frame(paint, 500, 300)
save_nparray(temp_file("saved-nparray.dat"), frame)
frame2 = load_nparray(temp_file("saved-nparray.dat"))
save_frame(temp_file("save-reload-nparray.png"), frame2)