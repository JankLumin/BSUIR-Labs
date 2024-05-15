import Input_data
import math
import numpy as np
from tabulate import tabulate
from statistics import median, mode, variance, stdev
import matplotlib.pyplot as plt


class SequenceAnalyzer:
    def __init__(self, sequence):
        # Initializes the SequenceAnalyzer with a sequence
        self.sequence = sequence

    def calculate_mean(self):
        # Calculates the mean of the sequence
        return sum(self.sequence) / len(self.sequence)

    def calculate_median(self):
        # Calculates the median of the sequence
        return median(self.sequence)

    def calculate_mode(self):
        # Calculates the mode of the sequence
        return mode(self.sequence)

    def calculate_variance(self):
        # Calculates the variance of the sequence
        return variance(self.sequence)

    def calculate_standard_deviation(self):
        # Calculates the variance of the sequence
        return stdev(self.sequence)


def calculate_actual_value(x):
    # Calculates the actual value based on a given input 'x'
    return math.log(1 + x)


class SequenceCalculator(SequenceAnalyzer):
    def __init__(self, max_iterations, eps):
        # Initializes the SequenceCalculator with maximum iterations and epsilon (eps)
        super().__init__([])
        self.max_iterations = max_iterations
        self.eps = eps

    def calculate_sequence(self, x):
        # Calculates the sequence based on a given 'x', maximum iterations, and epsilon (eps)
        result = 0
        n = 1
        term = x
        while abs(term) > self.eps and n <= self.max_iterations:
            result += term
            term *= -x * n / (n + 1)
            self.sequence.append(result)
            n += 1
        return result

    def generate_table(self, x, result, actual_value):
        # Generates a table with calculation results
        table_data = [[x, len(self.sequence), result, actual_value, self.eps]]
        table_headers = ["x", "Итерации", "F(x)", "Математический F(x)", "Точность"]
        table = tabulate(table_data, headers=table_headers, floatfmt=".8f")
        return table


def task3():
    # Main function for Task 3
    max_iterations = 500
    while True:
        x = Input_data.input_data("Введите x: ", float, -1, 1)
        if x == -1:
            print("Ошибка: Значение должно быть больше или равно -1. Пожалуйста, введите корректное значение.")
        elif x == 1:
            print("Ошибка: Значение должно быть меньше или равно 1. Пожалуйста, введите корректное значение.")
        else:
            break
    eps = Input_data.input_data("Введите eps: ", float, None, 1)
    if eps == 1:
        print("Ошибка: Значение должно быть меньше 1. Пожалуйста, введите корректное значение.")

    calculator = SequenceCalculator(max_iterations, eps)
    result = calculator.calculate_sequence(x)
    actual_value = calculate_actual_value(x)
    table = calculator.generate_table(x, result, actual_value)

    print(table)
    print("Среднее арифметическое:", calculator.calculate_mean())
    print("Медиана:", calculator.calculate_median())
    print("Мода:", calculator.calculate_mode())
    print("Дисперсия:", calculator.calculate_variance())
    print("Стандартное отклонение:", calculator.calculate_standard_deviation())

    x_values = np.linspace(0, 1, len(calculator.sequence))
    y_values = calculator.sequence

    plt.plot(x_values, y_values, color="blue", label="Ряд")
    plt.plot(x_values, [calculate_actual_value(x)] * len(calculator.sequence), color="red",
             linestyle="--", label="Математический F(x)")
    plt.xlabel('n')
    plt.ylabel('F(x)')
    plt.legend()
    plt.grid(True)
    plt.title("График разложения функции в ряд")

    plt.savefig("Task3.png")

    plt.show()
