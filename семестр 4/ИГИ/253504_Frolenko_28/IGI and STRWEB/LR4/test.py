import math
import unittest
from Task4 import Pentagon


class PentagonTestCase(unittest.TestCase):
    def test_calculate_area(self):
        pentagon = Pentagon("красный", 5)
        expected_area = (5 ** 2) * (5 * math.tan(math.pi / 5)) / 4
        self.assertEqual(pentagon.calculate_area(), expected_area)

    def test_draw(self):
        pentagon = Pentagon("красный", 5)
        self.assertIsNone(pentagon.draw())

    def test_figure_name(self):
        pentagon = Pentagon("красный", 5)
        pentagon.figure_name = "Мой пятиугольник"
        self.assertEqual(pentagon.figure_name, "Мой пятиугольник")

    def test_str(self):
        pentagon = Pentagon("красный", 5)
        pentagon.figure_name = "Мой пятиугольник"
        expected_str = "Мой пятиугольник со стороной 5 единиц, цвет: красный, площадь: 22.70 кв.ед."
        self.assertEqual(str(pentagon), expected_str)


if __name__ == '__main__':
    unittest.main()
