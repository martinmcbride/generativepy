# Author:  Martin McBride
# Created: 2020-11-22
# Copyright (C) 2020, Martin McBride
# License: MIT

import sys
import tempfile
import os.path
import math

def correct_pycairo_byte_order(array, channels):
    '''
    If byte ordering is little endian, bitmap data from Pycairo needs swapping
    Convert a numpy array from BGR/BGRA ordering to RGB/RGBA.
    Conversion is performed in place
    :param array: numpy array
    :param channels: number of colour channels (3 or 4 for RGB or RGBA)
    :return: converted array (will be original array if no conversion needed)
    '''

    if sys.byteorder == 'little' and array.ndim == 3:
        if channels==3:
            array[:, :, [0, 1, 2]] = array[:, :, [2, 1, 0]]
        elif channels==4:
            array[:, :, [0, 1, 2, 3]] = array[:, :, [2, 1, 0, 3]]

    return array

def temp_file(*names):
    '''
    Create a temporary file name.
    If *name has one element, return <temp>/name[0]
    If *name has two element, return <temp>/name[0]/name[1] etc
    :param names: one or more names
    :return:
    '''

    folder = tempfile.gettempdir()
    return os.path.join(folder, *names)

def vector_a_b(a, b):
    '''
    DEPRECATED - remove after fixing geometry usage
    Return vector from point a to point b
    :param a: 2-tuple point x, y
    :param b: 2-tuple point x, y
    :return: 2-tuple vector
    '''
    return b[0]-a[0], b[1]-a[1]

def vector_unit(a):
    '''
    DEPRECATED - remove after fixing geometry usage
    Return unit vector for a
    :param a: 2-tuple vector x, y
    :return: 2-tuple vector
    '''
    length = math.sqrt(a[0]*a[0] + a[1]*a[1])
    return a[0]/length, a[1]/length




