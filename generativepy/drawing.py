# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT
"""
The drawing module provides the ability to draw vector images and save them as either PNG images, SVG images, or frames.

The module is based on the Pycairo library. This provides many vector drawing methods.

However, it is often more convenient to use the `geometry` module of generativepy, which provides higher level versions
of most of the primitive drawing functions.
"""

import cairo
import generativepy.utils
import numpy as np

# Text align

# Centre text horizontally
CENTER = 0

# Centre text vertically
MIDDLE = 0

# Left align text
LEFT = 1

# Right align text
RIGHT = 2
TOP = 3
BOTTOM = 4
BASELINE = 5

# Fill rule
EVEN_ODD=0
WINDING=1

## Line cap/join
MITER = 0   # join
ROUND = 1   # join/cap
BEVEL = 2   # join
BUTT = 3    # cap
SQUARE = 4  # cap

## Line extension

SEGMENT = 0
RAY = 1
LINE = 2

## Font styles

FONT_WEIGHT_NORMAL = 0
FONT_WEIGHT_BOLD = 1

FONT_SLANT_NORMAL = 0
FONT_SLANT_ITALIC = 1
FONT_SLANT_OBLIQUE = 2


def setup(ctx, pixel_width, pixel_height, width=None, height=None, startx=0, starty=0, background=None, flip=False):
    """
    This function performs a scaling to set the drawing coordinates. This is optional, but in generative art you
    will often be using functions that work at a particular scale. It is very useful to be able to set your drawing
    coordinates to maths this, so you don't need to worry about scaling values when you draw.

    As a convenience it can also set the page background colour.

    Args:
        ctx:  Pycairo context - The drawing context.
        pixel_width: int  - Pycairo context. Use the value passed into the `draw` function.
        pixel_height: int  -  The device space height. Use the value passed into the `draw` function.
        width: number  - The user space width.
        height: number  -  The user space height.
        startx: number  - The x offset of the top left corner from the origin.
        starty: number  - The y offset of the top left corner from the origin.
        background: Color  - Color of the background.
        flip: bool  - If true, flips the page in the y direction, so the origin is at the bottom left, useful for
                    mathematical drawing.
    """

    if not height and not width:
        width = pixel_width
        height = pixel_height
    elif not height:
        height = width * pixel_height / pixel_width
    elif not width:
        width = height * pixel_width / pixel_height

    if flip:
        ctx.scale(1, -1)
        ctx.translate(0, -pixel_height)

    ctx.scale(pixel_width / width, pixel_height / height)
    ctx.translate(-startx, -starty)

    if background:
        ctx.set_source_rgba(*background)
        ctx.paint()



def make_image(outfile, draw, width, height, channels=3):
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
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    surface = cairo.ImageSurface(fmt, width, height)
    ctx = cairo.Context(surface)
    draw(ctx, width, height, 0, 1)
    surface.write_to_png(outfile + '.png')


def make_images(outfile, draw, width, height, count, channels=3):
    """
    Used to create a sequence of PNG images. These can be combined into an animated GIF or video. This is similar to
    `make_image` except it creates `count` files instead of just one.

    Creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the context.
    It repeats this process `count` times to create a sequence of image files.

    The image files are stored in numbered files. For example if `outfile` is "myfolder/myname.png" the files
    will be saved as "myfolder/myname00000000.png", "myfolder/myname00000001.png" and so on.

    The paint function must have the signature described for `example_draw_function`. Each time the draw function is
    called, `fn` will contain the frame number - 0, 1 etc

    Args:
        outfile: str - The path and filename template for the output PNG file. The '.png' extension is optional, it
                    will be added if it isn't present.
        draw: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        count: int - the number of images to create
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    for i in range(count):
        fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
        surface = cairo.ImageSurface(fmt, width, height)
        ctx = cairo.Context(surface)
        draw(ctx, width, height, i, count)
        surface.write_to_png(outfile + str(i).zfill(8) + '.png')


def make_image_frames(draw, width, height, count, channels=3):
    """
    Used to create a single image as a frame. A frame is a NumPy array with shape (pixel_height, pixel_width, channels).

    `make_image_frames` creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the context.
    It repeats this process `count` times to create a sequence of image frames.

    The function returns a lazy iterator. When this iterator is evaluated, the image frames are created on demand.

    The draw function must have the signature described for `example_draw_function`. Each time the paint function is
    called, `fn` will contain the frame number - 0, 1 etc

    Args:
        draw: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.

    Yields:
        A frame.
    """
    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    for i in range(count):
        surface = cairo.ImageSurface(fmt, width, height)
        ctx = cairo.Context(surface)
        draw(ctx, width, height, i, count)
        buf = surface.get_data()
        a = np.frombuffer(buf, np.uint8)
        a.shape = (height, width, 4)
        a = generativepy.utils.correct_pycairo_byte_order(a, channels)
        yield a

def make_image_frame(draw, width, height, channels=3):
    """
    Used to create a single image as a frame. A frame is a NumPy array with shape (pixel_height, pixel_width, channels).

    `make_image_frame` creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the
    context. The image is returned as a NumPy frame.

    The draw function must have the signature described for `example_draw_function`.

    Args:
        draw: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.

    Yields:
        A frame.
    """
    fmt = cairo.FORMAT_ARGB32 if channels==4 else cairo.FORMAT_RGB24
    surface = cairo.ImageSurface(fmt, width, height)
    ctx = cairo.Context(surface)
    draw(ctx, width, height, 0, 1)
    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (height, width, 4)
    if channels==3:
        a[:, :, [0, 1, 2]] = a[:, :, [2, 1, 0]]
    elif channels==4:
        a[:, :, [0, 1, 2, 3]] = a[:, :, [2, 1, 0, 3]]
    return a


def make_svg(outfile, draw, width, height):
    """
    Used to create a single SVG image. This function is similar to `make_image` except that it returns an SVG (vector
    image) instead of a PNG (bitmap image).

    `make_svg` creates a Pycairo drawing context object, then calls the user supplied `draw` function to draw on the
    context. It then stores the image as a PNG file.

    The draw function must have the signature described for `example_draw_function`.

    Args:
        outfile: str - The path and filename for the output SVG file. The '.svg' extension is optional, it will be added
                    if it isn't present.
        draw: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
    """
    if outfile.lower().endswith('.svg'):
        outfile = outfile[:-4]
    surface = cairo.SVGSurface(outfile + '.svg', width, height)
    ctx = cairo.Context(surface)
    draw(ctx, width, height, 0, 1)
    ctx.show_page()

def example_pycairo_draw_function(ctx, pixel_width, pixel_height, frame_no, frame_count):
    """
    This is an example draw function for use with `make_image` and similar functions. It is a dummy function used to document the required parameters.

    Args:
        ctx: PyCairo context object - The context object that the image will be drawn on.
        pixel_width: int - The width of the image in pixels.
        pixel_height: int - The height of the image in pixels.
        frame_no: int - the number of the current frame. For single images this will always be 0. For animations this
                        paint function will be called `frame_count` times (once for each frame) with `frame_no` incrementing
                        by 1 each time (ie it counts from 0 to `frame_count` - 1.
        frame_count: int - The total number of frames being created.For single images this will always be 0. For animations
                           this will be set to the total number of frames in the animation.
    """
    pass

