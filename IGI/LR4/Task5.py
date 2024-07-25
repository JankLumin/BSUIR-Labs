import numpy as np
import Input_data


class Matrix:
    def __init__(self, rows, columns):
        # Initialize the matrix with the given number of rows and columns
        self.rows = rows
        self.columns = columns
        self.data = np.empty((rows, columns))

    def fill_random(self):
        # Fill the matrix with random integers between -100 and 100
        self.data = np.random.randint(-100, 100, size=(self.rows, self.columns))

    def display(self):
        # Display the matrix
        print(self.data)


class IntegerMatrix(Matrix):
    def __init__(self, rows, columns):
        # Initialize the integer matrix with the given number of rows and columns
        super().__init__(rows, columns)
        self.data = np.empty((rows, columns), dtype=int)

    def divide_by_max_abs(self):
        # Divide all elements of the matrix by the maximum absolute value in the matrix
        max_value = np.max(self.data)
        min_value = np.min(self.data)
        if abs(max_value) < abs(min_value):
            max_value = min_value
        self.data = np.divide(self.data, max_value)

    def math_variance(self):
        # Calculate the variance of the matrix using numpy
        variance = round(np.var(self.data), 2)
        return variance

    def custom_variance(self):
        # Calculate the variance of the matrix using the formula
        mean = np.mean(self.data)
        squared_diff = np.mean((self.data - mean) ** 2)
        variance = round(squared_diff, 2)
        return variance


def task5():
    # Get the number of rows and columns for the matrix from the user
    m = Input_data.input_data("Введите количество столбцов матрицы: ", int, 1, 10000)
    n = Input_data.input_data("Введите количество строк матрицы: ", int, 1, 10000)

    integer_matrix = IntegerMatrix(m, n)
    integer_matrix.fill_random()
    print("Исходная матрица:")
    integer_matrix.display()
    integer_matrix.divide_by_max_abs()
    print()
    print("Матрица деленная на максимальный элемент по модулю:")
    integer_matrix.display()
    print()
    print("Дисперсия с помощью numpy:")
    print(integer_matrix.math_variance())
    print()
    print("Дисперсия с помощью формулы:")
    print(integer_matrix.custom_variance())
