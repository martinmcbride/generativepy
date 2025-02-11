import unittest
from image_test_helper import run_image_test
from generativepy.drawing3d import make_3dimage
from generativepy.geometry3d import FlatColorProgram, Triangle, Triangles
import moderngl
import numpy as np
from generativepy.color import Color
import math

class TestDrawing3dImages(unittest.TestCase):

    def test_simple_drawing3d(self):
        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            prog = ctx.program(
                vertex_shader='''
                    #version 330
                    in vec2 in_vert;
                    in vec3 in_color;
                    out vec3 v_color;    // Goes to the fragment shader
                    void main() {
                        gl_Position = vec4(in_vert, 0.0, 1.0);
                        v_color = in_color;
                    }
                ''',
                fragment_shader='''
                    #version 330
                    in vec3 v_color;
                    out vec4 f_color;
                    void main() {
                        // We're not interested in changing the alpha value
                        f_color = vec4(v_color, 1.0);
                    }
                ''',
            )

            # Point coordinates are put followed by the vec3 color values
            vertices = np.array([
                # x, y, red, green, blue
                0.0, 0.8, 1.0, 0.0, 0.0,
                -0.6, -0.8, 0.0, 1.0, 0.0,
                0.6, -0.8, 0.0, 0.0, 1.0,
            ], dtype='f4')

            vbo = ctx.buffer(vertices)

            # We control the 'in_vert' and `in_color' variables
            vao = ctx.vertex_array(
                prog,
                [
                    # Map in_vert to the first 2 floats
                    # Map in_color to the next 3 floats
                    (vbo, '2f 3f', 'in_vert', 'in_color')
                ],
            )

            vao.render(moderngl.TRIANGLES)

        def creator(file):
            make_3dimage(file, draw, 700, 600, Color('grey'))

        self.assertTrue(run_image_test('test_simple_drawing3d.png', creator))


    def test_flatcolor_drawing3d(self):
        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            prog = FlatColorProgram(ctx).set_uniform(eye=(0, 0, 6), up=(0, 1, 0)).get_program()
            vertices = Triangle([0, 0.8, 0], [-.6, -.8, 0], [.6, -.8, 0]).get_flat_color(Color('red'))

            vbo = ctx.buffer(vertices)

            vao = ctx.vertex_array(prog,
                                   [(vbo, '3f 3f', 'in_vert', 'in_color')])
            vao.render(moderngl.TRIANGLES)

            vertices = Triangle([0, 0.4, 0], [-.3, -.4, 0], [.3, -.4, 0]).get_flat_color(Color('blue'))

            vbo = ctx.buffer(vertices)

            vao = ctx.vertex_array(prog,
                                   [(vbo, '3f 3f', 'in_vert', 'in_color')])
            vao.render(moderngl.TRIANGLES)

        def creator(file):
            make_3dimage(file, draw, 700, 600, Color('grey'))

        self.assertTrue(run_image_test('test_flatcolor_drawing3d.png', creator))

    def test_flatcolor_rectangle_drawing3d(self):
        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            prog = FlatColorProgram(ctx).set_uniform(eye=(0, 0, 6), up=(0, 1, 0)).get_program()
            vertices = Triangles([0.5, 0.5, 0], [-0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.5, 0]).get_flat_color(Color('orange'))

            vbo = ctx.buffer(vertices)

            vao = ctx.vertex_array(prog,
                                   [(vbo, '3f 3f', 'in_vert', 'in_color')])
            vao.render(moderngl.TRIANGLE_STRIP)

        def creator(file):
            make_3dimage(file, draw, 700, 600, Color('grey'))

        self.assertTrue(run_image_test('test_flatcolor_rectangle_drawing3d.png', creator))


    def test_flatcolor_cube_drawing3d(self):
        def create_rect(ctx, a, b, c, d, color):
            angle = 2.5
            eye = (10 * math.cos(angle), 5, 10 * math.sin(angle))
            prog = FlatColorProgram(ctx).set_uniform(eye=eye, up=(0, 1, 0)).get_program()
            vertices = Triangles(a, b, c, d).get_flat_color(color)

            vbo = ctx.buffer(vertices)

            vao = ctx.vertex_array(prog,
                                   [(vbo, '3f 3f', 'in_vert', 'in_color')])
            vao.render(moderngl.TRIANGLE_STRIP)


        def displace(p, x, y, z):
            return p[0] + x, p[1] + y, p[2] + z

        def create_cube(ctx, unfold):
            '''
            Draw a cube centered on (0, 0, 0)
            :param ctx:
            :param unfold: 0.0 (totally folded) to 1.0 (totally unfolded)
            :return:
            '''
            angle = unfold * math.pi / 2
            s = math.sin(angle)
            c = math.cos(angle)
            s2 = math.sin(angle * 2)
            c2 = math.cos(angle * 2)
            A0 = (-1, -1, -1)
            A1 = (-1, -1, 1)
            A2 = (1, -1, -1)
            A3 = (1, -1, 1)

            E0 = (-1, 1, -1)
            E1 = (-1, 1, 1)
            E2 = (1, 1, -1)
            E3 = (1, 1, 1)

            C1 = displace(E0, 0, 2 * (c - 1), -2 * s)
            C3 = displace(E2, 0, 2 * (c - 1), -2 * s)
            B2 = displace(E0, -2 * s, 2 * (c - 1), 0)
            B3 = displace(E1, -2 * s, 2 * (c - 1), 0)
            D0 = displace(E1, 0, 2 * (c - 1), 2 * s)
            D2 = displace(E3, 0, 2 * (c - 1), 2 * s)
            F0 = displace(E0, 2 * s - 2 * (c2 - 1), 2 * (c - 1) + s2, 0)
            F1 = displace(E1, 2 * s - 2 * (c2 - 1), 2 * (c - 1) + s2, 0)
            F2 = displace(E2, 2 * s, 2 * (c - 1), 0)
            F3 = displace(E3, 2 * s, 2 * (c - 1), 0)

            create_rect(ctx, A0, A1, A2, A3, Color("orange"))
            create_rect(ctx, F0, F1, F2, F3, Color("purple"))
            create_rect(ctx, A0, C1, A2, C3, Color("cadetblue"))
            create_rect(ctx, A0, A1, B2, B3, Color("darkcyan"))
            create_rect(ctx, D0, A1, D2, A3, Color("lawngreen"))
            create_rect(ctx, F2, F3, A2, A3, Color("darkred"))

        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            ctx.enable(moderngl.DEPTH_TEST)
            create_cube(ctx, 0.4)
        def creator(file):
            make_3dimage(file, draw, 600, 600, Color('grey'))

        self.assertTrue(run_image_test('test_flatcolor_cube_drawing3d.png', creator))
