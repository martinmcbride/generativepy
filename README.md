# generativepy

Generative art and graphing library for creating images and animations.

## Version 23.11 notes

3D drawing is likely to change in a future release. The rest of the library is reasonably stable. 

* Switched to date based versioning
* Add parametric plots to the graph module 
* Allow The Turtle class to accept a list of colours, and cycle through the list as the turtle draws a path.
* Update geometry.Transform class to use generativepy matrix order rather than PyCairo matrix order.
* Add unit matrix to math module

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
* Latex formula rendering
* 3D geometry module using moderngl.
* Math modules for vectors, matrices and abstract shapes. 

## Website

Visit [pythoninformer.com](http://www.pythoninformer.com/generative-art/) for details:

* [generativepy reference](http://www.pythoninformer.com/generative-art/generativepy/).
* [generativepy tutorials](http://www.pythoninformer.com/generative-art/generativepy-tutorial/).

There are also some art examples in the Generative Art section of [my blog](https://martinmcbride.org/).

For detailed information of pycairo see the [Computer graphics in Python](https://leanpub.com/computergraphicsinpython) ebook.
