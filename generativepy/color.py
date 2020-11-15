# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT

import colorsys
import itertools

cssColors = {
"purple":(128,0,128),
"fuchsia":(255,0,255),
"lime":(0,255,0),
"teal":(0,128,128),
"aqua":(0,255,255),
"blue":(0,0,255),
"navy":(0,0,128),
"black":(0,0,0),
"gray":(128,128,128),
"silver":(192,192,192),
"white":(255,255,255),
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
    '''
    Holds a color value.

    Color is stored as a tuple (r, g, b, a), where each channel has a value between 0 and 1.

    Colour can be initialised with:
    - a grey value
    - a grey value + an alpha
    - r, g and b values (alpha defaults to 1)
    - r, g, b and a values
    - a CSS color name as a string (alpha defaults to 1)
    - a CSS color name as a string plus an alpha value (0 to 1)

    Color objects are immutable.

    get_rgb, get_rgba gets the colour values as a 3- or 4-tuple

    of_hsl, of_hsla creates a new Color from hsl values (color values are stored as RGB)

    get_r gets the red value (similar for b, g, a, h, s, l). h, s and l values are obtained by converting from rgb

    with_r creates a new Color from an existing colour by setting the r value (similar for b, g, a, h, s, l). For
    h, s, l values, the color is converted to hsl, modified, then converted back to rgb.

    with_r_factor creates a new Color from an existing colour by multiplying the r value by a factor. It is
    equivalent to with_r(get_r()*factor). Similar for b, g, a, h, s, l

    '''

    def __init__(self, *args):
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
        h = Color.clamp(h)
        s = Color.clamp(s)
        l = Color.clamp(l)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(r, g, b)

    @staticmethod
    def of_hsla(h, s, l, a):
        h = Color.clamp(h)
        s = Color.clamp(s)
        l = Color.clamp(l)
        a = Color.clamp(a)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(r, g, b, a)

    @property
    def rgb(self):
        return tuple(self.color[:3])

    @property
    def rgba(self):
        return tuple(self.color)

    @property
    def r(self):
        return self.color[0]

    def with_r(self, newval):
        newval = Color.clamp(newval)
        return Color(newval, self.color[1], self.color[2], self.color[3])

    def with_r_factor(self, factor):
        return Color(self.color[0]*factor, self.color[1], self.color[2], self.color[3])

    @property
    def g(self):
        return self.color[1]

    def with_g(self, newval):
        newval = Color.clamp(newval)
        return Color(self.color[0], newval, self.color[2], self.color[3])

    def with_g_factor(self, factor):
        return Color(self.color[0], self.color[1]*factor, self.color[2], self.color[3])

    @property
    def b(self):
        return self.color[2]

    def with_b(self, newval):
        newval = Color.clamp(newval)
        return Color(self.color[0], self.color[1], newval, self.color[3])

    def with_b_factor(self, factor):
        return Color(self.color[0], self.color[1], self.color[2]*factor, self.color[3])

    @property
    def a(self):
        return self.color[3]

    def with_a(self, newval):
        newval = Color.clamp(newval)
        return Color(self.color[0], self.color[1], self.color[2], newval)

    def with_a_factor(self, factor):
        return Color(self.color[0], self.color[1], self.color[2], self.color[3]*factor)

    @property
    def h(self):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return h

    def with_h(self, newval):
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(newval, l, s)
        return Color(r, g, b, self.color[3])

    def with_h_factor(self, factor):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(Color.clamp(h*factor), l, s)
        return Color(r, g, b, self.color[3])

    @property
    def s(self):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return s

    def with_s(self, newval):
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, l, newval)
        return Color(r, g, b, self.color[3])

    def with_s_factor(self, factor):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, l, Color.clamp(s*factor))
        return Color(r, g, b, self.color[3])

    @property
    def l(self):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        return l

    def with_l(self, newval):
        newval = Color.clamp(newval)
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, newval, s)
        return Color(r, g, b, self.color[3])

    def with_l_factor(self, factor):
        h, l, s = colorsys.rgb_to_hls(self.color[0], self.color[1], self.color[2])
        r, g, b = colorsys.hls_to_rgb(h, Color.clamp(l*factor), s)
        return Color(r, g, b, self.color[3])

    def lerp(self, other, factor):
        factor = Color.clamp(factor)
        col1 = self.rgba
        col2 = other.rgba
        col = [x*(1-factor) + y*factor for x, y in zip(col1, col2)]
        return Color(*col)

    def as_rgbstr(self):
        return 'rgb({}, {}, {})'.format(int(self.color[0] * 255),
                                       int(self.color[1] * 255),
                                       int(self.color[2] * 255))

    def as_rgb_bytes(self):
        return (int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255))

    def as_rgba_bytes(self):
        return (int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255),
                int(self.color[3] * 255))

    @staticmethod
    def clamp(v):
        try:
            v = min(1, max(0, v)) #Clamp v between 0 and 1
        except:
            raise ValueError('Numerical value required')
        return v

    def __str__(self):
        return 'rgba' + str(self.color)

    def __getitem__(self, i):
        if i < 4:
            return self.color[i]
        else:
            raise IndexError()


def make_colormap(length, colors, bands):
    '''
    Create a colormap, a list of varying colors.
    :param length: Total size of list
    :param colors: List of colors, must be at least 2 long.
    :param bands: Relative size of each band. bands[i] gives the size of teh band between color[i] and color[i+1].
                  len(bands) must be exactly 1 less than len(colors)
    :return:
    '''

    # Check parameters
    if length <= 0:
        raise ValueError('length must be > 0')
    if len(colors) < 2:
        raise ValueError('colors list must have at least 2 elements')
    if len(colors) != len(bands) + 1:
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

