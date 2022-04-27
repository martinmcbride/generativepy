# generativepy

Generative art and graphing library for creating images and animations.

## Version 3.1 notes

* New `formulas` module converts latex formulas to bitmap that can be used with the `Image` class.
* New `MovieBuilder` class allows movies to be created from multiple scenes, with option to add audio files.
* MINOR BREAKING CHANGE - `Plot` no longer automatically clips to axes, requires explicit axes.clip().
* Make right angle marker slightly bigger to match normal angle markers.
* Change angle, tick and parallel markers to be implemented as Shapes.
* Add text style (size and font) to `Axes` in the graph module.
* Started updating/extending tutorials on github to match the [generativepy tutorial](http://www.pythoninformer.com/generative-art/generativepy-tutorial/). The current examples folder will be deprecated.
* Clarify that default fill rule for `Shape` objects is `WINDING` (documentation change).
* Add [Transform](http://www.pythoninformer.com/generative-art/generativepy/transform/) class for transforming user space.

## Usage

generativepy is a library rather an application. It provides useful functions and example code that allow you to
create images and videos by writing simple Python scripts.

The library requires:

* [pycairo](https://pycairo.readthedocs.io/en/latest/index.html).
* NumPy.
* Pillow.
* easy_vector.
* moderngl (only required for 3D imaging).
* MoviePy
* Command line application gifsicle (only needed for GIF creation).
* Commandline applications latex and divpng

Main functionality:

* A simple framework for creating images, image sequences, and gifs, using pycairo.
* Support for bitmap processing using PIL and NumPy.
* Colour module that supports RGB, HSL and CSS colours, transparency, lerping, colormaps.
* A simple tweening module to help with animation.
* Geometry module for drawing shapes.
* A graphing library for plotting 2D functions.
* MovieBuilder supports creating video files from separate scenes.
* 3D geometry module using moderngl.

## Website

Visit [pythoninformer.com](http://www.pythoninformer.com/generative-art/) for details:

* [generativepy reference](http://www.pythoninformer.com/generative-art/generativepy/).
* [generativepy tutorials](http://www.pythoninformer.com/generative-art/generativepy-tutorial/).

There are also some art examples in the Generative Art section of [my blog](https://martinmcbride.org/).

For detailed information of pycairo see the [Computer graphics in Python](https://leanpub.com/computergraphicsinpython) ebook.
