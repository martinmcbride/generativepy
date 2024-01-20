# Author:  Martin McBride
# Created: 2021-06-06
# Copyright (C) 2021, Martin McBride
# License: MIT

"""
The `analytics` module provides functions for analysing the distribution of values in a NumPy array.

This is particularly useful when exploring generative art techniques such as fractal imaging. Often the result of the calculation will be a large array of
numerical values.

In order to create an image we usually need to convert the values into colours. To do this, it is useful to know how the values are distributed.

For example, if we run an imaging process and the output array contains values in the range 0 to 100, we could create a color map with 101 colours to map those
values onto a colour scheme.

But if we discovered that the output array contained values in the range 0 to 1000, we would need a different colour map. And if the range was 2000 to 2500, we
would probably want to subtract 2000 from each value to use a colour map in the range 0 to 500.

These functions will work on any NumPy array that has a numeric data type (which most arrays do). They are designed to work with single channel image data such
as greyscale data, or just the output from a fractal algorithm. That would be an array with shape `(height, width)`.

They can be used with multichannel data, such as RGB data, an array with shape `(height, width, 3)`. However in that case it would produce one value for all
the R, G amd B values combined.
"""
import numpy as np


def print_stats(array, title='stats'):
    """
    Prints the statistics for a NumPy array.

    This function takes a NumPy array, and calculates the minium, maximum, mean and median values.

    It prints the result to the console.

    `title` is printed before the stats. It can be useful if you are printing more than one set of statistics in a run.

    Args:

        array: NumPy array - the image data.
        title: str - the title to display (defaults to `stats`)
    """
    print(title)
    print('Min:', np.min(array))
    print('Max:', np.max(array))
    print('Mean:', np.mean(array))
    print('Median:', np.median(array))


def print_histogram(array, title='histogram', bins=10):
    """
   Prints the histogram for a NumPy array

    This function takes a NumPy array, and calculates a histogram of the values.

    It prints the result to the console.

    `title` is printed before the stats. It can be useful if you are printing more than one set of statistics in a run.

    Args:

        array: NumPy array - the image data.
        title: str - the title to display (defaults to `histogram`).
        bins: int - the number of bins in the histogram (defaults to 10).
    """


    data = np.histogram(array, bins)
    print(title)
    for count, bin in zip(*data):
        print(bin, count)
