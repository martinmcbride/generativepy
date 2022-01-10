# generativepy

Generative art and graphing library for creating images and animations.

## Version 3.0 notes

Version 3 introduces a few breaking changes compared to 2.x, mainly to improve the graph module.

* The `Axes` class has changed. The main breaking change is that it now uses the current user coordinates to control line thickness and text size, just like most other classes. Previously it used a crazy system of guesswork and magic scaling factors. On the plus side, it now also allows much more control over the axes appearance.
* The previous graph plotting functions have gone. Plotting is now done by a `Plot` class, that works in a similar way to other shape classes.
* A minor change is that the `color` parameter has been renamed to `pattern` in most places, to reflect the fact that it can now be a gradient (and hopefully soon image, vector pattern and mesh fills will be supported). This will only affect code that uses a named parameter for `color`. The parameter itself can still accept `Color` objects, as well as the new `LinearGradient` objects.

## Usage

generativepy is a library rather an application. It provides useful functions and example code that allow you to
create images and videos by writing simple Python scripts.

The library requires:

* [pycairo](https://pycairo.readthedocs.io/en/latest/index.html).
* NumPy.
* Pillow.
* easy_vector.
* moderngl (only required for 3D imaging).
* Command line application gifsicle (only needed for GIF creation).

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

There are also some art examples in the Generative Art section of [my blog](https://martinmcbride.org/).

For detailed information of pycairo see the [Computer graphics in Python](https://leanpub.com/computergraphicsinpython) ebook.
