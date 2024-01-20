# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT
"""
generativepy uses `Color` objects to represent colours.

Colours are stored as 4 values representing the red, green, blue and transparency (`rgba`). Each value has a range of 0.0 to 1.0, that represents the amount of that colour that is present:

* An `r` value of 0.0 means that colour contains no red.
* An `r` value of 1.0 means that colour contains the full intensity red.
* An `r` value of 0.25 means that colour contains a 25% of full intensity red.
* Similar for `b` and `g`, allowing any colour can be created using the `r`, `g`, `b` values.

For the alpha value, `a`:

* An `a` value of 0.0 means that colour is fully transparent (ie it can't be seen at all).
* An `a` value of 1.0 means that colour is fully opaque. It will completely hide anything behind it.
* An `a` value of 0.25 means that colour is partially transparent. It will partly hide anything behind it, creating a colour that is 75% of the background colour mixed with 25% of the foreground colour.
* The way foreground and background colours mix can be changed using Pycairo compositing operators if you wish.

`Color` can be used to represent various types of colour, but all are stored internally as `rgba` values (see the constructor section below for more details).

`Color` objects are immutable - you cannot change a `Color` object once it has been created. However there are various *factory methods* available for creating new colours that are based on an existing colour (for example you can create a new colour that is 20% more red, or 50% less saturated, based on an existing colour).

`Color` objects behave as immutable sequences (similar to tuples) so you can index, unpack, and loop over a `Color`.

The `color` module also contains:

* The `make_colormap` function that can be used to create a color map.
* Several reusable colour schemes.
"""

import colorsys
import itertools

