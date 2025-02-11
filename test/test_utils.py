import unittest
from generativepy.utils import correct_pycairo_byte_order, temp_file
import numpy as np


## These tests assume a littleendian machine

class TestUtils(unittest.TestCase):

    def test_tempfile_1_name(self):
        fn = temp_file('testname.png')
        self.assertEqual('/tmp/testname.png', fn)

    def test_tempfile_2_name(self):
        fn = temp_file('abc', 'testname.png')
        self.assertEqual('/tmp/abc/testname.png', fn)

    def test_3_channel(self):
        indata = [[[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]],
                  [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]],
                  [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]],
                  [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]]

        outdata = [[[3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]],
                   [[3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]],
                   [[3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]],
                   [[3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1], [3, 2, 1]]]
        array = np.array(indata)
        expected = np.array(outdata)
        result = correct_pycairo_byte_order(array, 3)
        self.assertTrue(np.array_equal(expected, result))


    def test_4_channel(self):
        indata = [[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                  [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                  [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                  [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]]

        outdata = [[[3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4]],
                   [[3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4]],
                   [[3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4]],
                   [[3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4], [3, 2, 1, 4]]]
        array = np.array(indata)
        expected = np.array(outdata)
        result = correct_pycairo_byte_order(array, 4)
        self.assertTrue(np.array_equal(expected, result))
