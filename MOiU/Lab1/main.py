import numpy as np

def get_input_data():
    """
    Считывание входных данных из консоли: матрица A, её обратная A_inv, вектор x и индекс столбца i.
    """
    try:
        n = int(input("Введите размерность квадратных матриц (n): "))
        if n <= 0:
            raise ValueError("Размерность должна быть положительным целым числом.")

        print(f"\nВведите элементы матрицы A по строкам, разделяя элементы пробелами (размер {n}x{n}):")
        A = []
        for row in range(1, n+1):
            while True:
                row_input = input(f"Строка {row}: ").strip().split()
                if len(row_input) != n:
                    print(f"Ошибка: необходимо ввести ровно {n} элементов.")
                else:
                    try:
                        A.append([float(num) for num in row_input])
                        break
                    except ValueError:
                        print("Ошибка: введите числовые значения.")
        A = np.array(A, dtype=float)

        print(f"\nВведите элементы обратной матрицы A⁻¹ по строкам, разделяя элементы пробелами (размер {n}x{n}):")
        A_inv = []
        for row in range(1, n+1):
            while True:
                row_input = input(f"Строка {row}: ").strip().split()
                if len(row_input) != n:
                    print(f"Ошибка: необходимо ввести ровно {n} элементов.")
                else:
                    try:
                        A_inv.append([float(num) for num in row_input])
                        break
                    except ValueError:
                        print("Ошибка: введите числовые значения.")
        A_inv = np.array(A_inv, dtype=float)

        print(f"\nВведите элементы вектора x, разделяя элементы пробелами (размер {n}):")
        while True:
            x_input = input("x: ").strip().split()
            if len(x_input) != n:
                print(f"Ошибка: необходимо ввести ровно {n} элементов.")
            else:
                try:
                    x = np.array([float(num) for num in x_input], dtype=float)
                    break
                except ValueError:
                    print("Ошибка: введите числовые значения.")

        while True:
            i_input = input(f"\nВведите индекс столбца для замены (от 1 до {n}): ").strip()
            try:
                i = int(i_input)
                if 1 <= i <= n:
                    break
                else:
                    print(f"Ошибка: индекс должен быть от 1 до {n}.")
            except ValueError:
                print("Ошибка: введите целое число.")

        return A_inv, A, x, i

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
        exit(1)

def clean_matrix(matrix):
    """
    Заменяет -0.0 на 0.0 для улучшения читаемости.
    """
    cleaned = matrix.copy()
    cleaned[np.isclose(cleaned, 0.0)] = 0.0
    return cleaned

def compute_inverse(A_inv, A, x, i):
    """
    Реализует алгоритм вычисления обратной матрицы A'.
    Возвращает (A')⁻¹, матрицу Q и матрицу A'.
    """
    n = A.shape[0]

    print("Шаг 0: Задание исходных данных")
    print(f"Исходная матрица A:\n{clean_matrix(A)}\n")
    print(f"Обратная матрица A⁻¹:\n{clean_matrix(A_inv)}\n")
    print(f"Вектор x:\n{clean_matrix(x.reshape(-1,1))}\n")
    print(f"Индекс столбца для замены: {i}\n")

    print("Шаг 1: Формируем матрицу A', заменяя i-й столбец на x")
    A_prime = A.copy()
    A_prime[:, i-1] = x
    print(f"A' =\n{clean_matrix(A_prime)}\n")

    print("Шаг 2: Вычисляем вектор ℓ = A⁻¹ * x")
    print(f"Матрица A⁻¹:\n{clean_matrix(A_inv)}\n")
    print(f"Вектор x:\n{clean_matrix(x.reshape(-1,1))}\n")
    l = A_inv @ x
    print(f"ℓ = A⁻¹ * x =\n{clean_matrix(l.reshape(-1,1))}\n")

    if l[i-1] == 0:
        print(f"Поскольку ℓ[{i}] = {l[i-1]} = 0, матрица A' необратима.\n")
        return None, None, None

    print(f"Поскольку ℓ[{i}] = {l[i-1]} ≠ 0, матрица A' обратима.\n")

    print("Шаг 3: Формируем вектор ℓₑ, заменяя i-й элемент на -1")
    l_e = l.copy()
    l_e[i-1] = -1
    print(f"ℓₑ =\n{clean_matrix(l_e.reshape(-1,1))}\n")

    print("Шаг 4: Вычисляем вектор ℓ_b = -1 / ℓ[i] * ℓₑ")
    l_b = (-1 / l[i-1]) * l_e
    print(f"ℓ_b = -1 / ℓ[{i}] * ℓₑ =\n{clean_matrix(l_b.reshape(-1,1))}\n")

    print("Шаг 5: Формируем матрицу Q, заменяя i-й столбец на ℓ_b")
    Q = np.identity(n)
    Q[:, i-1] = l_b
    print(f"Матрица Q:\n{clean_matrix(Q)}\n")

    print("Шаг 6: Вычисляем (A')⁻¹ = Q * A⁻¹")
    A_inv_new = Q @ A_inv
    print(f"(A')⁻¹ = Q * A⁻¹ =\n{clean_matrix(A_inv_new)}\n")

    return A_inv_new, Q, A_prime

def main():
    try:
        A_inv, A, x, i = get_input_data()
        A_inv_new, Q, A_prime = compute_inverse(A_inv, A, x, i)
        if A_inv_new is not None:
            print("Итоговая обратная матрица (A')⁻¹:")
            print(clean_matrix(A_inv_new))
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
