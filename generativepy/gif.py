# Author:  Martin McBride
# Created: 2020-09-10
# Copyright (C) 2020, Martin McBride
# License: MIT

import imageio
import subprocess

"""
This module creates an animated GIF from a sequence of frames.
"""

def save_animated_gif(filepath, frames, delay, loop=0):
    '''
    Save a set of frames as an animated GIF.
    Requires gifsicle to be installed

    Args:
        filepath: str - Output filepath.
        frames: iterator returning frames - sequence of frames.
        delay: number - Delay between frames in seconds (eg 0.2 for frame rate of 5 frames per second).
        loop: function - Easing function. Thus accepts a value that varies between 0 and 1.0.
    '''
    if not filepath.lower().endswith('.gif'):
        filepath += '.gif'
    images = list(frames)
    imageio.mimsave(filepath, images, duration=delay)
    subprocess.run(['gifsicle', '-b', '--colors', '256', '--optimize=3', filepath])
