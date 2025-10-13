# Author:  Martin McBride
# Created: 2025-10-13
# Copyright (C) 2025, Martin McBride
# License: MIT
"""
The matplotlib module uses the matplotlib library to create 3D plots
"""
import dataclasses
import math
from dataclasses import dataclass

from generativepy.color import Color
from matplotlib import pyplot, cm
import numpy as np
from matplotlib.ticker import LinearLocator



class Plot3dZofXY():

    def __init__(self, plt):
        """
        Args:
            plot: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.plt = plt
        self.function = lambda x, y: 0

    def of(self, function):
        self.function = function
        return self

    def render(self):
        fig, ax = self.plt.subplots(subplot_kw={"projection": "3d"})

        # Make data.
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = np.ones_like(X)
        Z = np.sin(np.sqrt(X * X + Y * Y))
        # for i, x in enumerate(X):
        #     for j, y in enumerate(Y):
        #         Z[i, j] = math.sqrt(x*x + y*y)

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=True)

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        ax.zaxis.set_major_formatter('{x:.02f}')

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)


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
    draw(pyplot, width, height, 0, 1)
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



