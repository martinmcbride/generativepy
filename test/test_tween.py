import unittest
from generativepy.tween import Tween, TweenVector

class TestTween(unittest.TestCase):

    def test_empty_tween(self):
        tween = Tween()
        self.assertEqual(len(tween), 0)

    def test_wait_tween(self):
        tween = Tween(5)
        tween.wait(10)
        self.assertEqual(len(tween), 10)
        self.assertEqual(tween.get(0), 5)
        self.assertEqual(tween.get(9), 5)
        self.assertEqual(tween[0], 5)
        self.assertEqual(tween[9], 5)

    def test_set_tween(self):
        tween = Tween(3)
        tween.wait(6)
        tween.set(2.5, 8)
        self.assertEqual(len(tween), 14)
        self.assertEqual(tween.get(0), 3)
        self.assertEqual(tween[5], 3)
        self.assertEqual(tween[6], 2.5)
        self.assertEqual(tween.get(13), 2.5)
        expected = [3, 3, 3, 3, 3, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 13)

    def test_to_tween(self):
        tween = Tween(3)
        tween.to(9, 10)
        self.assertEqual(len(tween), 10)
        expected = [3.6, 4.2, 4.8, 5.4, 6.0, 6.6, 7.2, 7.8, 8.4, 9]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 9)

    def test_to_tween_length_1(self):
        tween = Tween(3)
        tween.to(9, 1)
        self.assertEqual(len(tween), 1)
        expected = [9]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_to_tween_length_0(self):
        tween = Tween(3)
        tween.to(9, 0)
        self.assertEqual(len(tween), 0)

    def test_empty_tweenvector(self):
        tween = TweenVector((.1, .2, .3))
        self.assertEqual(len(tween), 0)

    def test_set_tweenvector(self):
        tween = TweenVector((.1, .2, .3))
        tween.wait(3)
        tween.set((6, 4, 2), 4)
        self.assertEqual(len(tween), 7)
        self.assertEqual(tween.get(0), (.1, .2, .3))
        self.assertEqual(tween[2], (.1, .2, .3))
        self.assertEqual(tween[3], (6, 4, 2))
        self.assertEqual(tween.get(6), (6, 4, 2))
        expected = [(.1, .2, .3), (.1, .2, .3), (.1, .2, .3), (6, 4, 2), (6, 4, 2), (6, 4, 2), (6, 4, 2)]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 6)

    def test_to_tweenvector(self):
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 5)
        self.assertEqual(len(tween), 5)
        expected = [[1, 2, 3], [2, 4, 6], [3, 6, 9], [4, 8, 12], [5, 10, 15]]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 4)

    def test_to_tweenvector_length_1(self):
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 1)
        self.assertEqual(len(tween), 1)
        expected = [[5, 10, 15]]
        for i, v in enumerate(tween):
            self.assertEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_to_tweenvector_length_0(self):
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 0)
        self.assertEqual(len(tween), 0)

