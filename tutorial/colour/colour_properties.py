# Author:  Martin McBride
# Created: 2021-04-19
# Copyright (C) 2021, Martin McBride
# License: MIT

from generativepy.color import Color

# Create a colour and print its properties

color = Color(1.0, 0.5, 0.0)

print(color.r)
print(color.g)
print(color.b)
print(color.a)

print(color.h)
print(color.s)
print(color.l)

print(color.as_rgbstr())
print(color.as_rgb_bytes())
print(color.as_rgba_bytes())
