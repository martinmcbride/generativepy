# generativepy

Generative art and graphing library for creating images and animations.

## Breaking changes

The graph module in this repo has been updated in anticipation of V3. This will offer significant improvements going forward:

* Fluent interface for axes will allow for more formatting options to be added in the future.
* Line thickness and text sizes are controlled by current context, rather than relying on magic scaling factors.
* Graph plots are now Shapes (similar to Polygons) to more consistent with other items.
* This will allow for other axis styles (eg logarithmic and polar plots) and other plot types (bar, scatter etc) in the future. 

*These are breaking changes, but affecting the graph module only. They should also be regarded as experimental, as they might change in the final release. The documentation on pythoninformer.com has not been updated and still reflects V2.5.*

It is recommended that you continue working with V2.5 for now, until V3 is released. The code can be donwloaded from PyPi.org and the documentation on pythoninformer is correct.

But if you are keen to try out the changes, feel free to dig into the code, and also look at test_graph_module.py in the imagetests folder, that shows how the new interface is used.

## Usage

generativepy is a library rather an application. It provides useful functions and example code that allow you to
create images and videos by writing simple Python scripts.

The library uses [pycairo](https://pycairo.readthedocs.io/en/latest/index.html) for drawing graphics.

Main functionality:

* A simple framework for creating images, image sequences, and gifs, using pycairo.
* Support for bitmap processing using PIL and NumPy.
* Colour module that supports RGB, HSL and CSS colours, transparency, lerping, colormaps.
* A simple tweening module to help with animation.
* Geometry module for drawing shapes.
* A graphing library for plotting 2D functions.
* 3D geometry module using moderngl.

## Website

Visit [pythoninformer.com](http://www.pythoninformer.com/generative-art/) for details:

* [generativepy reference](http://www.pythoninformer.com/generative-art/generativepy/).
* [generativepy tutorials](http://www.pythoninformer.com/generative-art/generativepy-tutorial/).
* [Generative art examples](http://www.pythoninformer.com/generative-art/generativepy-art/).
* [Fractal examples](http://www.pythoninformer.com/generative-art/fractals/).

For detailed information of pycairo see the [Computer graphics in Python](https://leanpub.com/computergraphicsinpython) ebook.
