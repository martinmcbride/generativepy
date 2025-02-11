# Author:  Martin McBride
# Created: 2020-09-05
# Copyright (C) 2020, Martin McBride
# License: MIT
"""
The bitmap module provides the ability to paint bitmap images and save them as either PNG images or frames.

The module is based on the popular [PIL Python imaging library](/python-libraries/pillow/). This provides many
functions for manipulating bitmap images, such as colour manipulation, filters, enhancement, morphing, colour channel
operations, and pixel access. It also provides drawing operations (rectangles, ellipses, text etc), but these are not as
powerful as the vector methods available via Pycairo in the `generativepy.drawing` module.

generativepy actually uses the Pillow library, which is a fork of PIL. That is because Pillow is actively maintained
whereas PIL is not. The Pillow library is compatible, and is still imported using the name PIL. We will refer to is as
PIL in the documentation.
"""
from PIL import Image
import numpy as np

class Scaler:
    """
    A PIL Image object always works in pixels. Unlike a Pycairo context used by `make_image` and similar functions, Image
    has no concept of a user space.

    However, it is sometimes useful to be able to calculate values in a user space and convert them to image pixels (device
    space), or vice versa.

    The `Scaler` class provides this functionality. You can create a scaler object with the dimensions of the image and the
    required user space. The scaler object can then be used to convert coordinates from one space to another.
    """
    def __init__(self, pixel_width, pixel_height, width=None, height=None, startx=0, starty=0):
        """
        The `Scaler` object is created using the image size in device space (`pixel_width`, `pixel_height`), and the
        user space size and origin (`width`, `height`, `startx`, `starty`). It can be used convert an (x, y) point
        between device space and user space.


        Args:
            pixel_width: int - The width of the image in pixels. Use the value passed into `paint`.
            pixel_height: int - The height of the image in pixels. Use the value passed into `paint`.
            width: number - The required image width in user coordinates. Default is `pixel_width`.
            height: number - The required image height in user coordinates. Default is `pixel_height`.
            startx: number - The user space x coordinate of the device space origin. Default is 0.
            starty: number - The use rspace y coordinate of the device space origin. Default is 0.

        Returns:
            A `Scaler` object
        """

        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        if not height and not width:
            self.width = pixel_width
            self.height = pixel_height
        elif not height:
            self.height = self.width * pixel_height / pixel_width
        elif not width:
            self.width = self.height * pixel_width / pixel_height

    def device_to_user(self, device_x, device_y):
        """
        Converts a device coordinate to user space.

        Args:
            device_x: number - the x coordinate in device space.
            device_y: number - the y coordinate in device space.

        Returns:
            float (x, y), a tuple of the equivalent coordinates in user space.
        """
        user_x = device_x * self.width / self.pixel_width + self.startx
        user_y = device_y * self.height / self.pixel_height + self.starty
        return user_x, user_y

    def user_to_device(self, user_x, user_y):
        """
        Converts a user coordinate to device space.

        Args:
            user_x: number - the x coordinate in user space.
            user_y: number - the y coordinate in user space.

        Returns:
            float (x, y), a tuple of the equivalent coordinates in device space.
        """
        device_x = int((user_x - self.startx) * self.pixel_width / self.width)
        device_y = int((user_y - self.starty) * self.pixel_height / self.height)
        return device_x, device_y

def get_mode(channels):
    """
    Convert the number of channels into a PIL mode string.

    Args:
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.

    Returns:
        Returns a string:
        * 'L' if channels is 1.
        * 'RGBA' if channels is 4.
        * 'RGB' in all other cases.

    """
    if channels == 1:
        mode = 'L'
    elif channels == 4:
        mode = 'RGBA'
    else:
        mode = 'RGB'
    return mode

def get_background(channels):
    """
    `channels` is an int that specifies a colour space:

    * 1 - monochrome.
    * 3 - RGB
    * 4 - RGBA

    The result can be passed as an argument to the `Color` construtor to craete a suitable colour for a white
    background.

    For RGBA images, the background is set to transparent white.

    Args:
        channels: int - Number of colour channels in the image.

    Returns:
        A color specifier for white in the colour space specified by `channels`.
    **Usage**
    """
    if channels == 1:
        color = 'white'
    elif channels == 4:
        color = (255, 255, 255, 0)
    else:
        color = 'white'
    return color