cssColors = {
    "indianred":(205,92,92),
    "lightcoral":(240,128,128),
    "salmon":(250,128,114),
    "darksalmon":(233,150,122),
    "lightsalmon":(255,160,122),
    "crimson":(220,20,60),
    "red":(255,0,0),
    "firebrick":(178,34,34),
    "darkred":(139,0,0),
    "pink":(255,192,203),
    "lightpink":(255,182,193),
    "hotpink":(255,105,180),
    "deeppink":(255,20,147),
    "mediumvioletred":(199,21,133),
    "palevioletred":(219,112,147),
    "coral":(255,127,80),
    "tomato":(255,99,71),
    "orangered":(255,69,0),
    "darkorange":(255,140,0),
    "orange":(255,165,0),
    "gold":(255,215,0),
    "yellow":(255,255,0),
    "lightyellow":(255,255,224),
    "lemonchiffon":(255,250,205),
    "lightgoldenrodyellow":(250,250,210),
    "papayawhip":(255,239,213),
    "moccasin":(255,228,181),
    "peachpuff":(255,218,185),
    "palegoldenrod":(238,232,170),
    "khaki":(240,230,140),
    "darkkhaki":(189,183,107),
    "lavender":(230,230,250),
    "thistle":(216,191,216),
    "plum":(221,160,221),
    "violet":(238,130,238),
    "orchid":(218,112,214),
    "fuchsia":(255,0,255),
    "magenta":(255,0,255),
    "mediumorchid":(186,85,211),
    "mediumpurple":(147,112,219),
    "blueviolet":(138,43,226),
    "darkviolet":(148,0,211),
    "darkorchid":(153,50,204),
    "darkmagenta":(139,0,139),
    "purple":(128,0,128),
    "rebeccapurple":(102,51,153),
    "indigo":(75,0,130),
    "mediumslateblue":(123,104,238),
    "slateblue":(106,90,205),
    "darkslateblue":(72,61,139),
    "greenyellow":(173,255,47),
    "chartreuse":(127,255,0),
    "lawngreen":(124,252,0),
    "lime":(0,255,0),
    "limegreen":(50,205,50),
    "palegreen":(152,251,152),
    "lightgreen":(144,238,144),
    "mediumspringgreen":(0,250,154),
    "springgreen":(0,255,127),
    "mediumseagreen":(60,179,113),
    "seagreen":(46,139,87),
    "forestgreen":(34,139,34),
    "green":(0,128,0),
    "darkgreen":(0,100,0),
    "yellowgreen":(154,205,50),
    "olivedrab":(107,142,35),
    "olive":(128,128,0),
    "darkolivegreen":(85,107,47),
    "mediumaquamarine":(102,205,170),
    "darkseagreen":(143,188,143),
    "lightseagreen":(32,178,170),
    "darkcyan":(0,139,139),
    "teal":(0,128,128),
    "aqua":(0,255,255),
    "cyan":(0,255,255),
    "lightcyan":(224,255,255),
    "paleturquoise":(175,238,238),
    "aquamarine":(127,255,212),
    "turquoise":(64,224,208),
    "mediumturquoise":(72,209,204),
    "darkturquoise":(0,206,209),
    "cadetblue":(95,158,160),
    "steelblue":(70,130,180),
    "lightsteelblue":(176,196,222),
    "powderblue":(176,224,230),
    "lightblue":(173,216,230),
    "skyblue":(135,206,235),
    "lightskyblue":(135,206,250),
    "deepskyblue":(0,191,255),
    "dodgerblue":(30,144,255),
    "cornflowerblue":(100,149,237),
    "royalblue":(65,105,225),
    "blue":(0,0,255),
    "mediumblue":(0,0,205),
    "darkblue":(0,0,139),
    "navy":(0,0,128),
    "midnightblue":(25,25,112),
    "cornsilk":(255,248,220),
    "blanchedalmond":(255,235,205),
    "bisque":(255,228,196),
    "navajowhite":(255,222,173),
    "wheat":(245,222,179),
    "burlywood":(222,184,135),
    "tan":(210,180,140),
    "rosybrown":(188,143,143),
    "sandybrown":(244,164,96),
    "goldenrod":(218,165,32),
    "darkgoldenrod":(184,134,11),
    "peru":(205,133,63),
    "chocolate":(210,105,30),
    "saddlebrown":(139,69,19),
    "sienna":(160,82,45),
    "brown":(165,42,42),
    "maroon":(128,0,0),
    "white":(255,255,255),
    "snow":(255,250,250),
    "honeydew":(240,255,240),
    "mintcream":(245,255,250),
    "azure":(240,255,255),
    "aliceblue":(240,248,255),
    "ghostwhite":(248,248,255),
    "whitesmoke":(245,245,245),
    "seashell":(255,245,238),
    "beige":(245,245,220),
    "oldlace":(253,245,230),
    "floralwhite":(255,250,240),
    "ivory":(255,255,240),
    "antiquewhite":(250,235,215),
    "linen":(250,240,230),
    "lavenderblush":(255,240,245),
    "mistyrose":(255,228,225),
    "gainsboro":(220,220,220),
    "lightgray":(211,211,211),
    "lightgrey":(211,211,211),
    "silver":(192,192,192),
    "darkgray":(169,169,169),
    "darkgrey":(169,169,169),
    "gray":(128,128,128),
    "grey":(128,128,128),
    "dimgray":(105,105,105),
    "dimgrey":(105,105,105),
    "lightslategray":(119,136,153),
    "lightslategrey":(119,136,153),
    "slategray":(112,128,144),
    "slategrey":(112,128,144),
    "darkslategray":(47,79,79),
    "darkslategrey":(47,79,79),
    "black":(0,0,0),
}

