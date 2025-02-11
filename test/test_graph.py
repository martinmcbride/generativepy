import unittest
import cairo
from generativepy.graph import Axes
from generativepy.math import Vector as V


class TestGraph(unittest.TestCase):

    # Test text extent
    def test_axes_point(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        axes = Axes(ctx, (20, 30), 400, 500).of_start((1, 2)).of_extent((4, 10))
        t = axes.transform_from_graph([2, 4])
        self.assertEqual(t, V(120, 430))

    def test_axes_points1(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        axes = Axes(ctx, (20, 30), 400, 500).of_start((1, 2)).of_extent((4, 10))
        t = axes.transform_from_graph(([2, 4],))
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0], V(120, 430))

    def test_axes_points2(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        axes = Axes(ctx, (20, 30), 400, 500).of_start((1, 2)).of_extent((4, 10))
        t = axes.transform_from_graph(([2, 4], [4, 2]))
        self.assertEqual(len(t), 2)
        self.assertEqual(t[0], V(120, 430))
        self.assertEqual(t[1], V(320, 530))

    def test_axes_points0(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        axes = Axes(ctx, (20, 30), 400, 500).of_start((1, 2)).of_extent((4, 10))
        t = axes.transform_from_graph(())
        self.assertEqual(len(t), 0)

    def test_axes_error(self):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 200)
        ctx = cairo.Context(surface)
        axes = Axes(ctx, (20, 30), 400, 500).of_start((1, 2)).of_extent((4, 10))
        with self.assertRaises(TypeError):
            axes.transform_from_graph(1)
        with self.assertRaises(ValueError):
            axes.transform_from_graph([1])
        with self.assertRaises(ValueError):
            axes.transform_from_graph([1, 2, 3])
        with self.assertRaises(ValueError):
            axes.transform_from_graph([[1]])
        with self.assertRaises(ValueError):
            axes.transform_from_graph([[1, 2, 3]])



if __name__ == '__main__':
    unittest.main()
