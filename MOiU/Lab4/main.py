import numpy as np


def clean_matrix(matrix):
    """
    Заменяет значения, близкие к нулю, на 0.0 для лучшей читаемости.
    """
    cleaned = matrix.copy()
    cleaned[np.isclose(cleaned, 0.0)] = 0.0
    return cleaned


def dual_simplex_method(c, A, b, B_initial):
    """
    Реализует двойственный симплекс-метод.
    """
    m, n = A.shape
    # Преобразуем базис, введённый пользователем (от 1 до n), в индексы 0...n-1.
    B = [idx - 1 for idx in B_initial]
    iteration = 1

    while True:
        print("\n" + "=" * 50)
        print(f"Итерация {iteration}")
        print("=" * 50)
        # Шаг 1: формируем базисную матрицу и вычисляем её обратную
        A_B = A[:, B]
        try:
            A_B_inv = np.linalg.inv(A_B)
        except np.linalg.LinAlgError:
            print("Ошибка: базисная матрица вырождена, метод не может быть применён.")
            return None

        print("\nШаг 1. Вычисляем базисную матрицу A_B и её обратную:")
        print("Базисные индексы B: ", [i + 1 for i in B])
        print("A_B =\n", clean_matrix(A_B))
        print("A_B⁻¹ =\n", clean_matrix(A_B_inv))

        # Шаг 2: вычисляем вектор c_B и план двойственной задачи y, где y^T = c_B^T * A_B⁻¹.
        c_B = c[B]
        # Вычисляем y так: y^T = c_B^T * A_B_inv, т.е. y = (A_B_inv)^T * c_B.
        y = A_B_inv.T @ c_B
        print("\nШаг 2. Вычисляем план двойственной задачи y:")
        print("c_B =", c_B)
        print("y^T = c_B^T * A_B⁻¹ =", y)

        # Шаг 3: вычисляем псевдоплан κ:
        #   κ_B = A_B⁻¹ * b, а компоненты, не входящие в базис, равны 0.
        kappa_B = A_B_inv @ b
        kappa = np.zeros(n)
        for i, bi in enumerate(B):
            kappa[bi] = kappa_B[i]
        print("\nШаг 3. Вычисляем псевдоплан κ:")
        print("κ_B = A_B⁻¹ * b =", kappa_B)
        print("Псевдоплан κ (все компоненты):\n", kappa)

        # Шаг 4: проверяем, неотрицателен ли псевдоплан
        if np.all(kappa >= -1e-10):
            print(
                "\nВсе компоненты псевдоплана неотрицательны. Оптимальный план найден."
            )
            return kappa  # оптимальное решение прямой задачи
        else:
            # Шаг 5: выбираем отрицательную компоненту псевдоплана.
            # Выбираем первый элемент из κ_B, который меньше 0.
            negative_indices = [i for i in range(m) if kappa_B[i] < -1e-10]
            if not negative_indices:
                print(
                    "Ошибка: отрицательная компонента не найдена, хотя условие не выполнено."
                )
                return None
            k_index = negative_indices[0]
            j_k = B[k_index]
            print(
                f"\nШаг 4. Выбираем отрицательную компоненту псевдоплана: κ[{j_k + 1}] = {kappa[j_k]}"
            )

            # Шаг 6: вычисляем вектор Δy – k_index-я строка матрицы A_B⁻¹.
            delta_y = A_B_inv[k_index, :]
            print("\nШаг 5. Вычисляем вектор Δy (строка A_B⁻¹ с индексом k):")
            print("Δy =", delta_y)

            # Шаг 7: для каждого j, не входящего в базис, вычисляем µ_j = Δy^T * A[:, j].
            nonbasic_indices = [j for j in range(n) if j not in B]
            mu = {}
            print("\nШаг 6. Вычисляем µ_j для j ∉ B:")
            for j in nonbasic_indices:
                mu_j = delta_y @ A[:, j]
                mu[j] = mu_j
                print(f"µ[{j + 1}] = Δy^T * A[:, {j + 1}] = {mu_j}")

            # Шаг 8: если для всех не базисных переменных µ_j ≥ 0, то прямая задача не совместна.
            if all(mu[j] >= -1e-10 for j in mu):
                print("\nДля всех j вне базиса µ[j] ≥ 0 → прямая задача не совместна.")
                return None

            # Шаг 9: для каждого j с µ_j < 0 вычисляем
            #         σ_j = (c[j] - A[:, j]^T * y) / µ_j.
            sigma = {}
            print("\nШаг 7. Вычисляем σ_j для j с µ[j] < 0:")
            for j in nonbasic_indices:
                if mu[j] < -1e-10:
                    numerator = c[j] - (A[:, j] @ y)
                    sigma_j = numerator / mu[j]
                    sigma[j] = sigma_j
                    print(
                        f"σ[{j + 1}] = (c[{j + 1}] - A[:, {j + 1}]^T * y) / µ[{j + 1}] = {sigma_j}"
                    )

            # Шаг 10: выбираем j₀, при котором σ_j минимально.
            j0, sigma0 = min(sigma.items(), key=lambda item: item[1])
            print(
                f"\nШаг 8. Выбираем j₀ с минимальным σ: σ₀ = {sigma0} при j₀ = {j0 + 1}"
            )

            # Шаг 11: обновляем базис, заменяя в нем индекс j_k на j₀.
            print(
                f"\nШаг 9. Обновляем базис: заменяем базисный индекс {j_k + 1} на {j0 + 1}."
            )
            B[k_index] = j0
            print("Новый базис B:", [i + 1 for i in B])

            iteration += 1


