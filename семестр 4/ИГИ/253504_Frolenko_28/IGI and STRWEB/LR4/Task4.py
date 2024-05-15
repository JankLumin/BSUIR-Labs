import math
from abc import ABC, abstractmethod

from matplotlib import pyplot as plt

import Input_data


class GeometricFigure(ABC):
    # Abstract method to calculate the area of a geometric figure
    @abstractmethod
    def calculate_area(self):
        pass


class FigureColor:
    def __init__(self, color):
        # Initialize the color of the figure
        self.color = color

    @property
    def color(self):
        # Getter for the color property
        return self._color

    @color.setter
    def color(self, value):
        # Setter for the color property
        self._color = value


class Pentagon(GeometricFigure):
    _figure_name = "Пятиугольник"

    def __init__(self, color, side):
        # Initialize the pentagon with a color and side length
        self.color = FigureColor(color)
        self.side = side

    @property
    def figure_name(self):
        # Getter for the figure name property
        return self._figure_name

    @figure_name.setter
    def figure_name(self, value):
        # Setter for the figure name property
        self._figure_name = value

    def calculate_area(self):
        # Calculate the area of the pentagon
        return (self.side ** 2) * (5 * math.tan(math.pi / 5)) / 4

    def draw(self):
        # Draw the pentagon using matplotlib
        s = self.side
        x = [s * math.cos(2 * math.pi * i / 5) for i in range(5)]
        y = [s * math.sin(2 * math.pi * i / 5) for i in range(5)]
        if self.color.color == "красный":
            plt.fill(x, y, "red")
        elif self.color.color == "зеленый":
            plt.fill(x, y, "green")
        elif self.color.color == "синий":
            plt.fill(x, y, "blue")
        elif self.color.color == "черный":
            plt.fill(x, y, "black")
        elif self.color.color == "желтый":
            plt.fill(x, y, "yellow")
        plt.axis("equal")
        plt.xlim(min(x) - s, max(x) + s)
        plt.ylim(min(y) - s, max(y) + s)
        plt.text(0, -s - 4, self.figure_name, ha="center")
        plt.savefig("figure.png")

        plt.show()

    def __str__(self):
        # String representation of the pentagon
        return "{} со стороной {} единиц, цвет: {}, площадь: {:.2f} кв.ед.".format(
            self.figure_name, self.side, self.color.color, self.calculate_area()
        )


def task4():
    # Get the name, side length, and color of the figure from the user
    name = Input_data.input_data("Введите название фигуры: ", str)
    side = Input_data.input_data("Введите размер стороны: ", float)
    allowed_colors = ["красный", "зеленый", "синий", "черный", "желтый"]
    color = Input_data.input_data("Введите цвет фигуры(красный, зеленый, синий, черный, желтый): ", str)
    while color.lower() not in allowed_colors:
        print("Недопустимый цвет! Попробуйте снова.")
        color = Input_data.input_data("Введите цвет фигуры(красный, зеленый, синий, черный, желтый): ", str)
    pentagon = Pentagon(color, side)
    pentagon.figure_name = name
    print(pentagon)
    pentagon.draw()
