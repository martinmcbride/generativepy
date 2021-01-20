# Author:  Martin McBride
# Created: 2021-019-01
# Copyright (C) 2018, Martin McBride
# License: MIT

from direct.showbase.ShowBase import ShowBase
from panda3d.core import FrameBufferProperties, WindowProperties, loadPrcFileData
import numpy as np
from PIL import Image

def make_image3d(outfile, draw, width, height, channels=3):
    '''
    Create a PNG file using panda3d
    :param outfile: Name of output file
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    frame = make_image3d_frame(draw, width, height, channels)
    image = Image.fromarray(frame)
    image.save(outfile + '.png')

def make_image3d_frame(draw, width, height, channels=3):
    '''
    Create a numpy frame file using panda3d
    :param draw: the draw function
    :param width: width in pixels, int
    :param height: height in pixels, int
    :param channels: 3 for rgb, 4 for rgba
    :return:
    '''
    base = ShowBase()
    loadPrcFileData("", "window-type offscreen")
    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    # fb_prop.setRgbColor(True)
    # fb_prop.setRgbaBits(8, 8, 8, 0)
    # fb_prop.setDepthBits(16)
    props.set_rgb_color(True)
    props.set_depth_bits(16)
    props.set_stereo(True)

    # Create a WindowProperties object set to 512x512 size.
    win_prop = WindowProperties.size(512, 512)    # Add the model
    cube = base.loader.loadModel('misc/rgbCube')
    cube.reparent_to(base.render)
    # Initial camera setup
    base.camera.set_pos(5, 5, 5)
    base.camera.look_at(0, 0, 0)
    ##
    base.graphicsEngine.renderFrame()
    dr = base.camNode.getDisplayRegion(0)
    tex = dr.getScreenshot()
    data = tex.getRamImage()
    v = memoryview(data).tolist()
    frame = np.array(v, dtype=np.uint8)
    frame = frame.reshape((tex.getYSize(), tex.getXSize(), 4))
    frame = frame[::-1]

    return frame


