# Author:  Martin McBride
# Created: 2020-12-28
# Copyright (C) 2020, Martin McBride
# License: MIT

from generativepy.utils import temp_file
from pathlib import Path
from PIL import Image
from PIL import ImageChops
import os

def compare_images(path1, path2):
    with Image.open(path1) as im1:
        with Image.open(path2) as im2:
            if im1.size != im2.size:
                return False
            if im1.mode != im2.mode:
                return False
            diff = ImageChops.difference(im1, im2)
            if diff.getbbox():
                return False

    return True


def run_image_test(name, creator):
    """
    Create an image and check it matches the reference image
    :param name: test name (used as the image file name)
    :param creator: a function that takes a filepath ans creates an image
    :return:
    """
    # Create test output folder
    out_folder_name = 'genpy-test-images'
    ref_folder_name = 'images'
    out_folder = temp_file(out_folder_name)
    Path(out_folder).mkdir(exist_ok=True)

    # Warn if output file exists, or if reference file doesn't exist
    out_file = temp_file(out_folder_name, name)
    ref_file = os.path.join(ref_folder_name, name)
    if Path(out_file).exists():
        print("WARNING temp file {} already exists".format(out_file))
    if not Path(ref_file).exists():
        print("WARNING reference file {} doesn't exist".format(ref_file))

    # Create the test image file
    creator(out_file)
    return compare_images(out_file, ref_file)
