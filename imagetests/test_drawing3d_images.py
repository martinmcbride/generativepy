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

        self.assertTrue(run_image3d_test('test_simple_drawing3d.png', draw, 700, 600, Color('grey')))
