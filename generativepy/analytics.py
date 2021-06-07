# Author:  Martin McBride
# Created: 2021-06-06
# Copyright (C) 2021, Martin McBride
# License: MIT

import numpy as np


def print_stats(array, title='stats'):
    '''
    Print the stats of a numpy array
    :param array: the array to analyse
    :param title: Title to display
    :return:
    '''
    print(title)
    print('Min:', np.min(array))
    print('Max:', np.max(array))
    print('Mean:', np.mean(array))
    print('Median:', np.median(array))


def print_histogram(array, title='histogram', bins=10):
    '''
    Print the histogram of a numpy array
    :param array: the array to analyse
    :param title: Title to display
    :param bins: Number of bins to use
    :return:
    '''
    data = np.histogram(array, bins)
    print(title)
    for count, bin in zip(*data):
        print(bin, count)
