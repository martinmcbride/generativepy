# Author:  Martin McBride
# Created: 2020-12-28
# Copyright (C) 2020, Martin McBride
# License: MIT

from generativepy.utils import temp_file
from pathlib import Path
from generativepy.drawing import make_image

def compare_images(path1, path2):

def run_image_test(name, draw, pixel_width, pixel_height, channels=3):
    # Create test output folder
    folder_name = 'genpy-test-images'
    out_folder = temp_file(folder_name)
    Path(out_folder).mkdir(exist_ok=True)

    # Warn if output file exists
    out_file = temp_file(folder_name, name)
    if Path(out_file).exists():
        print("WARNING temp file {} already exists".format(name))

    # Create the test image file
    make_image(out_file, draw, pixel_width, pixel_height, channels)