class Color():
    """
    `Color` holds an `rgba` colour object.

    All numerical input values are clamped in the range 0.0 to 1.0 (values less than 0.0 are replaced with 0.0, values greater than 1.0 are replaced with 1.0).
    """

    def __init__(self, *args):
        """
        A color object always contains four values, `r`, `g`, `b` and `a`. Each value can have a value between
        0.0 and 1.0. Out of range values are automatically clamped.

        RGB values represent he three colours, where 0 is no colour, 1 is full intensity colour.

        A is the alpha channel, where 0 is fully transparent and 1 is fully opaque.

        Options for initialisation parameters are:

        * `Color(k)` a grey color, value `k`.
        * `Color(k, a)` a transparent grey color, value `k`, alpha `a`.
        * `Color(r, g, b)` an RGB color.
        * `Color(r, g, b, a)` a transparent RGB color, alpha `a`.
        * `Color(name)` a CSS named color, where `name` is the colour name (case insensitive).
        * `Color(name, a)` a transparent CSS named color, alpha `a`.

        Color objects are immutable.

        There are also various static methods and properties for creating other colours.

        Args:
            args: various - See usage.

        Returns:
            A `Color` object.
        """

        if len(args) == 1:
            if args[0] in cssColors:
                self.color = tuple([x/255 for x in cssColors[args[0]]]) + (1,)
            else:
                g = Color.clamp(args[0])
                self.color = (g,)*3 + (1,)
        elif len(args) == 2:
            if args[0] in cssColors:
                self.color = tuple([x/255 for x in cssColors[args[0]]]) + (args[1],)
            else:
                g = Color.clamp(args[0])
                a = Color.clamp(args[1])
                self.color = (g,) * 3 + (a,)
        elif len(args) == 3:
            self.color = tuple([Color.clamp(x) for x in args]) + (1,)
        elif len(args) == 4:
            self.color = tuple([Color.clamp(x) for x in args])
        else:
            raise ValueError("Color takes 1, 2, 3 or 4 arguments")

    @staticmethod
    def of_hsl(h, s, l):
        """
        Static method to create an HSL colour.

        HSL colours are defined by 3 values:

        * The hue value controls the position of the colour on the colour wheel.
        * The saturation controls how pure the colour is. For a particular hue, reducing the saturation creates a greyed
        out version of the same colour.
        * The lightness controls how light the colour is. Varying the lightness creates a lighter or darker version of
        the same colour.

        HSL is very useful because it allows you to control colours more intuitively.

        Internally the colour is still represented as an `rgba` colour. The `h`, `s` and `l` values are converted to `rgb`,
        with the `a` value to 1.

        Args:
            h: number - Hue of colour.
            s: number - Saturation of colour.
            v: number - Value (lightness) of colour.

        Returns:
            A `Color` object.
        """
        h = Color.clamp(h)
        s = Color.clamp(s)
        l = Color.clamp(l)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(r, g, b)

    @staticmethod
    def of_hsla(h, s, l, a):
        """
        Static method to create a transparent HSL colour.

        Similar to `of_hsl` but provides alpha channel.

        Args:
            h: number - Hue of colour.
            s: number - Saturation of colour.
            v: number - Value (lightness) of colour.
            a: number - Alpha (transparency) of colour.

        Returns:
            A `Color` object.
        """
        h = Color.clamp(h)
        s = Color.clamp(s)
        l = Color.clamp(l)
        a = Color.clamp(a)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(r, g, b, a)

    @property
    def rgb(self):
        """
        Read-only property returns RGB values as a tuple of floats. Each value is in range 0.0 to 1.0.
        """
        return tuple(self.color[:3])

    @property
    def rgba(self):
        """
        Read-only property returns RGBA values as a tuple of floats. Each value is in range 0.0 to 1.0.
        """
        return tuple(self.color)

    @property
    def r(self):
        """
        Read-only property returns the red value of the colour as a float in range 0.0 to 1.0.
        """
        return self.color[0]

    def with_r(self, newval):
        """
        Read-only property returns a new `Color` object with its red value set to `newval`
        """
        newval = Color.clamp(newval)
        return Color(newval, self.color[1], self.color[2], self.color[3])

    def with_r_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its red value multiplied by `factor`
        """
        return Color(self.color[0]*factor, self.color[1], self.color[2], self.color[3])

    @property
    def g(self):
        """
        Read-only property returns green value of the colour as a float in range 0.0 to 1.0.
        """
        return self.color[1]

    def with_g(self, newval):
        """
        Read-only property returns a new `Color` object with its green value set to `newval`
        """
        newval = Color.clamp(newval)
        return Color(self.color[0], newval, self.color[2], self.color[3])

    def with_g_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its green value multiplied by `factor`
        """
        return Color(self.color[0], self.color[1]*factor, self.color[2], self.color[3])

    @property
    def b(self):
        """
        Read-only property returns blue value of the colour as a float in range 0.0 to 1.0.
        """
        return self.color[2]

    def with_b(self, newval):
        """
        Read-only property returns a new `Color` object with its blue value set to `newval`
        """
        newval = Color.clamp(newval)
        return Color(self.color[0], self.color[1], newval, self.color[3])

    def with_b_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its blue value multiplied by `factor`
        """
        return Color(self.color[0], self.color[1], self.color[2]*factor, self.color[3])

    @property
    def a(self):
        """
        Read-only property returns the alpha value of the colour as a float in range 0.0 to 1.0.
        """
        return self.color[3]

    def with_a(self, newval):
        """
        Read-only property returns a new `Color` object with its alpha value set to `newval`
        """
        newval = Color.clamp(newval)
        return Color(self.color[0], self.color[1], self.color[2], newval)

    def with_a_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its alpha value multiplied by `factor`
        """
        return Color(self.color[0], self.color[1], self.color[2], self.color[3]*factor)

    @property
    def h(self):
        """
        Read-only property returns the h value of the colour as a float in range 0.0 to 1.0.
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return h

    def with_h(self, newval):
        """
        Read-only property returns a new `Color` object with its h value set to `newval`
        """
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(newval, l, s)
        return Color(r, g, b, self.color[3])

    def with_h_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its h value multiplied by `factor`
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(Color.clamp(h*factor), l, s)
        return Color(r, g, b, self.color[3])

    @property
    def s(self):
        """
        Read-only property returns the s value of the colour as a float in range 0.0 to 1.0.
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return s

    def with_s(self, newval):
        """
        Read-only property returns a new `Color` object with its s value set to `newval`
        """
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, l, newval)
        return Color(r, g, b, self.color[3])

    def with_s_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its s value multiplied by `factor`
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, l, Color.clamp(s*factor))
        return Color(r, g, b, self.color[3])

    @property
    def l(self):
        """
        Read-only property returns the l value of the colour as a float in range 0.0 to 1.0.
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return l

    def with_l(self, newval):
        """
        Read-only property returns a new `Color` object with its l value set to `newval`
        """
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, newval, s)
        return Color(r, g, b, self.color[3])

    def with_l_factor(self, factor):
        """
        Read-only property returns a new `Color` object with its l value multiplied by `factor`
        """
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, Color.clamp(l*factor), s)
        return Color(r, g, b, self.color[3])

    @property
    def dark3(self):
        """
        Read-only property returns a new `Color` object that is a much darker version of the current colout.
        """
        return self.with_l_factor(0.3)

    @property
    def dark2(self):
        """
        Read-only property returns a new `Color` object that is a darker version of the current colout.
        """
        return self.with_l_factor(0.5)

    @property
    def dark1(self):
        """
        Read-only property returns a new `Color` object that is a slightly darker version of the current colout.
        """
        return self.with_l_factor(0.75)

    @property
    def light3(self):
        """
        Read-only property returns a new `Color` object that is a much lighter version of the current colout.
        """
        return self.with_l_factor(2.5)

    @property
    def light2(self):
        """
        Read-only property returns a new `Color` object that is a lighter version of the current colout.
        """
        return self.with_l_factor(1.9)

    @property
    def light1(self):
        """
        Read-only property returns a new `Color` object that is a slightly lighter version of the current colout.
        """
        return self.with_l_factor(1.4)

    def lerp(self, other, factor):
        """
        Creates a new `Color` object that is part way between the current colour and the `other` colour. `factor` controls
        the mixture, eg:

        * 0: Current colour
        * 0.2: 80% current + 20% other
        * 0.7: 30% current + 70% other
        * 1: Other colour

        Args:
            other: `Color` - the other colour to mix with the current colour.
            factor: number - the amount of the other colour to mix (see above).

        Returns:
            The new `Color`.
        """
        """
        """
        factor = Color.clamp(factor)
        col1 = self.rgba
        col2 = other.rgba
        col = [x*(1-factor) + y*factor for x, y in zip(col1, col2)]
        return Color(*col)

    def as_rgbstr(self):
        """
        Converts current colour into a string format.

        Returns:
            String of form rgb(255, 128, 0)
        """
        return 'rgb({}, {}, {})'.format(int(self.color[0] * 255),
                                        int(self.color[1] * 255),
                                        int(self.color[2] * 255))

    def as_rgb_bytes(self):
        """
        Converts current colour into a tuple.

        Returns:
            Tuple of form (255, 128, 0)
        """
        return (int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255))

    def as_rgba_bytes(self):
        """
        Converts current colour into a tuple including alpha.

        Returns:
            Tuple of form (255, 128, 0, 64)
        """
        return (int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255),
                int(self.color[3] * 255))

    @staticmethod
    def clamp(v):
        try:
            v = min(1, max(0, v)) #Clamp v between 0 and 1
        except Exception as e:
            raise ValueError('Numerical value required') from e
        return v

    def __str__(self):
        return 'rgba' + str(self.color)

    def __getitem__(self, i):
        if i < 4:
            return self.color[i]
        else:
            raise IndexError()


def make_colormap(length, colors, bands=None):
    """
    A colormap is a list of varying colors. It can be used to map a set of integers onto a list of colours.

    A colormap can be used to assign colour gradients, gradients with step changes, or discrete colours depending on how
    it is set up.

    Args:
        length: int - Total size of returned list.
        colors: list[Colors] - Colours for creating the map. The list must be at least 2 long.
        bands: list[number] - Relative size of each band. bands[i] gives the size of the band between color[i] and color[i+1].
                    len(bands) must be exactly 1 less than len(colors). If bands is None, equal bands will be used.

    Returns:
        A list of `Color` objects.
    """

    color_count = len(colors)

    # Check parameters
    if length <= 0:
        raise ValueError('length must be > 0')
    if color_count < 2:
        raise ValueError('colors list must have at least 2 elements')
    if not bands:
        bands = [1]*(color_count - 1)
    if color_count != len(bands) + 1:
        raise ValueError('colors list must be exactly 1 longer than bands list')


    band_total = sum(bands)
    band_breakpoints = [int(x*length/band_total) for x in itertools.accumulate(bands)]

    current_colour = 0
    band_index = 0
    colormap = [None]*length
    band_size = []
    for i in range(length):
        while band_breakpoints[current_colour] <= i:
            band_size.append(band_index)
            current_colour += 1
            band_index = 0
        colormap[i] = (current_colour, band_index)
        band_index += 1
    band_size.append(band_index)

    colormap = [colors[col].lerp(colors[col+1], band/(band_size[col]-1))
                for col, band in colormap ]

    return colormap

## Colour schemes

class ArtisticColorScheme:
    """
    An example colour scheme suitable for a white background,
    """

    def __init__(self):
        self._RED = Color(0.941, 0.234, 0.125)
        self._BLUE = Color(0.250, 0.336, 0.629)
        self._GREEN = Color(0.250, 0.629, 0.336)
        self._YELLOW = Color(0.840, 0.598, 0.133)
        self._MAGENTA = Color(0.840, 0.133, 0.598)
        self._ORANGE = Color("orangered")
        self._CYAN = Color(0.250, 0.629 , 0.629)
        self._STEEL = Color(0.770, 0.793, 0.887)
        self._CREAM = Color(0.934, 0.883, 0.727)
        self._LIME = Color(0.727, 0.934, 0.727)
        self._BLACK = Color(0.2)
        self._GREY = Color(0.4)
        self._WHITE = Color(1)

    @property
    def RED(self):
        return self._RED

    @property
    def BLUE(self):
        return self._BLUE

    @property
    def GREEN(self):
        return self._GREEN

    @property
    def YELLOW(self):
        return self._YELLOW

    @property
    def MAGENTA(self):
        return self._MAGENTA

    @property
    def ORANGE(self):
        return self._ORANGE

    @property
    def CYAN(self):
        return self._CYAN

    @property
    def STEEL(self):
        return self._STEEL

    @property
    def CREAM(self):
        return self._CREAM

    @property
    def LIME(self):
        return self._LIME

    @property
    def BLACK(self):
        return self._BLACK

    @property
    def GREY(self):
        return self._GREY

    @property
    def WHITE(self):
        return self._WHITE

class DarkColorScheme:
    """
    An example colour scheme suitable for a dark grey background, such as the `BACKGROUND` colour below.
    """

    def __init__(self):
        self._BACKGROUND = Color(0.2)
        self._RED = Color("firebrick")
        self._GREEN = Color("mediumseagreen")
        self._BLUE = Color("steelblue")
        self._WHITE = Color(0.8)
        self._GREY = Color(0.5)
        self._BLACK = Color(0)
        self._YELLOW = Color("darkkhaki")
        self._CYAN = Color("darkturquoise")
        self._MAGENTA = Color("orchid")
        self._ORANGE = Color("orangered")

    @property
    def BACKGROUND(self):
        return self._BACKGROUND

    @property
    def RED(self):
        return self._RED

    @property
    def GREEN(self):
        return self._GREEN

    @property
    def BLUE(self):
        return self._BLUE

    @property
    def WHITE(self):
        return self._WHITE

    @property
    def GREY(self):
        return self._GREY

    @property
    def BLACK(self):
        return self._BLACK

    @property
    def YELLOW(self):
        return self._YELLOW

    @property
    def CYAN(self):
        return self._CYAN

    @property
    def MAGENTA(self):
        return self._MAGENTA

    @property
    def ORANGE(self):
        return self._ORANGE