def make_bitmap(outfile, paint, pixel_width, pixel_height, channels=3):
    """
    Used to create a single PNG image.

    `make_bitmap` creates a PIL Image object, then calls the user supplied `paint` function to fill the image. It then
    stores the image as a PNG file.

    The paint function must have the signature described for `example_paint_function`.

    Args:
        outfile: str - The path and filename for the output PNG file. The '.png' extension is optional, it will be added
                    if it isn't present.
        paint: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
    paint(image, pixel_width, pixel_height, 0, 1)
    image.save(outfile + '.png')

def make_bitmaps(outfile, paint, pixel_width, pixel_height, count, channels=3):
    """
    Used to create a sequence of PNG images. These can be combined into an animated GIF or video. This is similar to
    `make_bitmap` except it creates `count` files instead of just one.

    `make_bitmaps` creates a PIL Image object, then calls the user supplied `paint` function to fill the
    image. It repeats this process `count` times to create a sequence of image files.

    The image files are stored in numbered files. For example if `outfile` is "myfolder/myname.png" the files
    will be saved as "myfolder/myname00000000.png", "myfolder/myname00000001.png" and so on.

    The paint function must have the signature described for `example_paint_function`. Each time the paint function is
    called, `fn` will contain the frame number - 0, 1 etc

    Args:
        outfile: str - The path and filename template for the output PNG file. The '.png' extension is optional, it
                    will be added if it isn't present.
        paint: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        count: int - the number of images to create
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.
    """
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    for i in range(count):
        image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
        paint(image, pixel_width, pixel_height, i, count)
        image.save(outfile + str(i).zfill(8) + '.png')

def make_bitmap_frame(paint, pixel_width, pixel_height, channels=3):
    """
    Used to create a single image as a frame. A frame is a NumPy array with shape (pixel_height, pixel_width, channels).

    `make_bitmap_frame` creates a PIL Image object, then calls the user supplied `paint` function to fill the image. The
    image is returned as a NumPy frame.

    The paint function must have the signature described for `example_paint_function`.

    Args:
        paint: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.

    Returns:
        A frame.
    """
    image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
    paint(image, pixel_width, pixel_height, 0, 1)
    frame = np.copy(np.asarray(image))
    return frame

def make_bitmap_frames(paint, pixel_width, pixel_height, count, channels=3):
    """
    Used to create a sequence of frames. These can be combined into an animated GIF or video. This is similar to
    `make_bitmap_frame` except it creates `count` frames instead of just one.

    `make_bitmaps` creates a PIL Image object, then calls the user supplied `paint` function to fill the
    image. It repeats this process `count` times to create a sequence of frames.

    The function returns a lazy iterator. When this iterator is evaluated, the image frames are created on demand.

    The paint function must have the signature described for `example_paint_function`. Each time the paint function is
    called, `fn` will contain the frame number - 0, 1 etc

    Args:
        paint: function - A drawing function object, see below.
        pixel_width: int - The width of the image that will be created, in pixels.
        pixel_height: int - The height of the image that will be created, in pixels.
        count: int - the number of images to create
        channels: int - The number of colour channels. 1 for greyscale, 3 for RGB, 4 for RGBA.

    Returns:
        An iterator returning a sequence of frames.
    """
    for i in range(count):
        image = Image.new(get_mode(channels), (pixel_width, pixel_height), get_background(channels))
        paint(image, pixel_width, pixel_height, i, count)
        frame = np.copy(np.asarray(image))
        yield frame

def example_paint_function(image, pixel_width, pixel_height, frame_no, frame_count):
    """
    This is an example paint function. It is a dummy function used to document the required parameters.

    Args:
        image: PIL Image object - A drawing function object, see below.
        pixel_width: int - The width of the image in pixels.
        pixel_height: int - The height of the image in pixels.
        frame_no: int - the number of the current frame. For single images this will always be 0. For animations this
                        paint function will be called `frame_count` times (once for each frame) with `frame_no` incrementing
                        by 1 each time (ie it counts from 0 to `frame_count` - 1.
        frame_count: int - The total number of frames being created.For single images this will always be 0. For animations
                           this will be set to the total number of frames in the animation.
    """
    pass