def get_input_data():
    """
    Считывает входные данные задачи линейного программирования:
      - m: число ограничений,
      - n: число переменных,
      - вектор c,
      - матрицу A,
      - вектор правых частей b,
      - начальный базис B (индексы от 1 до n, размер равен числу ограничений m).
    """
    print("Входные данные для задачи линейного программирования:")
    try:
        m = int(input("Введите количество ограничений (m): "))
        n = int(input("Введите количество переменных (n): "))
    except ValueError:
        print("Ошибка ввода: введите целые числа для m и n.")
        exit(1)

    print(f"\nВведите вектор c (размер {n}):")
    c_input = input("c: ").strip().split()
    if len(c_input) != n:
        print("Ошибка: количество элементов в векторе c не соответствует n.")
        exit(1)
    c = np.array([float(num) for num in c_input], dtype=float)

    print(f"\nВведите матрицу A (размер {m}x{n}):")
    A = []
    for i in range(m):
        row_input = input(f"Строка {i + 1}: ").strip().split()
        if len(row_input) != n:
            print("Ошибка: количество элементов в строке не соответствует n.")
            exit(1)
        A.append([float(num) for num in row_input])
    A = np.array(A, dtype=float)

    print(f"\nВведите вектор правых частей b (размер {m}):")
    b_input = input("b: ").strip().split()
    if len(b_input) != m:
        print("Ошибка: количество элементов в векторе b не соответствует m.")
        exit(1)
    b = np.array([float(num) for num in b_input], dtype=float)

    print(f"\nВведите начальный базис B (размер {m}, индексы от 1 до {n}):")
    B_input = input("B (индексы через пробел): ").strip().split()
    if len(B_input) != m:
        print(
            "Ошибка: количество базисных индексов не соответствует числу ограничений m."
        )
        exit(1)
    B_initial = [int(idx) for idx in B_input]
    if any(j < 1 or j > n for j in B_initial):
        print("Ошибка: базисные индексы должны быть в диапазоне от 1 до n.")
        exit(1)

    return c, A, b, B_initial


def main():
    c, A, b, B_initial = get_input_data()
    print("\n=== Начало работы двойственного симплекс-метода ===")
    optimal_plan = dual_simplex_method(c, A, b, B_initial)

    if optimal_plan is not None:
        print("\nОптимальный план прямой задачи (псевдоплан κ):")
        for i, val in enumerate(optimal_plan):
            print(f"x[{i + 1}] = {val}")
    else:
        print("\nПрямая задача не совместна (нет допустимого плана).")


if __name__ == "__main__":
    main()
