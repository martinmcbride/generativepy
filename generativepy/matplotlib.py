# Author:  Martin McBride
# Created: 2025-10-13
# Copyright (C) 2025, Martin McBride
# License: MIT
"""
The matplotlib module uses the matplotlib library to create 3D plots
"""
from matplotlib import pyplot
import numpy as np

class Plot3dZofXY():

    def __init__(self, plt):
        """
        Args:
            plot: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.plt = plt

    def render(self):
        x = np.arange(-5, 5, 0.01)
        y = np.arange(-5, 5, 0.01)

        X, Y = np.meshgrid(x, y)

        Z = 1 - X*X - Y*Y

        fig, ax = self.plt.subplots(subplotkw={'projection': '3d'})
        im = ax.plotsurface(X, Y, Z, cmap='plasma')

        fig.colorbar(im, shrink=0.5, aspect=5, pad=0.07)

        ax.grid(False)

        ax.setxticks([])
        ax.setyticks([])
        ax.set_zticks([])



def make_mpl_image(outfile, draw, width, height, channels=3):
    """
    Creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the
    context. It then stores the image as a PNG file.

    The draw function must have the signature described for `example_draw_function`.

    Args:
        outfile: str - The path and filename for the output PNG file. The '.png' extension is optional, it will be added
                    if it isn't present.
        draw: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        channels: int - The number of colour channels, currently only supports 3. 3 for RGB.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    #draw(pyplot, width, height, 0, 1)
    fig, ax = pyplot.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    pyplot.savefig(outfile + '.png', bbox_inches='tight')


def example_mpl_draw_function(plt, pixel_width, pixel_height, frame_no, frame_count):
    """
    This is an example draw function for use with `make_mpl_image` and similar functions. It is a dummy function used to document the required parameters.

    Args:
        plt: matplotlib pyplot object
        pixel_width: int - The width of the image in pixels.
        pixel_height: int - The height of the image in pixels.
        frame_no: int - the number of the current frame. For single images this will always be 0. For animations this
                        paint function will be called `frame_count` times (once for each frame) with `frame_no` incrementing
                        by 1 each time (ie it counts from 0 to `frame_count` - 1.
        frame_count: int - The total number of frames being created.For single images this will always be 0. For animations
                           this will be set to the total number of frames in the animation.
    """
    pass



