import unittest
from generativepy.drawing import setup, make_image, BUTT, ROUND, BEVEL, FONT_WEIGHT_BOLD, FONT_SLANT_ITALIC
from image_test_helper import run_image_test
from generativepy.color import Color
from generativepy.geometry import Image, Text, Circle, circle, Bezier, Polygon, Square, square, Rectangle, \
    rectangle, Line, line, Ellipse, ellipse, tick, paratick, arrowhead, polygon, \
    angle_marker, Path, Triangle, triangle, Turtle, Transform, AngleMarker, \
    ParallelMarker, TickMarker, RegularPolygon
import math

"""
Test the geometry module.
"""


class TestGeometryImages(unittest.TestCase):

    def test_markers(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))
            red = Color('red')
            thickness = 3

            ## Draw lines with ticks and paraticks
            a = (50, 50)
            b = (50, 150)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            TickMarker(ctx).of_start_end(a, b).with_length(12).stroke(red, thickness)

            a = (100, 50)
            b = (150, 150)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            TickMarker(ctx).of_start_end(a, b).with_length(12).with_count(2).with_gap(6).stroke(red, thickness)

            a = (250, 50)
            b = (200, 150)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            TickMarker(ctx).of_start_end(a, b).with_length(12).with_count(3).with_gap(6).stroke(red, thickness)

            a = (350, 50)
            b = (350, 150)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            ParallelMarker(ctx).of_start_end(a, b).with_length(12).stroke(red, thickness)

            a = (400, 50)
            b = (450, 150)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            ParallelMarker(ctx).of_start_end(a, b).with_length(12).with_count(2).with_gap(6).stroke(red, thickness)

            a = (550, 150)
            b = (500, 50)
            Line(ctx).of_start_end(a, b).stroke(red, thickness)
            ParallelMarker(ctx).of_start_end(a, b).with_length(12).with_count(3).with_gap(6).stroke(red, thickness)


            ## Draw lines with angles
            a = (50, 250)
            b = (50, 450)
            c = (150, 450)
            Polygon(ctx).of_points((a, b, c)).open().stroke(red, thickness)
            AngleMarker(ctx).of_points(a, b, c).with_radius(24).with_gap(6).as_right_angle().stroke(red, thickness)

            a = (250, 250)
            b = (200, 450)
            c = (300, 450)
            Polygon(ctx).of_points((a, b, c)).open().stroke(red, thickness)
            AngleMarker(ctx).of_points(a, b, c).with_count(3).with_radius(24).with_gap(6).stroke(red, thickness)

            a = (300, 250)
            b = (400, 300)
            c = (500, 300)
            Polygon(ctx).of_points((a, b, c)).open().stroke(red, thickness)
            AngleMarker(ctx).of_points(c, b, a).with_radius(24).with_gap(6).stroke(red, thickness)

            a = (300, 350)
            b = (400, 400)
            c = (500, 400)
            Polygon(ctx).of_points((a, b, c)).open().stroke(red, thickness)
            AngleMarker(ctx).of_points(a, b, c).with_count(2).with_radius(24).with_gap(6).stroke(red, thickness)


        def creator(file):
            make_image(file, draw, 600, 500)

        self.assertTrue(run_image_test('test_markers.png', creator))


    def test_old_markers(self):
        # Deprecated marker functions
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))

            ctx.set_source_rgba(*Color(0, 0, 0.5))
            ctx.set_line_width(3)

            ## Draw lines with ticks, paraticks and arrowheads
            a = (50, 50)
            b = (50, 150)
            line(ctx, a, b)
            ctx.stroke()
            tick(ctx, a, b, length=12, gap=6)
            ctx.stroke()
            arrowhead(ctx, a, b, length=24)
            ctx.stroke()

            a = (100, 50)
            b = (150, 150)
            line(ctx, a, b)
            ctx.stroke()
            tick(ctx, a, b, 2, length=12, gap=6)
            ctx.stroke()

            a = (250, 50)
            b = (200, 150)
            line(ctx, a, b)
            ctx.stroke()
            tick(ctx, a, b, 3, length=12, gap=6)
            ctx.stroke()

            a = (350, 50)
            b = (350, 150)
            line(ctx, a, b)
            ctx.stroke()
            paratick(ctx, a, b, length=12, gap=6)
            ctx.stroke()

            a = (400, 50)
            b = (450, 150)
            line(ctx, a, b)
            ctx.stroke()
            paratick(ctx, a, b, 2, length=12, gap=6)
            ctx.stroke()

            a = (550, 150)
            b = (500, 50)
            line(ctx, a, b)
            ctx.stroke()
            paratick(ctx, a, b, 3, length=12, gap=6)
            ctx.stroke()

            ## Draw lines with angles
            a = (50, 250)
            b = (50, 450)
            c = (150, 450)
            polygon(ctx, (a, b, c), closed=False)
            ctx.stroke()
            angle_marker(ctx, a, b, c, radius=24, gap=6, right_angle=True)
            ctx.stroke()

            a = (250, 250)
            b = (200, 450)
            c = (300, 450)
            polygon(ctx, (a, b, c), closed=False)
            ctx.stroke()
            angle_marker(ctx, a, b, c, 3, radius=24, gap=6)
            ctx.stroke()

            a = (300, 250)
            b = (400, 300)
            c = (500, 300)
            polygon(ctx, (a, b, c), closed=False)
            ctx.stroke()
            angle_marker(ctx, c, b, a, radius=24, gap=6)
            ctx.stroke()

            a = (300, 350)
            b = (400, 400)
            c = (500, 400)
            polygon(ctx, (a, b, c), closed=False)
            ctx.stroke()
            angle_marker(ctx, a, b, c, 2, radius=24, gap=6)
            ctx.stroke()

        def creator(file):
            make_image(file, draw, 600, 500)

        self.assertTrue(run_image_test('test_old_markers.png', creator))

    def test_lines(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # The line function is a convenience function that adds a line as a new path.
            # You can fill or stroke it as you wish.
            line(ctx, (1, 1), (2, 3))
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.set_line_width(0.1)
            ctx.stroke()

            # Line objects can only be stroked as they do not contain an area.
            Line(ctx).of_start_end((3, 1), (4, 4)).stroke(Color('fuchsia'), 0.2)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_lines.png', creator))

    def test_line_segment(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=6, background=Color(0.8))

            for i in range(9):
                angle = 2*math.pi*i/9
                a = (1.5 + 1.5*(i%3), 1.5 + 1.5*(i//3))
                b = (a[0] + math.cos(angle), a[1] + math.sin(angle))
                Line(ctx).of_start_end(a, b).as_segment().stroke(Color('fuchsia'), 0.05)
                Circle(ctx).of_center_radius(a, .1).fill(Color(0))

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_line_segment.png', creator))

    def test_line_ray(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=6, background=Color(0.8))

            for i in range(9):
                angle = 2*math.pi*i/9
                a = (1.5 + 1.5*(i%3), 1.5 + 1.5*(i//3))
                b = (a[0] + math.cos(angle), a[1] + math.sin(angle))
                Line(ctx).of_start_end(a, b).as_ray().stroke(Color('fuchsia'), 0.05)
                Circle(ctx).of_center_radius(a, .1).fill(Color(0))

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_line_ray.png', creator))

    def test_line_full(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=6, background=Color(0.8))

            for i in range(9):
                angle = 2*math.pi*i/9
                a = (1.5 + 1.5*(i%3), 1.5 + 1.5*(i//3))
                b = (a[0] + math.cos(angle), a[1] + math.sin(angle))
                Line(ctx).of_start_end(a, b).as_line().stroke(Color('fuchsia'), 0.05)
                Circle(ctx).of_center_radius(a, .1).fill(Color(0))

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_line_full.png', creator))

    def test_line_styles(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            Rectangle(ctx).of_corner_size((0.5, 1), 1, 1.2).stroke(Color(0, .5, 0), 0.1, dash=[0.25])
            Rectangle(ctx).of_corner_size((2, 1), 1, 1.2).stroke(Color(0, .5, 0), 0.1, dash=[0.25], cap=BUTT)
            Rectangle(ctx).of_corner_size((3.5, 1), 1.2, 1).stroke(Color(0, .5, 0), 0.1, dash=[0.25], cap=ROUND)
            Rectangle(ctx).of_corner_size((0.5, 3), 1, 1.2).stroke(Color(0, .5, 0), 0.1, join=ROUND)
            Rectangle(ctx).of_corner_size((2, 3), 1, 1.2).stroke(Color(0, .5, 0), 0.1, join=BEVEL)
            Rectangle(ctx).of_corner_size((3.5, 3), 1.2, 1).stroke(Color(0, .5, 0), 0.1, miter_limit=1)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_line_styles.png', creator))

    def test_ellipse(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # The ellipse function is a convenience function that adds a ellipse as a new the path.
            # You can fill or stroke it as you wish.
            ellipse(ctx, (1, 1), 0.7, 1.1)
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            # Ellipse objects can be filled, stroked, filled and stroked.
            Ellipse(ctx).of_center_radius((2.5, 1), 0.7, 0.3).fill(Color(0, 0, 1)).stroke(Color(0), 0.05)
            Ellipse(ctx).of_center_radius((4, 1), 0.7, 0.3).as_arc(0, 1).stroke(Color(0, 0.5, 0), 0.05)

            Ellipse(ctx).of_center_radius((1, 2.5), 0.7, 0.3).as_sector(1, 3).stroke(Color('orange'), 0.05)
            Ellipse(ctx).of_center_radius((2.5, 2.5), 0.7, 0.3).as_sector(2, 4.5).fill(Color('cadetblue'))
            Ellipse(ctx).of_center_radius((4, 2.5), 0.7, 0.3).as_sector(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

            Ellipse(ctx).of_center_radius((1, 4), 0.7, 0.3).as_segment(1, 3).stroke(Color('orange'), 0.05)
            Ellipse(ctx).of_center_radius((2.5, 4), 0.7, 0.3).as_segment(2, 4.5).fill(Color('cadetblue'))
            Ellipse(ctx).of_center_radius((4, 4), 0.7, 0.3).as_segment(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_ellipse.png', creator))

    def test_complex_paths(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=300, background=Color(1))

            # Fill then stroke a rectangle
            ctx.save()
            ctx.translate(0, 0)
            Rectangle(ctx).of_corner_size((20, 20), 60, 60).fill(Color('red')).stroke(Color('blue'), 10)
            ctx.restore()

            # Stroke then fill a rectangle
            ctx.save()
            ctx.translate(100, 0)
            Rectangle(ctx).of_corner_size((20, 20), 60, 60).stroke(Color('blue'), 10).fill(Color('red'))
            ctx.restore()

            # Path with two rectangles
            ctx.save()
            ctx.translate(200, 0)
            Rectangle(ctx).of_corner_size((20, 20), 60, 60).add()
            Rectangle(ctx).of_corner_size((30, 30), 60, 60).as_sub_path().fill(Color('red')).stroke(Color('blue'), 5)
            ctx.restore()

            # Path from several lines
            ctx.save()
            ctx.translate(0, 100)
            Line(ctx).of_start_end((20, 20), (60, 30)).add()
            Line(ctx).of_end((60, 60)).extend_path().add()
            Line(ctx).of_end((30, 50)).extend_path().fill(Color('red')).stroke(Color('blue'), 5)
            ctx.restore()

            # Path from several lines, closed
            ctx.save()
            ctx.translate(100, 100)
            Line(ctx).of_start_end((20, 20), (60, 30)).add()
            Line(ctx).of_end((60, 60)).extend_path().add()
            Line(ctx).of_end((30, 50)).extend_path(close=True).fill(Color('red')).stroke(Color('blue'), 5)
            ctx.restore()

            # roundrect open
            ctx.save()
            ctx.translate(0, 200)
            Circle(ctx).of_center_radius((20, 20), 10).as_arc(math.pi, math.pi * 3 / 2).add()
            Circle(ctx).of_center_radius((60, 20), 10).as_arc(math.pi * 3 / 2, 0).extend_path().add()
            Circle(ctx).of_center_radius((60, 60), 10).as_arc(0, math.pi / 2).extend_path().add()
            Circle(ctx).of_center_radius((20, 60), 10).as_arc(math.pi / 2, math.pi).extend_path().fill(
                Color('red')).stroke(Color('blue'), 5)
            ctx.restore()

            # roundrect closed
            ctx.save()
            ctx.translate(100, 200)
            Circle(ctx).of_center_radius((20, 20), 10).as_arc(math.pi, math.pi * 3 / 2).add()
            Circle(ctx).of_center_radius((60, 20), 10).as_arc(math.pi * 3 / 2, 0).extend_path().add()
            Circle(ctx).of_center_radius((60, 60), 10).as_arc(0, math.pi / 2).extend_path().add()
            Circle(ctx).of_center_radius((20, 60), 10).as_arc(math.pi / 2, math.pi).extend_path(close=True).fill(
                Color('red')).stroke(Color('blue'), 5)
            ctx.restore()

        def creator(file):
            make_image(file, draw, 600, 600)

        self.assertTrue(run_image_test('test_complex_paths.png', creator))

    def test_clip(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # Create a circular clip region and draw some squares in it
            ctx.save()
            Circle(ctx).of_center_radius((1.9, 1.9), 1).clip()
            Square(ctx).of_corner_size((1, 1), .8).fill(Color('red'))
            Square(ctx).of_corner_size((1, 2), .8).fill(Color('green'))
            Square(ctx).of_corner_size((2, 1), .8).fill(Color('blue'))
            Square(ctx).of_corner_size((2, 2), .8).fill(Color('black'))
            ctx.restore()

            ctx.save()
            Text(ctx).of("ABC", (1.5, 3.5)).font("Times", weight=FONT_WEIGHT_BOLD).size(1.5).align_left().align_top().clip()
            circles = [(2, 3.8, 'orange'), (2, 4.5, 'cyan'), (3, 3.8, 'green'),
                       (3, 4.5, 'purple'), (4, 3.8, 'yellow'), (4, 4.5, 'blue')]
            for x, y, color in circles:
                Circle(ctx).of_center_radius((x, y), 0.7).fill(Color(color))
            ctx.restore()

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_clip.png', creator))

    def test_circle(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # The circle function is a convenience function that adds a circle as a new the path.
            # You can fill or stroke it as you wish.
            circle(ctx, (1, 1), 0.7)
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            # Circle objects can be filled, stroked, filled and stroked.
            Circle(ctx).of_center_radius((2.5, 1), 0.7).fill(Color(0, 0, 1)).stroke(Color(0), 0.05)
            Circle(ctx).of_center_radius((4, 1), 0.7).as_arc(0, 1).stroke(Color(0, 0.5, 0), 0.05)

            Circle(ctx).of_center_radius((1, 2.5), 0.7).as_sector(1, 3).stroke(Color('orange'), 0.05)
            Circle(ctx).of_center_radius((2.5, 2.5), 0.7).as_sector(2, 4.5).fill(Color('cadetblue'))
            Circle(ctx).of_center_radius((4, 2.5), 0.7).as_sector(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

            Circle(ctx).of_center_radius((1, 4), 0.7).as_segment(1, 3).stroke(Color('orange'), 0.05)
            Circle(ctx).of_center_radius((2.5, 4), 0.7).as_segment(2, 4.5).fill(Color('cadetblue'))
            Circle(ctx).of_center_radius((4, 4), 0.7).as_segment(2.5, 6).fill(Color('yellow')).stroke(Color('magenta'), 0.05)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_circle.png', creator))

    def test_polygon(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=500, background=Color(0.8))

            # The polygon function is a convenience function that adds a polygon as a new path.
            # You can fill or stroke it as you wish.
            polygon(ctx, ((100, 100), (150, 50), (200, 150), (200, 200)))
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            Polygon(ctx).of_points([(300, 100), (300, 150), (400, 200), (450, 100)]).open().stroke(Color('orange'), 10)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_polygon.png', creator))

    def draw_regular_polygon(self, ctx, centre, sides, radius, angle):
        # Draw a regular polygon, including inner and outer circle and points.
        p = RegularPolygon(ctx).of_centre_sides_radius(centre, sides, radius, angle).fill(Color("palegoldenrod")).stroke(Color("blue"), 4)
        Circle(ctx).of_center_radius(centre, p.outer_radius).stroke(Color("black"), 4)
        Circle(ctx).of_center_radius(centre, p.inner_radius).stroke(Color("grey"), 4)
        for v in p.vertices:
            Circle(ctx).of_center_radius(v, 5).fill(Color("green"))


    def test_regular_polygon(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, background=Color(0.8))

            self.draw_regular_polygon(ctx, (150, 150), 3, 100, 0)
            self.draw_regular_polygon(ctx, (350, 150), 4, 100, 0)
            self.draw_regular_polygon(ctx, (550, 150), 7, 100, 0)
            self.draw_regular_polygon(ctx, (750, 150), 8, 100, 0)

            self.draw_regular_polygon(ctx, (150, 350), 3, 100, math.pi/6)
            self.draw_regular_polygon(ctx, (350, 350), 4, 100, math.pi/6)
            self.draw_regular_polygon(ctx, (550, 350), 7, 100, math.pi/6)
            self.draw_regular_polygon(ctx, (750, 350), 8, 100, math.pi/6)


        def creator(file):
            make_image(file, draw, 900, 500)

        self.assertTrue(run_image_test('test_regular_polygon.png', creator))

    def test_rectangle(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # The rectangle function is a convenience function that adds a rectangle as a new the path.
            # You can fill or stroke it as you wish.
            rectangle(ctx, (1, 1), 1, 1.2)
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            # Rectangle objects can be filled, stroked, filled and stroked.
            Rectangle(ctx).of_corner_size((3, 1), 1, 1.2).fill(Color(0, .5, 0))
            Rectangle(ctx).of_corner_size((1, 3), 1.2, 1).stroke(Color(0, .5, 0), 0.1)
            Rectangle(ctx).of_corner_size((3, 3), 1.2, 1).fill(Color(0, 0, 1)).stroke(Color(0), 0.2)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_rectangle.png', creator))

    def test_square(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # The square function is a convenience function that adds a square as a new the path.
            # You can fill or stroke it as you wish.
            square(ctx, (1, 1), 1)
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            # Square objects can be filled, stroked, filled and stroked.
            Square(ctx).of_corner_size((3, 1), 1).fill(Color(0, .5, 0))
            Square(ctx).of_corner_size((1, 3), 1).stroke(Color(0, .5, 0), 0.1)
            Square(ctx).of_corner_size((3, 3), 1).fill(Color(0, 0, 1)).stroke(Color(0), 0.2)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_square.png', creator))

    def test_triangle(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=500, background=Color(0.8))

            # The triangle function is a convenience function that adds a triangle as a new path.
            # You can fill or stroke it as you wish.
            triangle(ctx, (100, 100), (150, 50), (200, 150))
            ctx.set_source_rgba(*Color(1, 0, 0))
            ctx.fill()

            Triangle(ctx).of_corners((300, 100), (300, 150), (400, 200)).stroke(Color('orange'), 10)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_triangle.png', creator))

    def test_bezier(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=5, background=Color(0.8))

            # Bezier objects can only be stroked as they do not contain an area.
            Bezier(ctx).of_abcd((1, 1.5), (3, 0.5), (2, 2.5), (4, 1.5)).stroke(Color('darkgreen'), 0.1)

            # Create a polygon with a bezier side
            Polygon(ctx).of_points([(1, 4.5), (1, 2.5), (2, 3, 3, 4, 4, 2.5), (4, 4.5)])\
                        .fill(Color('red')).stroke(Color('blue'), 0.05)

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_bezier.png', creator))

    def test_text(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, width=5, background=Color(0.8))

            Text(ctx).of("Left", (0.5, 0.5)).font("Times").size(0.2).align_left().align_baseline().fill(Color('blue'))
            Text(ctx).of("Aligned", (0.5, 0.7)).font("Times").size(0.2).align_left().align_baseline().fill(Color('red'))
            Text(ctx).of("Text", (0.5, 0.9)).font("Times").size(0.2).align_left().align_baseline().fill(Color('blue'))

            Text(ctx).of("Centre", (2.5, 0.5)).font("Times", weight=FONT_WEIGHT_BOLD).size(0.2)\
                     .align_center().align_baseline().fill(Color('blue'))
            Text(ctx).of("Aligned", (2.5, 0.7)).font("Times", weight=FONT_WEIGHT_BOLD).size(0.2)\
                     .align_center().align_baseline().fill(Color('red'))
            Text(ctx).of("Text", (2.5, 0.9)).font("Times", weight=FONT_WEIGHT_BOLD).size(0.2)\
                     .align_center().align_baseline().fill(Color('blue'))

            Text(ctx).of("Right", (4.5, 0.5)).font("Times", slant=FONT_SLANT_ITALIC).size(0.2)\
                     .align_right().align_baseline().fill(Color('blue'))
            Text(ctx).of("Aligned", (4.5, 0.7)).font("Times", slant=FONT_SLANT_ITALIC).size(0.2)\
                     .align_right().align_baseline().fill(Color('red'))
            Text(ctx).of("Text", (4.5, 0.9)).font("Times", slant=FONT_SLANT_ITALIC).size(0.2)\
                     .align_right().align_baseline().fill(Color('blue'))

            Circle(ctx).of_center_radius((1.9, 2), 0.02).fill(Color(0, 0, 1))
            Text(ctx).of("gTop", (2, 2)).font("Times").size(0.2).align_left().align_top().fill(Color('black'))

            Circle(ctx).of_center_radius((1.9, 2.5), 0.02).fill(Color(0, 0, 1))
            Text(ctx).of("gMid", (2, 2.5)).font("Times").size(0.2).align_left().align_middle().fill(Color('black'))

            Circle(ctx).of_center_radius((1.9, 3), 0.02).fill(Color(0, 0, 1))
            Text(ctx).of("gBase", (2, 3)).font("Times").size(0.2).align_left().align_baseline().fill(Color('black'))

            Circle(ctx).of_center_radius((1.9, 3.5), 0.02).fill(Color(0, 0, 1))
            Text(ctx).of("gBottom", (2, 3.5)).font("Times").size(0.2).align_left().align_bottom().fill(Color('black'))

        def creator(file):
            make_image(file, draw, 400, 400)

        self.assertTrue(run_image_test('test_text.png', creator))

    def test_text_offset(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))

            Circle(ctx).of_center_radius((200, 200), 10).fill(Color('red'))
            Circle(ctx).of_center_radius((100, 150), 10).fill(Color('blue'))
            Text(ctx).of('A', (200, 200)).font('Arial').size(40).fill(Color(0))
            Text(ctx).of('B', (200, 200)).font('Arial').offset(100, 20).size(40).fill(Color(0))
            Text(ctx).of('C', (200, 200)).font('Arial').offset_angle(1, 150).size(40).fill(Color(0))
            Text(ctx).of('D', (200, 200)).font('Arial').offset_towards((100, 150), 50).size(40).fill(Color(0))

        def creator(file):
            make_image(file, draw, 400, 400)

        self.assertTrue(run_image_test('test_text_offset.png', creator))

    def test_geometry_image(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(1))
            Image(ctx).of_file_position('cat.png', (50, 50)).paint()
            Image(ctx).of_file_position('cat.png', (300, 50)).scale(0.5).paint()
            Image(ctx).of_file_position('cat.png', (50, 300)).scale(1.5).paint()
            Image(ctx).of_file_position('formula.png', (50, 600)).paint()
            Image(ctx).of_file_position('formula.png', (350, 200)).scale(0.5).paint()

        def creator(file):
            make_image(file, draw, 800, 800)

        self.assertTrue(run_image_test('test_geometry_image.png', creator))

    def test_path(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, width=5, background=Color(0.8))

            # Get a polygon path object
            path1 = Polygon(ctx).of_points([(0, 0), (1, 1), (0.5, 2), (0.5, 1)]).path()

            # Get a text path object
            path2 = Text(ctx).of("Path text", (0, 0)).font("Times", weight=FONT_WEIGHT_BOLD).size(0.2).align_left().align_top().path()

            # Apply the polygon in various places
            ctx.save()
            ctx.translate(0.5, 1)
            Path(ctx).of(path1).stroke(Color('darkgreen'), 0.1)
            ctx.restore()

            ctx.save()
            ctx.translate(1, 2.5)
            Path(ctx).of(path1).fill(Color('blue'))
            ctx.restore()

            ctx.save()
            ctx.translate(2.5, 0.5)
            ctx.scale(2, 2)
            Path(ctx).of(path1).fill(Color('orange')).stroke(Color('black'), 0.05)
            ctx.restore()

            # Apply the text in various places
            ctx.save()
            ctx.translate(0, 0)
            Path(ctx).of(path2).fill(Color('black'))
            ctx.restore()

            ctx.save()
            ctx.translate(2, 3)
            Path(ctx).of(path2).stroke(Color('red'), 0.01)
            ctx.restore()

            ctx.save()
            ctx.translate(2, 4)
            ctx.scale(2, 2)
            Path(ctx).of(path2).fill(Color('yellow')).stroke(Color('black'), 0.01)
            ctx.restore()

        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_path.png', creator))

    def test_turtle(self):

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            setup(ctx, pixel_width, pixel_height, background=Color(0.8))

            turtle = Turtle(ctx)
            turtle.move_to(100, 100).forward(50).left(math.pi/2).forward(50).left(math.pi/4).forward(50)

            turtle = Turtle(ctx)
            turtle.move_to(200, 300).set_style(Color('green'), line_width=5, dash=[10]) \
                .push().forward(100).pop() \
                .push().left(3 * math.pi / 4).forward(100).pop() \
                .right(3 * math.pi / 4).forward(100)

            turtle = Turtle(ctx)
            turtle.move_to(350, 100).right(math.pi/2).set_style(Color('red'), line_width=5, dash=[10], cap=ROUND)
            turtle.push().forward(100)
            turtle.set_style(Color('blue'), line_width=2, dash=[]).forward(100)
            turtle.pop().move_to(350, 300).forward(100)


        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_turtle.png', creator))

    def test_transform(self):
        def draw(ctx, width, height, frame_no, frame_count):
            setup(ctx, width, height, width=500, background=Color(0.8))

            with Transform(ctx) as transform:
                Text(ctx).of('A', (10, 100)).size(80).fill(Color('blue'))

            Text(ctx).of('B', (110, 100)).size(80).fill(Color('black'))
            with Transform(ctx) as transform:
                transform.scale(0.75, 1.5)
                Text(ctx).of('B', (110, 100)).size(80).fill(Color('blue', 0.5))

            Text(ctx).of('C', (210, 100)).size(80).fill(Color('black'))
            Circle(ctx).of_center_radius((250, 80), 5).fill(Color('red'))
            with Transform(ctx).scale(0.75, 1.5, (250, 80)):
                Text(ctx).of('C', (210, 100)).size(80).fill(Color('blue', 0.5))

            Text(ctx).of('D', (110, 200)).size(80).fill(Color('black'))
            with Transform(ctx) as transform:
                transform.translate(20, 30)
                Text(ctx).of('D', (110, 200)).size(80).fill(Color('blue', 0.5))

            Text(ctx).of('E', (110, 300)).size(80).fill(Color('black'))
            with Transform(ctx) as transform:
                transform.rotate(0.1)
                Text(ctx).of('E', (110, 300)).size(80).fill(Color('blue', 0.5))

            Text(ctx).of('F', (210, 300)).size(80).fill(Color('black'))
            Circle(ctx).of_center_radius((250, 80), 5).fill(Color('red'))
            with Transform(ctx).rotate(0.1, (210, 300)):
                Text(ctx).of('F', (210, 300)).size(80).fill(Color('blue', 0.5))

            Text(ctx).of('G', (210, 400)).size(80).fill(Color('black'))
            Circle(ctx).of_center_radius((250, 80), 5).fill(Color('red'))
            with Transform(ctx).matrix([1, 0.5, 0, 0, 1, 0]):
                Text(ctx).of('G', (210, 400)).size(80).fill(Color('blue', 0.5))


        def creator(file):
            make_image(file, draw, 500, 500)

        self.assertTrue(run_image_test('test_transform.png', creator))

