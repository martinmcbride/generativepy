# Author:  Martin McBride
# Created: 2019-05-12
# Copyright (C) 2019, Martin McBride
# License: MIT

import imageio
import subprocess


def saveAnimatedGif(filepath, frames, delay, loop=0):
    '''
    Save a set of frames as an animated GIF.
    Requires gifsicle to be installed
    :param filepath: Output filepath
    :param frames: sequence fo frames
    :param delay: Delay between frames in seconds (eg 0.2 for frame rate of 5 frames per second)
    :param loop: Not implemented
    :return:
    '''
    if not filepath.lower().endswith('.gif'):
        filepath += '.gif'
    images = list(frames)
    imageio.mimsave(filepath, images, duration=delay)
    subprocess.run(['gifsicle', '-b', '--colors', '256', filepath])
