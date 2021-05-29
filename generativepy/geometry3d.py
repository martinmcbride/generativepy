# Author:  Martin McBride
# Created: 2021-05-27
# Copyright (C) 2021, Martin McBride
# License: MIT

import numpy as np
from generativepy.color import Color

class Shader():

    def __init__(self):
        self.code = ''

    def get_code(self):
        return self.code


class FlatColorVertexShader(Shader):

    def __init__(self):
        self.code = '''
                #version 330
                in vec3 in_vert;
                in vec3 in_color;
                out vec3 v_color;    // Goes to the fragment shader
                uniform float z_near;
                uniform float z_far;
                uniform float fovy;
                uniform float ratio;
                uniform vec3 center;
                uniform vec3 eye;
                uniform vec3 up;
                mat4 perspective() {
                    float zmul = (-2.0 * z_near * z_far) / (z_far - z_near);
                    float ymul = 1.0 / tan(fovy * 3.14159265 / 360);
                    float xmul = ymul / ratio;
                    return mat4(
                        xmul, 0.0, 0.0, 0.0,
                        0.0, ymul, 0.0, 0.0,
                        0.0, 0.0, -1.0, -1.0,
                        0.0, 0.0, zmul, 0.0
                    );
                }
                mat4 lookat() {
                    vec3 forward = normalize(center - eye);
                    vec3 side = normalize(cross(forward, up));
                    vec3 upward = cross(side, forward);
                    return mat4(
                        side.x, upward.x, -forward.x, 0,
                        side.y, upward.y, -forward.y, 0,
                        side.z, upward.z, -forward.z, 0,
                        -dot(eye, side), -dot(eye, upward), dot(eye, forward), 1
                    );
                }
                void main() {
                    gl_Position = perspective() * lookat() * vec4(in_vert, 1.0);
                    v_color = in_color;
                }
            '''


class FlatColorFragmentShader(Shader):

    def __init__(self):
        self.code = '''
                    #version 330
                    in vec3 v_color;
                    out vec4 f_color;
                    void main() {
                        f_color = vec4(v_color, 1.0);
                    }
            '''


class FlatColorProgram:

    def __init__(self, ctx):
        self.program = ctx.program(vertex_shader=FlatColorVertexShader().get_code(),
                                   fragment_shader=FlatColorFragmentShader().get_code())

    def set_uniform(self, z_near=0.1, z_far=1000.0, ratio=1, fovy=20, eye=(1, 0, 0), center=(0, 0, 0), up=(0, 1, 1)):
        self.program['z_near'].value = z_near
        self.program['z_far'].value = z_far
        self.program['ratio'].value = ratio
        self.program['fovy'].value = fovy

        self.program['eye'].value = eye
        self.program['center'].value = center
        self.program['up'].value = up
        return self

    def set_value(self, name, value):
        self.program[name].value = value
        return self

    def get_program(self):
        return self.program


class Triangle():

    def __init__(self):
        self.vertices = np.array([
                # x, y, z
                [0.0, 0.8, 0.0],
                [-0.6, -0.8, 0.0],
                [0.6, -0.8, 0.0]
            ], dtype='f4')
        self.Color = Color(0)

    def get_flat_color(self, color):
        self.Color = color
        color_row = np.array([color.as_rgb_bytes()], dtype='f4')
        colors = np.repeat(color_row, 3, axis=0)
        vertex_data = np.concatenate([self.vertices, colors], axis=1)
        return vertex_data

