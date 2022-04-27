import subprocess
from PIL import Image
import numpy as np
import random
import os


tex1 = '\n'.join([r'\documentclass[preview]{standalone}'
                  r'\usepackage{amsmath}',
                  r'\begin{document}',
                  r'\begin{equation*}'])
tex2 = '\n'.join([r'\end{equation*}'
                  r'\end{document}'])

def _crop(inname, outname, color):
    """
    Crop the image and colour it in a flat colour. The alpha channel is left unchanged.
    :param inname: base name of input file. Input image is {inname}1.png. The 1 is added by latex.
    :param outname: base name of output file. Output image is {outname}.png
    :param color:
    :return:
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
    cropbox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    image_data_new = image_data[cropbox[0]:cropbox[1]+1, cropbox[2]:cropbox[3]+1 , :]

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
    return filename, (cropbox[3]-cropbox[2], cropbox[1]-cropbox[0])

def _remove_ignore_errors(filename):
    """
    Remove a file but ignore errors. We shouldn;t fail just because a temp file didn't get deleted.
    :param filename:
    :return: None
    """
    try:
        os.remove(filename)
    except Exception:
        pass


def rasterise_formula(name, formula, color, dpi=600):
    """
    Convert a latex formula into a PNG image. The PNG image will be tightly cropped, with a transparent background and
    text in the selected colour.
    :param name: Name of the output images. String with no extension, eg "myformula". The final output will be stored
    using this name, in the current working folder, so if you are creating multiple formulae give each one a unique name
    :param formula: The forumal, as a latex string.
    :param color: Color object defining the required colour of the output.
    :param dpi: The resolution, in dpi. This indirectly controls the size of the image,
    :return: A tuple containing the filename of teh result (with a png extension) and the (width, height) of the image
    in pixels.
    """
    unique_name = "{}-{}".format(name, random.randint(100000, 999999))
    tex = '\n'.join([tex1, formula, tex2])
    tex_fn = '{}.tex'.format(unique_name)
    with open(tex_fn, 'w') as tex_file:
        tex_file.write(tex)
    process = subprocess.Popen('latex {}.tex'.format(unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen('dvipng -T tight -D {} {}.dvi'.format(dpi, unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.wait()

    filename, size = _crop(unique_name, name, color)

    _remove_ignore_errors("{}.aux".format(unique_name))
    _remove_ignore_errors("{}.log".format(unique_name))
    _remove_ignore_errors("{}.tex".format(unique_name))
    _remove_ignore_errors("{}.dvi".format(unique_name))
    _remove_ignore_errors("{}1.png".format(unique_name))

    return filename, size
