import unittest
from generativepy.tween import Tween, TweenVector, set_frame_rate, ease_linear
import generativepy.tween


def test_linear():
    def f(x):
        if x < -0.0001:
            return -1000
        elif x > 1.0001:
            return 1000
        else:
            return x

    return f


class TestTween(unittest.TestCase):

    def test_empty_tween(self):
        set_frame_rate(2)
        tween = Tween()
        self.assertEqual(len(tween), 0)

    def test_wait_tween(self):
        set_frame_rate(2)
        tween = Tween(5)
        tween.wait(10)
        tween.wait(15)
        self.assertEqual(len(tween), 30)
        self.assertEqual(tween.get(0), 5)
        self.assertEqual(tween.get(9), 5)
        self.assertEqual(tween[0], 5)
        self.assertEqual(tween[9], 5)

    def test_wait_d_tween(self):
        set_frame_rate(2)
        tween = Tween(5)
        tween.wait_d(10)
        tween.wait_d(5)
        self.assertEqual(len(tween), 30)
        self.assertEqual(tween.get(0), 5)
        self.assertEqual(tween.get(9), 5)
        self.assertEqual(tween[0], 5)
        self.assertEqual(tween[9], 5)

    def test_set_tween(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.wait(6)
        tween.set(2.5)
        tween.wait(14)
        self.assertEqual(len(tween), 28)
        self.assertEqual(tween.get(0), 3)
        self.assertEqual(tween[11], 3)
        self.assertEqual(tween[12], 2.5)
        self.assertEqual(tween.get(27), 2.5)
        expected = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 27)

    def test_to_tween(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.to(9, 10)
        tween.to(3, 20)
        self.assertEqual(len(tween), 40)
        expected = [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.7, 6.0, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8, 8.1, 8.4, 8.7, 9.0,
                    8.7, 8.4, 8.1, 7.8, 7.5, 7.2, 6.9, 6.6, 6.3, 6.0, 5.7, 5.4, 5.1, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.0]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 39)

    def test_to_d_tween(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.to_d(9, 10)
        tween.to_d(3, 10)
        self.assertEqual(len(tween), 40)
        expected = [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.7, 6.0, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8, 8.1, 8.4, 8.7, 9.0,
                    8.7, 8.4, 8.1, 7.8, 7.5, 7.2, 6.9, 6.6, 6.3, 6.0, 5.7, 5.4, 5.1, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.0]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 39)

    def test_to_tween_length_1(self):
        set_frame_rate(1)
        tween = Tween(3)
        tween.to(9, 1)
        self.assertEqual(len(tween), 1)
        expected = [9]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_to_tween_length_0(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.to(9, 0)

    def test_ease_tween(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.ease(9, 10, test_linear())
        tween.ease(3, 20, test_linear())
        self.assertEqual(len(tween), 40)
        expected = [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.7, 6.0, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8, 8.1, 8.4, 8.7, 9.0,
                    8.7, 8.4, 8.1, 7.8, 7.5, 7.2, 6.9, 6.6, 6.3, 6.0, 5.7, 5.4, 5.1, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.0]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 39)

    def test_ease_d_tween(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.ease_d(9, 10, test_linear())
        tween.ease_d(3, 10, test_linear())
        self.assertEqual(len(tween), 40)
        expected = [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 5.4, 5.7, 6.0, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8, 8.1, 8.4, 8.7, 9.0,
                    8.7, 8.4, 8.1, 7.8, 7.5, 7.2, 6.9, 6.6, 6.3, 6.0, 5.7, 5.4, 5.1, 4.8, 4.5, 4.2, 3.9, 3.6, 3.3, 3.0]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 39)

    def test_ease_tween_length_1(self):
        set_frame_rate(1)
        tween = Tween(3)
        tween.ease(9, 1, test_linear())
        self.assertEqual(len(tween), 1)
        expected = [9]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_ease_tween_length_0(self):
        set_frame_rate(2)
        tween = Tween(3)
        tween.ease(9, 0, test_linear())

    def test_empty_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((.1, .2, .3))
        self.assertEqual(len(tween), 0)

    def test_set_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((.1, .2, .3))
        tween.wait(3)
        tween.set((6, 4, 2))
        tween.wait(7)
        self.assertEqual(len(tween), 14)
        self.assertEqual(tween.get(0), (.1, .2, .3))
        self.assertEqual(tween[2], (.1, .2, .3))
        self.assertEqual(tween[6], (6, 4, 2))
        self.assertEqual(tween.get(13), (6, 4, 2))
        expected = [(0.1, 0.2, 0.3), (0.1, 0.2, 0.3), (0.1, 0.2, 0.3), (0.1, 0.2, 0.3), (0.1, 0.2, 0.3),
                    (0.1, 0.2, 0.3), (6, 4, 2), (6, 4, 2), (6, 4, 2), (6, 4, 2), (6, 4, 2), (6, 4, 2),
                    (6, 4, 2), (6, 4, 2)]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 13)

    def test_to_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 5)
        tween.to((0, 0, 0), 10)
        self.assertEqual(len(tween), 20)
        expected = [[0.5, 1.0, 1.5], [1.0, 2.0, 3.0], [1.5, 3.0, 4.5], [2.0, 4.0, 6.0], [2.5, 5.0, 7.5],
                    [3.0, 6.0, 9.0], [3.5, 7.0, 10.5], [4.0, 8.0, 12.0], [4.5, 9.0, 13.5], [5.0, 10.0, 15.0],
                    [4.5, 9.0, 13.5], [4.0, 8.0, 12.0], [3.5, 7.0, 10.5], [3.0, 6.0, 9.0], [2.5, 5.0, 7.5],
                    [2.0, 4.0, 6.0], [1.5, 3.0, 4.5], [1.0, 2.0, 3.0], [0.5, 1.0, 1.5], [0.0, 0.0, 0.0]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 19)

    def test_to_d_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.to_d((5, 10, 15), 5)
        tween.to_d((0, 0, 0), 5)
        self.assertEqual(len(tween), 20)
        expected = [[0.5, 1.0, 1.5], [1.0, 2.0, 3.0], [1.5, 3.0, 4.5], [2.0, 4.0, 6.0], [2.5, 5.0, 7.5],
                    [3.0, 6.0, 9.0], [3.5, 7.0, 10.5], [4.0, 8.0, 12.0], [4.5, 9.0, 13.5], [5.0, 10.0, 15.0],
                    [4.5, 9.0, 13.5], [4.0, 8.0, 12.0], [3.5, 7.0, 10.5], [3.0, 6.0, 9.0], [2.5, 5.0, 7.5],
                    [2.0, 4.0, 6.0], [1.5, 3.0, 4.5], [1.0, 2.0, 3.0], [0.5, 1.0, 1.5], [0.0, 0.0, 0.0]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 19)

    def test_to_tweenvector_length_1(self):
        set_frame_rate(1)
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 1)
        self.assertEqual(len(tween), 1)
        expected = [[5, 10, 15]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_to_tweenvector_length_0(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.to((5, 10, 15), 0)

    def test_ease_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.ease((5, 10, 15), 5, test_linear())
        tween.ease((0, 0, 0), 10, test_linear())
        self.assertEqual(len(tween), 20)
        expected = [[0.5, 1.0, 1.5], [1.0, 2.0, 3.0], [1.5, 3.0, 4.5], [2.0, 4.0, 6.0], [2.5, 5.0, 7.5],
                    [3.0, 6.0, 9.0], [3.5, 7.0, 10.5], [4.0, 8.0, 12.0], [4.5, 9.0, 13.5], [5.0, 10.0, 15.0],
                    [4.5, 9.0, 13.5], [4.0, 8.0, 12.0], [3.5, 7.0, 10.5], [3.0, 6.0, 9.0], [2.5, 5.0, 7.5],
                    [2.0, 4.0, 6.0], [1.5, 3.0, 4.5], [1.0, 2.0, 3.0], [0.5, 1.0, 1.5], [0.0, 0.0, 0.0]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 19)

    def test_ease_d_tweenvector(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.ease_d((5, 10, 15), 5, test_linear())
        tween.ease_d((0, 0, 0), 5, test_linear())
        self.assertEqual(len(tween), 20)
        expected = [[0.5, 1.0, 1.5], [1.0, 2.0, 3.0], [1.5, 3.0, 4.5], [2.0, 4.0, 6.0], [2.5, 5.0, 7.5],
                    [3.0, 6.0, 9.0], [3.5, 7.0, 10.5], [4.0, 8.0, 12.0], [4.5, 9.0, 13.5], [5.0, 10.0, 15.0],
                    [4.5, 9.0, 13.5], [4.0, 8.0, 12.0], [3.5, 7.0, 10.5], [3.0, 6.0, 9.0], [2.5, 5.0, 7.5],
                    [2.0, 4.0, 6.0], [1.5, 3.0, 4.5], [1.0, 2.0, 3.0], [0.5, 1.0, 1.5], [0.0, 0.0, 0.0]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 19)

    def test_ease_tweenvector_length_1(self):
        set_frame_rate(1)
        tween = TweenVector((0, 0, 0))
        tween.ease((5, 10, 15), 1, test_linear())
        self.assertEqual(len(tween), 1)
        expected = [[5, 10, 15]]
        for i, v in enumerate(tween):
            self.assertAlmostEqual(v, expected[i])
        self.assertEqual(i, 0)

    def test_ease_tweenvector_length_0(self):
        set_frame_rate(2)
        tween = TweenVector((0, 0, 0))
        tween.ease((5, 10, 15), 0, test_linear())

    def test_ease_linear(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_linear()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.4, 0.4), (0.5, 0.5),
                                  (0.6, 0.6), (0.7, 0.7), (0.8, 0.8), (0.9, 0.9), (1.0, 1.0)])

    def test_ease_in_harm(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_harm()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.01231165940486223),
                                  (0.2, 0.04894348370484647),
                                  (0.3, 0.10899347581163221),
                                  (0.4, 0.19098300562505255),
                                  (0.5, 0.29289321881345254),
                                  (0.6, 0.41221474770752686),
                                  (0.7, 0.5460095002604533),
                                  (0.8, 0.6909830056250527),
                                  (0.9, 0.8435655349597692),
                                  (1.0, 1.0)])

    def test_ease_out_harm(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_out_harm()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.15643446504023087),
                                  (0.2, 0.3090169943749474),
                                  (0.3, 0.45399049973954675),
                                  (0.4, 0.5877852522924731),
                                  (0.5, 0.7071067811865475),
                                  (0.6, 0.8090169943749475),
                                  (0.7, 0.8910065241883678),
                                  (0.8, 0.9510565162951535),
                                  (0.9, 0.9876883405951378),
                                  (1.0, 1.0)])

    def test_ease_in_out_harm(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_out_harm()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.024471741852423234),
                                  (0.2, 0.09549150281252627),
                                  (0.3, 0.20610737385376343),
                                  (0.4, 0.34549150281252633),
                                  (0.5, 0.5),
                                  (0.6, 0.6545084971874737),
                                  (0.7, 0.7938926261462365),
                                  (0.8, 0.9045084971874737),
                                  (0.9, 0.9755282581475768),
                                  (1.0, 1.0)])

    def test_ease_in_elastic(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_elastic()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.0019290787902248785),
                                  (0.2, 0.0012070976342771387),
                                  (0.3, -0.006960988470221623),
                                  (0.4, -0.009184144567069896),
                                  (0.5, 0.022097086912079605),
                                  (0.6, 0.05056356214843423),
                                  (0.7, -0.056748812467443184),
                                  (0.8, -0.2377641290737885),
                                  (0.9, 0.07821723252011564),
                                  (1.0, 1.0)])

    def test_ease_out_elastic(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_out_elastic()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.9217827674798844),
                                  (0.2, 1.2377641290737884),
                                  (0.3, 1.0567488124674431),
                                  (0.4, 0.9494364378515657),
                                  (0.5, 0.9779029130879204),
                                  (0.6, 1.00918414456707),
                                  (0.7, 1.0069609884702215),
                                  (0.8, 0.9987929023657228),
                                  (0.9, 0.9980709212097751),
                                  (1.0, 1.0)])

    def test_ease_in_out_elastic(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_out_elastic()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.0006035488171385693),
                                  (0.2, -0.004592072283534948),
                                  (0.3, 0.025281781074217115),
                                  (0.4, -0.11888206453689425),
                                  (0.5, 0.5),
                                  (0.6, 1.1188820645368942),
                                  (0.7, 0.9747182189257829),
                                  (0.8, 1.0045920722835349),
                                  (0.9, 0.9993964511828615),
                                  (1.0, 1.0)])

    def test_ease_in_back(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_back()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, -0.02990169943749474),
                                  (0.2, -0.10955705045849462),
                                  (0.3, -0.21570509831248422),
                                  (0.4, -0.3164226065180614),
                                  (0.5, -0.375),
                                  (0.6, -0.3546339097770922),
                                  (0.7, -0.2233118960624632),
                                  (0.8, 0.0417717981660215),
                                  (0.9, 0.45088470506254735),
                                  (1.0, 0.9999999999999999)])

    def test_ease_out_back(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_out_back()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 1.1102230246251565e-16),
                                  (0.1, 0.5491152949374527),
                                  (0.2, 0.9582282018339785),
                                  (0.3, 1.2233118960624632),
                                  (0.4, 1.354633909777092),
                                  (0.5, 1.375),
                                  (0.6, 1.3164226065180613),
                                  (0.7, 1.2157050983124842),
                                  (0.8, 1.1095570504584946),
                                  (0.9, 1.0299016994374948),
                                  (1.0, 1.0)])

    def test_ease_in_out_back(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_out_back()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, -0.05477852522924731),
                                  (0.2, -0.1582113032590307),
                                  (0.3, -0.1773169548885461),
                                  (0.4, 0.02088589908301075),
                                  (0.5, 0.5),
                                  (0.6, 0.9791141009169892),
                                  (0.7, 1.177316954888546),
                                  (0.8, 1.1582113032590307),
                                  (0.9, 1.0547785252292474),
                                  (1.0, 1.0)])

    def test_ease_in_bounce(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_bounce()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, -1.7763568394002505e-15),
                                  (0.1, -1.7763568394002505e-15),
                                  (0.2, 0.08775623268697963),
                                  (0.3, 0.08325000000000093),
                                  (0.4, 0.273000000000001),
                                  (0.5, 0.28125000000000044),
                                  (0.6, 0.10800000000000054),
                                  (0.7, 0.31937499999999985),
                                  (0.8, 0.6975000000000001),
                                  (0.9, 0.9243750000000001),
                                  (1.0, 1.0)])

    def test_ease_out_bounce(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_out_bounce()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, 0.0),
                                  (0.1, 0.07562500000000001),
                                  (0.2, 0.30250000000000005),
                                  (0.3, 0.6806249999999999),
                                  (0.4, 0.8919999999999995),
                                  (0.5, 0.7187499999999996),
                                  (0.6, 0.726999999999999),
                                  (0.7, 0.9167499999999991),
                                  (0.8, 0.9122437673130204),
                                  (0.9, 1.0000000000000018),
                                  (1.0, 1.0000000000000018)])

    def test_ease_in_out_bounce(self):
        set_frame_rate(2)
        ease_function = generativepy.tween.ease_in_out_bounce()
        result = []
        for i in range(11):
            x = i / 10
            result.append((x, ease_function(x)))
        self.assertEqual(result, [(0.0, -8.881784197001252e-16),
                                  (0.1, 0.043878116343489815),
                                  (0.2, 0.1365000000000005),
                                  (0.3, 0.05400000000000027),
                                  (0.4, 0.34875000000000006),
                                  (0.5, 0.5),
                                  (0.6, 0.6512499999999999),
                                  (0.7, 0.946),
                                  (0.8, 0.8634999999999997),
                                  (0.9, 0.9561218836565102),
                                  (1.0, 1.0000000000000009)])

    def test_tween_value_errors(self):
        set_frame_rate(2)
        with self.assertRaises(ValueError):
            tween = Tween("a")
        tween = Tween(0)
        tween.wait(5)
        with self.assertRaises(ValueError):
            tween.wait("a")
        with self.assertRaises(ValueError):
            tween.wait(4)
        with self.assertRaises(ValueError):
            tween.wait_d("a")
        with self.assertRaises(ValueError):
            tween.wait_d(-1)
        with self.assertRaises(ValueError):
            tween.set("a")
        with self.assertRaises(ValueError):
            tween.to("a", 6)
        with self.assertRaises(ValueError):
            tween.to(1, 4)
        with self.assertRaises(ValueError):
            tween.to_d("a", 6)
        with self.assertRaises(ValueError):
            tween.to_d(1, -1)
        with self.assertRaises(ValueError):
            tween.ease("a", 6, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease(1, 4, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease_d("a", 6, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease_d(1, -1, ease_linear)

    def test_tweenvector_value_errors(self):
        set_frame_rate(2)
        with self.assertRaises(ValueError):
            tween = TweenVector(None)
        with self.assertRaises(ValueError):
            tween = TweenVector(1)
        tween = TweenVector((0, 0))
        tween.wait(5)
        with self.assertRaises(ValueError):
            tween.wait("a")
        with self.assertRaises(ValueError):
            tween.wait(4)
        with self.assertRaises(ValueError):
            tween.wait_d("a")
        with self.assertRaises(ValueError):
            tween.wait_d(-1)
        with self.assertRaises(ValueError):
            tween.set("a")
        with self.assertRaises(ValueError):
            tween.to("a", 6)
        with self.assertRaises(ValueError):
            tween.to((1, 1), 4)
        with self.assertRaises(ValueError):
            tween.to_d("a", 6)
        with self.assertRaises(ValueError):
            tween.to_d((1, 1), -1)
        with self.assertRaises(ValueError):
            tween.ease("a", 6, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease((1, 1), 4, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease_d("a", 6, ease_linear)
        with self.assertRaises(ValueError):
            tween.ease_d((1, 1), -1, ease_linear)

