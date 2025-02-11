# Image tests

This area contains image tests for generativepy.

The purpose of these tests is to check the images created by generativepy is an automated, repeatable way.

Each test creates a PNG file the exercises particular drawing capabilities. This PNG files are written out to the system temp folder.

After each test, the image created is compared, pixel-for-pixel, with the equivalent reference image in the images folder. The reference images have been previously checked manually.

The tests are implemented as unit tests to allow the unit test discovery and reporting tools to be used.

Run all_image_tests.py to run all the tests.

There is also a set of unit tests in the test folder which test the non-image functionality. Both the image tests and the unit tests should be run to check the library.

