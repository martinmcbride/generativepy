import unittest
from image_test_helper import run_image3d_test
import moderngl
import numpy as np
from generativepy.color import Color

class TestDrawing3dImages(unittest.TestCase):

    def test_simple_drawing3d(self):
        def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
            prog = ctx.program(
                vertex_shader='''
                    #version 330

                    in vec2 in_vert;
                    in vec3 in_color;

                    out vec3 v_color;

                    void main() {
                        v_color = in_color;
                        gl_Position = vec4(in_vert, 0.0, 1.0);
                    }
                ''',
                fragment_shader='''
                    #version 330

                    in vec3 v_color;

                    out vec3 f_color;

                    void main() {
                        f_color = v_color;
                    }
                ''',
            )

            x = np.linspace(-1.0, 1.0, 50)
            y = np.random.rand(50) - 0.5
            r = np.ones(50)
            g = np.zeros(50)
            b = np.zeros(50)

            vertices = np.dstack([x, y, r, g, b])

            vbo = ctx.buffer(vertices.astype('f4').tobytes())
            vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

            vao.render(moderngl.LINE_STRIP)

        self.assertTrue(run_image3d_test('test_simple_drawing3d.png', draw, 700, 600, Color('grey')))
