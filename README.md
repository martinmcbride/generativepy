# generativepy

Generative art and graphing library for creating images and animations.

## Version 4.0 notes

3D drawing is likely to change in a future release. The rest of the library is reasonably stable. 

* Allow images to eb preloaded for `Image` objects, to avoid frequent file reloads when creating animations.
* Add shapes2d module representing abstract shapes.
* Add math module with 2D vector and matrix classes.
* Add `ORANGE`, `CYAN` to `ArtisticColorScheme`.
* Add table module for table layouts.
* MINOR BREAKING CHANGE - Extra warning if some scenes don't have audio (behaviour change if not all audio present).
* BREAKING CHANGE - Tween use absolute time and a global frame rate. New methods wait_d and to_d for relative times.
* BREAKING CHANGE - Remove count for Tween set method. This didn't work well with absolute times. Use `set` followed by `wait` or `wait_d` to set and hold a value.
* BREAKING CHANGE - Improve geometry3d.
* Fix colour depth problem in geometry3d (previously r, g, b values were forced to either 0% to 100%)
* Allow special formatting of graph tick text labels
* Allow tick label positions to be controlled in graph `Axes`.
* Allow extra Latex packages to be specified in `formulas` module.
* Fix bug in `formulas` module when function could hang if Latex formula was incorrect.

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
