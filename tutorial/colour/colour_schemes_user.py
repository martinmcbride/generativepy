# Author:  Martin McBride
# Created: 2022-06-04
# Copyright (C) 2022, Martin McBride
# License: MIT

from generativepy.drawing import make_image, setup
from generativepy.color import Color, ArtisticColorScheme
from generativepy.geometry import Square

# Create a user defined colour scheme and use it

class UserColorScheme:
    def __init__(self):
        self._RED = Color(0.5, 0, 0.25)
        self._BLUE = Color(0, 0, 0.5)
        self._GREEN = Color(0, 0.5, 0.25)

    @property
    def RED(self):
        return self._RED

    @property
    def BLUE(self):
        return self._BLUE

    @property
    def GREEN(self):
        return self._GREEN


cs = UserColorScheme()

def draw_color_scheme_user(ctx, pixel_width, pixel_height, frame_no, frame_count):
    setup(ctx, pixel_width, pixel_height, background=Color("white"))

    # Fill a square with red
    Square(ctx).of_corner_size((50, 50), 200).fill(cs.RED)

    # Fill a square with a lighter version of RED, stroke with a darker version
    Square(ctx).of_corner_size((300, 50), 200).fill(cs.RED.light1).stroke(cs.RED.dark1, 10)


make_image("colour-scheme-user.png", draw_color_scheme_user, 600, 300)
