# Author:  Martin McBride
# Created: 2022-07-24
# Copyright (C) 2022, Martin McBride
# License: MIT
"""
The `formulas` module provides the ability to display formatted mathematical equations.

The module converts latex format equations into bitmap images, with text of any required colour and a transparent background.
The image can be displayed using the `Image` class, which allows positioning and scaling of the formula. It is also
possible to use the `Transform` class to apply general transforms to the formula image.

The image will be tightly cropped to include just the marked pixels, with no border.
"""
import subprocess
from PIL import Image
import numpy as np
import random
import os

def _create_tex(formula, packages):
    """
    Create tex from the formula and any optional packages.
    Return latex string
    """
    tex_elements = [r'\documentclass[preview]{standalone}', r'\usepackage{amsmath}']
    if packages:
        tex_elements += [r'\usepackage{' + package + '}' for package in packages]
    tex_elements += [r'\begin{document}', r'\begin{equation*}']
    tex_elements += [formula]
    tex_elements += [r'\end{equation*}', r'\end{document}']

    return "\n".join(tex_elements)

def _crop(inname, outname, color):
    """
    Crop the image and colour it in a flat colour. The alpha channel is left unchanged.

    Args:
        inname:  str - base name of input file. Input image is {inname}1.png. The 1 is added by latex.
        outname: str - base name of output file. Output image is {outname}.png
        color: `Color` - colour of the formula text
    """
    image=Image.open('{}1.png'.format(inname))
    image.load()

    image_data = np.asarray(image)
    shape = image_data.shape
    shape = (shape[0], shape[1], 4)
    image_temp = np.zeros(shape, dtype=np.uint8)
    for i in range(shape[0]):
        for j in range(shape[1]):
            image_temp[i][j][3] = 255 - image_data[i][j][0]

    image_data = image_temp
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]

    # If the image is empty, cropping will fail because non_empty_rows and non_empty_columns are empty. In that case
    # we should not crop the image
    if len(non_empty_rows) and len(non_empty_columns):
        cropbox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
        image_data_new = image_data[cropbox[0]:cropbox[1]+1, cropbox[2]:cropbox[3]+1, :]
        image_size = (cropbox[3]-cropbox[2], cropbox[1]-cropbox[0])
    else:
        image_data_new = image_data
        image_size = image_data_new.shape[0:2]

    image_data_colored = np.zeros_like(image_data_new)
    color_data = (color.r*255, color.g*255, color.b*255)
    for i in range(image_data_new.shape[0]):
        for j in range(image_data_new.shape[1]):
            image_data_colored[i][j][3] = image_data_new[i][j][3]
            image_data_colored[i][j][0] = color_data[0]
            image_data_colored[i][j][1] = color_data[1]
            image_data_colored[i][j][2] = color_data[2]

    new_image = Image.fromarray(image_data_colored)
    filename = '{}.png'.format(outname)
    new_image.save(filename)
    return filename, image_size

def _remove_ignore_errors(filename):
    """
    Remove a file but ignore errors. We shouldn;t fail just because a temp file didn't get deleted.

    Args:
        filename: str - the filename.
    """
    try:
        os.remove(filename)
    except Exception:
        pass


def rasterise_formula(name, formula, color, dpi=600, packages=None):
    """
    Convert a latex formula into a PNG image. The PNG image will be tightly cropped, with a transparent background and
    text in the selected colour.

    The default `dpi`value of 600 creates the formula using a text height of about 60 pixels. The exact size of the image
    depends on the formula used. The image is cropped tightly to the image area that includes the formula.

    You can change the image size by altering the `dpi` value - a smaller number creates a smaller image, larger value
    creates a larger image. Since the scaling is applied to the vector data, it is always rendered at the best quality
    at any size.

    You can also resize the image when it is drawn on the page, using the `scale` method of the `Image` class. This method
    can reduce the size of the formula with reasonable quality, but since it works on the bitmap data increasing the size
    will cause pixelation problems.

    The function return a tuple. The first element is the name of the PNG file where the output is stored. The output is
    always place in the current working directory. The filename will be base on tehe `name` parameter, but it will also
    have additional characters to avoid name clashes.

    The second element is a size tuple, `(width, height)`, giving the exact size of the output image. The image is tightly
    cropped so the dimensions can be used to align the image.

    Args:
        name: str - The base filename for the output PNG file. String with no extension, eg "myformula". The final
            output will be stored using this name, in the current working folder, so if you are creating multiple formulae give
            each one a unique name.
        formula: string - The formula, as a latex string.
        color: `Color` object - The colour that will be used to paint the formula.
        dpi: number - The nominal size of the formula. See usage.
        packages: sequence of strings - a list of the names of any required latex packages.  Any valid packages listed
                here will be imported into the Latex equation description so that they can be used in the formula.

    Returns:
        A tuple containing the filename of the result (with a png extension) and the (width, height) of the image
        in pixels.
    """
    unique_name = "{}-{}".format(name, random.randint(100000, 999999))
    tex = _create_tex(formula, packages)
    tex_fn = '{}.tex'.format(unique_name)
    with open(tex_fn, 'w') as tex_file:
        tex_file.write(tex)
    process = subprocess.Popen('latex -interaction=batchmode {}.tex'.format(unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.communicate()
    process.wait()

    process = subprocess.Popen('dvipng -T tight -D {} {}.dvi'.format(dpi, unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.communicate()
    process.wait()

    filename, size = _crop(unique_name, name, color)

    _remove_ignore_errors("{}.aux".format(unique_name))
    _remove_ignore_errors("{}.log".format(unique_name))
    _remove_ignore_errors("{}.tex".format(unique_name))
    _remove_ignore_errors("{}.dvi".format(unique_name))
    _remove_ignore_errors("{}1.png".format(unique_name))

    return filename, size
