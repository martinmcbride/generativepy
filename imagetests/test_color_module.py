import unittest

from generativepy.geometry import Transform, Square

from generativepy.color import Color, ArtisticColorScheme, DarkColorScheme
from generativepy.drawing import make_image, setup

from image_test_helper import run_image_test

"""
Test each function of the color module
"""


class TestDrawingModule(unittest.TestCase):

    def test_basic_colors(self):
        """
        Test basic colors using pycairo set_source_* functions.
        """

        def draw(ctx, width, height, frame_no, frame_count):
            # Set the background to white, using the paint function.
            # Color(1) creates a grey value of 1 (ie white)
            # A Color object behaves like a 4-tuple (r, g, b, a), therefore *Color unpacks a colour into the
            # r, g, b, a values that set_source_rgba() requires.
            ctx.set_source_rgba(*Color(1))
            ctx.paint()

            # Set the colour to rgb(0.5, 0, 0), dark red. The alpha channel is automatically set to 1.
            # Even though we have set an rgb colour, the Color object still internally holds r, g, b, a so the
            # Color object still unpacks into 4 elements.
            ctx.set_source_rgba(*Color(0.5, 0, 0))
            ctx.rectangle(50, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color(0, 0, 0.5))
            ctx.rectangle(200, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color(0.8, 0.8, 0))
            ctx.rectangle(350, 50, 100, 100)
            ctx.fill()

            # Color(0.5).rgb creates a mid grey colour, then extracts its rgb property (0.5, 0.5, 0.5)
            # When we unpack this we get 3 parameters, which is what set_source_rgb requires.
            # We could have done:
            #
            #     ctx.set_source_rgba(*Color(0.5))
            #
            # This is just an example of how to retrieve 3 colour values if you need to
            ctx.set_source_rgb(*Color(0.5).rgb)
            ctx.rectangle(50, 200, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color(0.25))
            ctx.rectangle(200, 200, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color(0.8, 0.8, 0))
            ctx.rectangle(330, 180, 100, 100)
            ctx.fill()

            # Here we create a rectangle with a colour Color(1, 0, 1, 0.4).
            # That is magenta with a 0.4 alpha value (40% opacity, ie 60% transparent).
            # This overlaps the previous rectangle, and you can see the background through it.
            ctx.set_source_rgba(*Color(1, 0, 1, 0.4))
            ctx.rectangle(370, 220, 100, 100)
            ctx.fill()

        def creator(file):
            make_image(file, draw, 500, 350, channels=3)

        self.assertTrue(run_image_test('test_basic_colors.png', creator))

    def test_rgb_color_panels(self):
        """
        Create RGB colour panels
        """

        def draw(ctx, width, height, frame_no, frame_count):
            ctx.set_source_rgba(*Color(1))
            ctx.paint()

            for i in range(200):
                for j in range(200):
                    ctx.set_source_rgba(*Color(i / 200, j / 200, 0))
                    ctx.rectangle(i + 50, j + 50, 1, 1)
                    ctx.fill()

            for i in range(200):
                for j in range(200):
                    ctx.set_source_rgba(*Color(i / 200, 0, j / 200))
                    ctx.rectangle(i + 50, j + 300, 1, 1)
                    ctx.fill()

            for i in range(200):
                for j in range(200):
                    ctx.set_source_rgba(*Color(0, i / 200, j / 200))
                    ctx.rectangle(i + 50, j + 550, 1, 1)
                    ctx.fill()

        def creator(file):
            make_image(file, draw, 300, 800, channels=3)

        self.assertTrue(run_image_test('test_rgb_color_panels.png', creator))

    def test_hsl_colors(self):
        """
        Create HSL colours
        """

        def draw(ctx, width, height, frame_no, frame_count):
            ctx.set_source_rgba(*Color(1))
            ctx.paint()

            # We use Color.of_hsl() to create an HSL colour.
            # A hue of 0 gives pure red. We then set the saturation ot 0.5, which greys the colour
            # out a little, and lightness to 0.5 which creates a slightly dark red.
            ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5))
            ctx.rectangle(50, 50, 100, 100)
            ctx.fill()

            # Same as before, but a hue of 0.33 gives the equivalent green colour
            ctx.set_source_rgba(*Color.of_hsl(0.33, 0.5, 0.5))
            ctx.rectangle(200, 50, 100, 100)
            ctx.fill()

            # Same as before, but a hue of 0.66 gives the equivalent blue colour
            ctx.set_source_rgba(*Color.of_hsl(0.66, 0.5, 0.5))
            ctx.rectangle(350, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color.of_hsl(0, 0.25, 0.5))
            ctx.rectangle(50, 200, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.25))
            ctx.rectangle(200, 200, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color.of_hsl(0, 0.5, 0.5))
            ctx.rectangle(330, 180, 100, 100)
            ctx.fill()

            # Here we create a rectangle with a colour Color.of_hsla(0.5, 0.5, 0.5, 0.3).
            # That is blue-green with a 0.3 alpha value (30% opacity, ie 70% transparent).
            # This overlaps the previous rectangle, and you can see the background through it.
            ctx.set_source_rgba(*Color.of_hsla(0.5, 0.5, 0.5, 0.3))
            ctx.rectangle(370, 220, 100, 100)
            ctx.fill()

        def creator(file):
            make_image(file, draw, 500, 350, channels=3)

        self.assertTrue(run_image_test('test_hsl_colors.png', creator))

    def test_hsl_color_bars(self):
        """
        Create HSL colour bars
        """

        def draw(ctx, width, height, frame_no, frame_count):
            ctx.set_source_rgba(*Color(0))
            ctx.paint()

            # Vary hue, with s = 1, l = 0.5.
            # The hue is the position on the colour circle:
            #  - hue 0 is pure red
            #  - as hue increases the colour moves through yellow towards green
            #  - hue 0.33 is pure green
            #  - as hue increases the colour moves through cyan towards blue
            #  - hue 0.66 is pure blue
            #  - as hue increases the colour moves through magenta towards red
            #  - as the hue approaches 1, the colour goes back to pure red.
            # This is a circular parameter, th eci#ycle starts again at 1
            for i in range(200):
                ctx.set_source_rgba(*Color.of_hsl(i / 200, 1, 0.5))
                ctx.rectangle(2 * i + 100, 100, 2, 100)
                ctx.fill()

            # Vary saturation, with h = 0.33 (green), l = 0.5.
            # With saturation 1, the colour is pure (fully saturated).
            # Reducing the saturation makes the colour more "grey".
            # When the saturation is 0, the colour is totally grey. All hues look identical ar zero saturation,
            # they all become the same grey (the shade og grey depends on the lightness value)
            for i in range(200):
                ctx.set_source_rgba(*Color.of_hsl(0.33, i / 200, 0.5))
                ctx.rectangle(2 * i + 100, 300, 2, 100)
                ctx.fill()

            # Vary lightness, with h = 0.33 (green), s = 1.
            # Changing the lightness creates lighter or darker versions of the same colour,
            # rather like looking at the same object in a brighter or darker room.
            # When lightness is 0, all colours are black. When lightness is 1, all colours are white.
            for i in range(200):
                ctx.set_source_rgba(*Color.of_hsl(0.33, 1, i / 200))
                ctx.rectangle(2 * i + 100, 500, 2, 100)
                ctx.fill()

        def creator(file):
            make_image(file, draw, 600, 700, channels=3)

        self.assertTrue(run_image_test('test_hsl_color_bars.png', creator))

    def test_css_colors(self):
        """
        Create css colours
        """

        def draw(ctx, width, height, frame_no, frame_count):
            # Set the background to 'white', using the paint function.
            # Color('white') creates a colour with r, g, and b set to 1. Since s#no alpha is specified, alpha is
            # set to 1 by default.
            # A Color object behaves like a 4-tuple (r, g, b, a), therefore *Color unpacks a colour into the
            # r, g, b, a values that set_source_rgba() requires.
            ctx.set_source_rgba(*Color('white'))
            ctx.paint()

            ctx.set_source_rgba(*Color('salmon'))
            ctx.rectangle(50, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color('firebrick'))
            ctx.rectangle(200, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color('fuchsia'))
            ctx.rectangle(350, 50, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color('deepskyblue'))
            ctx.rectangle(50, 200, 100, 100)
            ctx.fill()

            ctx.set_source_rgba(*Color('hotpink'))
            ctx.rectangle(200, 200, 100, 100)
            ctx.fill()

            # *Color('lawngreen').rgb gets the rgb values of the 'lawngreen colour.
            # When we unpack this we get 3 parameters, which is what set_source_rgb requires.
            # We could have done:
            #
            #     ctx.set_source_rgba(*Color('lawngreen))
            #
            # This is just an example of how to retrieve 3 colour values if you need to
            ctx.set_source_rgb(*Color('lawngreen').rgb)
            ctx.rectangle(330, 180, 100, 100)
            ctx.fill()

            # Here we create a rectangle with a colour Color('navy', 0.4).
            # That is 'navy' with a 0.4 alpha value (40% opacity, ie 60% transparent).
            # This overlaps the previous rectangle, and you can see the background through it.
            ctx.set_source_rgba(*Color('navy', 0.4))
            ctx.rectangle(370, 220, 100, 100)
            ctx.fill()

        def creator(file):
            make_image(file, draw, 500, 350, channels=3)

        self.assertTrue(run_image_test('test_css_colors.png', creator))


    def test_light_dark_colors(self):
        """
        Create light and dark properties
        """

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            colors = [Color(0.5, 0, 0),  # red
                      Color(0, 0.5, 0),  # green
                      Color(0, 0, 0.5),  #blue
                      Color(0, 0.5, 0.5),  # cyan
                      Color(0.5, 0, 0.5),  # magenta
                      Color(0.5, 0.5, 0),  # yellow
                      Color(1, 1, 1),  # white
                      Color(0.5, 0.5, 0.5),  # grey
                      ]

            Transform(ctx).translate(50, 50)

            for i, color in enumerate(colors):
                Square(ctx).of_corner_size((i*50, 0), 50).fill(color.dark3)
                Square(ctx).of_corner_size((i*50, 50), 50).fill(color.dark2)
                Square(ctx).of_corner_size((i*50, 100), 50).fill(color.dark1)
                Square(ctx).of_corner_size((i*50, 150), 50).fill(color)
                Square(ctx).of_corner_size((i*50, 200), 50).fill(color.light1)
                Square(ctx).of_corner_size((i*50, 250), 50).fill(color.light2)
                Square(ctx).of_corner_size((i*50, 300), 50).fill(color.light3)

        def creator(file):
            make_image(file, draw, 500, 450, channels=3)

        self.assertTrue(run_image_test('test_light_dark_colors.png', creator))

    def test_artistic_color_scheme(self):
        """
        Create light and dark properties
        """

        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(1))

            cs = ArtisticColorScheme()

            colors = [cs.RED,
                      cs.BLUE,
                      cs.GREEN,
                      cs.YELLOW,
                      cs.MAGENTA,
                      cs.CYAN,
                      cs.ORANGE,
                      cs.STEEL,
                      cs.CREAM,
                      cs.LIME,
                      cs.BLACK,
                      cs.GREY,
                      cs.WHITE,
                      ]

            Transform(ctx).translate(50, 50)

            for i, color in enumerate(colors):
                Square(ctx).of_corner_size((i*50, 0), 50).fill(color.dark3)
                Square(ctx).of_corner_size((i*50, 50), 50).fill(color.dark2)
                Square(ctx).of_corner_size((i*50, 100), 50).fill(color.dark1)
                Square(ctx).of_corner_size((i*50, 150), 50).fill(color)
                Square(ctx).of_corner_size((i*50, 200), 50).fill(color.light1)
                Square(ctx).of_corner_size((i*50, 250), 50).fill(color.light2)
                Square(ctx).of_corner_size((i*50, 300), 50).fill(color.light3)

        def creator(file):
            make_image(file, draw, 750, 450, channels=3)

        self.assertTrue(run_image_test('test_artistic_color_scheme.png', creator))


    def test_dark_color_scheme(self):
        """
        Create light and dark properties
        """

        def draw(ctx, width, height, frame_no, frame_count):
            cs = DarkColorScheme()
            setup(ctx, width, height, background=cs.BACKGROUND)

            colors = [cs.RED,
                      cs.GREEN,
                      cs.BLUE,
                      cs.WHITE,
                      cs.GREY,
                      cs.BLACK,
                      cs.YELLOW,
                      cs.CYAN,
                      cs.MAGENTA,
                      cs.ORANGE,
                      cs.BACKGROUND,
                      ]

            Transform(ctx).translate(50, 50)

            for i, color in enumerate(colors):
                Square(ctx).of_corner_size((i*50, 0), 50).fill(color.dark3)
                Square(ctx).of_corner_size((i*50, 50), 50).fill(color.dark2)
                Square(ctx).of_corner_size((i*50, 100), 50).fill(color.dark1)
                Square(ctx).of_corner_size((i*50, 150), 50).fill(color)
                Square(ctx).of_corner_size((i*50, 200), 50).fill(color.light1)
                Square(ctx).of_corner_size((i*50, 250), 50).fill(color.light2)
                Square(ctx).of_corner_size((i*50, 300), 50).fill(color.light3)

        def creator(file):
            make_image(file, draw, 650, 450, channels=3)

        self.assertTrue(run_image_test('test_dark_color_scheme.png', creator))


