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

import PIL.Image

from generativepy.color import Color
from matplotlib import pyplot, cm
import numpy as np
from matplotlib.ticker import LinearLocator

MPL_DPI = 80


class Plot3dZofXY():

    def __init__(self, plt, width, height):
        """
        Args:
            plot: Pycairo drawing context - The context to draw on.

        Returns:
            self
        """
        self.plt = plt
        self.width = width
        self.height = height
        self.function = lambda x, y: 0
        self.start = (-5, -5, -5)
        self.extent = (10, 10, 10)
        self.divisions = (1, 1, 1)
        self.precision = 100
        self.cmap = cm.plasma
        self.elev = 30
        self.azim = -60
        self.contour_plot = True

    def of(self, function):
        self.function = function
        return self

    def of_start(self, start):
        '''
        Sets the start value of the axes

        Args:
            start: (x, y, z) value of bottom left corner of axes

        Returns:
            self
        '''
        self.start = start
        return self

    def of_extent(self, extent):
        '''
        Sets the range of the axes

        Args:
            extent: (x, y, z) range of axes

        Returns:
            self
        '''
        self.extent = extent
        return self

    def with_divisions(self, divisions):
        '''
        Set divisions spacing

        Args:
            divisions: (x, y, z) spacing divisions in each direction

        Returns:
            self
        '''
        self.divisions = divisions
        return self

    def with_colormap(self, cmap):
        '''
        Set color map.

        Args:
            cmap: a color map. Can use standard ones provided in maplotlib library, cm.plasma etc

        Returns:
            self
        '''
        self.cmap = cmap
        return self

    def with_view_rot(self, elev, azim):
        '''
        Set view rotation.

        Args:
            elev: the elevation, in degrees
            elev: the azimuth, in degrees

        Returns:
            self
        '''
        self.elev = elev
        self.azim = azim
        return self

    def with_contour_plot(self, visible):
        '''
        Add a contour plot under main plat

        Args:
            visible: True to make contour plot visible

        Returns:
            self
        '''
        self.contour_plot = visible
        return self

    def get_ticks(self, start, extent, division):
        v = ((start + division)//division)*division
        ticks = [v]
        while v < (start + extent):
            v += division
            if v < (start + extent):
                ticks.append(v)
        return ticks

    def render(self):
        fig, ax = self.plt.subplots(subplot_kw={"projection": "3d"}, figsize=(self.width/MPL_DPI, self.height/MPL_DPI))

        # Make data.
        Xval = np.arange(self.start[0], self.extent[0] + self.start[0], self.extent[0]/self.precision)
        Yval = np.arange(self.start[1], self.extent[1] + self.start[1], self.extent[1]/self.precision)
        X, Y = np.meshgrid(Xval, Yval)
        Z = np.ones_like(X)
        for i, x in enumerate(Xval):
            for j, y in enumerate(Yval):
                Z[i, j] = self.function(x, y)

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=self.cmap, antialiased=True)

        # Customize the axes
        ax.set_xticks(self.get_ticks(self.start[0], self.extent[0], self.divisions[0]))
        ax.set_yticks(self.get_ticks(self.start[1], self.extent[1], self.divisions[1]))
        ax.set_zlim(self.start[2], self.extent[2] + self.start[2])
        # ax.zaxis.set_major_locator(LinearLocator(10))
        # # A StrMethodFormatter is used automatically
        # ax.zaxis.set_major_formatter('{x:.02f}')
        ax.set_zticks(self.get_ticks(self.start[2], self.extent[2], self.divisions[2]))

        ## Contour map
        if self.contour_plot:
            ax.contourf(X, Y, Z, zdir="z", cmap=self.cmap, offset=self.start[2])

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5, pad=0.07)

        # SEt view rotation
        self.plt.gca().azim = self.azim
        self.plt.gca().elev = self.elev

def resize_image(filepath, newsize):
    img1 = PIL.Image.open(filepath)
    oldsize = img1.size
    if oldsize[0]==newsize[0] and oldsize[1]==newsize[1]:
        return
    img2 = PIL.Image.new("RGB", newsize, (255, 255, 255))
    pos = (newsize[0] - oldsize[0])//2, (newsize[1] - oldsize[1])//2
    print(oldsize, newsize, pos)
    img2.paste(img1, pos)
    img2.save(filepath)

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
    draw(pyplot, int(width*0.95), int(height*0.95), 0, 1)
    pyplot.savefig(outfile + '.png', bbox_inches='tight', dpi=100)
    resize_image(outfile + '.png', (width, height))

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



