# Author:  Martin McBride
# Created: 2020-11-22
# Copyright (C) 2020, Martin McBride
# License: MIT

import numpy as np
from generativepy.movie import save_frame, save_frames
from generativepy.color import make_colormap

def make_nparray_frame(paint, pixel_width, pixel_height, channels=3, out=None):
    """
    Create a frame using numpy

    Args:
        paint: function - the paint function.
        pixel_width: int - width in pixels.
        pixel_height: int - height in pixels.
        channels: int - 1 for greyscale, 3 for rgb, 4 for rgba.
        out: numpy array - optional array to hold result. Must be correct width, height and channels, but can be any int type.

    Returns:
        A numpy array frame buffer
    """
    if out is not None:
        if out.shape != (pixel_height, pixel_width, channels):
            raise ValueError('out array shape not compatible with image dimensions')
        array = out
    else:
        array = np.full((pixel_height, pixel_width, channels), 255, dtype=np.uint)
    paint(array, pixel_width, pixel_height, 0, 1)
    array = np.clip(array, 0, 255).astype(np.uint8)
    return array

def make_nparray_data(paint, pixel_width, pixel_height, channels=3, dtype=np.uint):
    """
    Create a data array using numpy.

    This is similar to `make_nparray_frame` except that it produce a general purpose numpy array rather than a
    frame buffer. The difference is that the data from this function isn't constrained to the range 0-255.

    The data can be outside that normal range, and it can also be a different type (eg signed integer or floating point).
    This allows the method to be used for storing intermediate data such as per pixel counts.

    Args:
        paint: function - the paint function.
        pixel_width: int - width in pixels.
        pixel_height: int - height in pixels.
        channels: int - 1 for greyscale, 3 for rgb, 4 for rgba.
        dtype: numpy data type - the type of the array.

    Returns:
        A numpy array
    """
    array = np.full((pixel_height, pixel_width, channels), 0, dtype=dtype)
    paint(array, pixel_width, pixel_height, 0, 1)
    return array

def make_nparray_frames(paint, pixel_width, pixel_height, count, channels=3):
    """
    Create a frame sequence using numpy.

    This function returns a lazy iterator that can be used to access the sequence. Images will be
    created as they are requested.

    Args:
        paint: function - the paint function.
        pixel_width: int - width in pixels.
        pixel_height: int - height in pixels.
        count: int - number of frames ot create.
        channels: int - 1 for greyscale, 3 for rgb, 4 for rgba.

    Yields:
        Lazy iterator of frames.
    """
    for i in range(count):
        array = np.full((pixel_height, pixel_width, channels), 255, dtype=np.uint)
        paint(array, pixel_width, pixel_height, i, count)
        array = np.clip(array, 0, 255).astype(np.uint8)
        yield array


def make_nparray(outfile, paint, pixel_width, pixel_height, channels=3):
    """
    Create a PNG file using numpy.

    Args:
        outfile: str - Name of output file.
        paint: function - the paint function.
        pixel_width: int - width in pixels.
        pixel_height: int - height in pixels.
        channels: int - 1 for greyscale, 3 for rgb, 4 for rgba.
    """
    frame = make_nparray_frame(paint, pixel_width, pixel_height, channels)
    save_frame(outfile, frame)

def make_nparrays(outfile, paint, pixel_width, pixel_height, count, channels=3):
    """
    Create a set of PNG files using numpy.

    Args:
        outfile: str - Name of output file.
        paint: function - the paint function.
        pixel_width: int - width in pixels.
        pixel_height: int - height in pixels.
        count: int - number of frames to create.
        channels: int - 1 for greyscale, 3 for rgb, 4 for rgba.
    """
    frames = make_nparray_frames(paint, pixel_width, pixel_height, count, channels)
    save_frames(outfile, frames)

def overlay_nparrays(array1, array2):
    """
    Overlay array2 on top of array1. Any pixels in array2 that are fully white are treated as transparent.

    Both frames nust be same size, and both must be 4 channel RGBA data.

    Args:
        array1: numpy frame - first (lower) frame.
        array2: numpy frame - second (upper) frame.

    Returns:
        A numpy array frame buffer
    """

    if (array1.shape[0] != array2.shape[0]
            or array1.shape[1] != array2.shape[1]
            or array1.shape[2] != 4
            or array2.shape[2] != 4):
        raise ValueError("array1 and array2 must be same shape and must contain 4 channel (RGBA) data.")

    # Create a mask. The mask has value 255 if the corresponding array2 pixel is pure white.
    m0 = array2[:, :, 0]
    m1 = array2[:, :, 1]
    m2 = array2[:, :, 2]
    mask = m0 & m1 & m2 # Bitwise AND of RGB values is 255 only if all 3 values are 255.

    # Extend the mask to be width by height by 4 to match image data
    mask = np.repeat(mask[:, :, np.newaxis], 4, axis=2)

    # Array full of 255 for comparison
    white = np.full_like(mask, 255)

    # Create a merged image, using the array1 pixel if the mask is white, else array2
    image = np.where(mask==white, array1, array2)
    return image

def save_nparray(outfile, array):
    """
    Save a general array to file in mumpy format. The saved file is not an image file.

    The file created can be read back in using `load_nparray`.

    Args:
        outfile: str - numpy file path including extension.
        array: numpy array - data to be saved.
    """
    with open(outfile, 'wb') as f:
        np.save(f, array)

def save_nparray_image(outfile, array):
    """
    Save an array to an image file.

    Args:
        outfile: str - image file path including extension.
        array: numpy array - data to be saved.
    """
    array = np.clip(array, 0, 255).astype(np.uint8)
    save_frame(outfile, array)

def load_nparray(infile):
    """
    Load a numpy array from file

    Args:
        infile: str - file path including extension.

    Returns:
        A numpy array. No checking is done on the array.
    """
    with open(infile, 'rb') as f:
        return np.load(f)

def make_npcolormap(length, colors, bands=None, channels=3):
    """
    Create a colormap, a list of varying colors, as a numpy array.

    Args:
        length: - int, required size of list
        colors: - tuple of Color objects - the list of colours, must be at least 2 long.
        bands: tuple of numbers - Relative size of each band. bands[i] gives the size of the band between color[i] and color[i+1].
                                  len(bands) must be exactly 1 less than len(colors). If bands is None, equal bands will be used.
        channels: int 3 for RGB, 4 for RGBA

    Returns:
        An array of shape (length, channels) containing the RGB(A) values for each entry, as integers from 0-255
    """

    colors = make_colormap(length, colors, bands)

    npcolormap = np.zeros((length, channels), dtype=np.uint8)
    for i in range(length):
        rgba = colors[i].as_rgba_bytes()
        npcolormap[i, 0] = rgba[0]
        npcolormap[i, 1] = rgba[1]
        npcolormap[i, 2] = rgba[2]
        if channels==4:
            npcolormap[i, 3] = rgba[3]

    return npcolormap

def apply_npcolormap(out, counts, npcolormap):
    """
    Apply a color map to an array of counts, filling an existing output array

    Args:
        out: numpy array - the output array, height x width x channels (channels is 3 or 4).
        counts: numpy array - the counts array, height x width, count range 0 to max_count.
        npcolormap: numpy array - a numpy color map, must have at least maxcount+1 elements.
    """

    if out.shape[0] != counts.shape[0] or out.shape[1] != counts.shape[1]:
        raise ValueError('out and counts are incompatible shapes')

    if np.max(counts) > npcolormap.shape[0]:
        raise ValueError('npcolormap too small for maximum value in counts array')

    out[...] = npcolormap[counts]