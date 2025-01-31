import numpy as np


def clean_matrix(matrix):
    """Заменяет значения, близкие к нулю, на 0.0 для лучшей читаемости."""
    cleaned = matrix.copy()
    cleaned[np.isclose(cleaned, 0.0)] = 0.0
    return cleaned


def print_iteration(
    iteration,
    AB,
    AB_inv,
    cB,
    u,
    delta,
    j0=None,
    z=None,
    theta=None,
    theta0=None,
    k=None,
    j_star=None,
    B_new=None,
    x_new=None,
):
    """Выводит информацию об итерации."""
    print(f"\n{'-'*40}\nИтерация {iteration}\n{'-'*40}")
    print("Базисная матрица AB:")
    print(clean_matrix(AB))
    print("\nОбратная матрица AB⁻¹:")
    print(clean_matrix(AB_inv))
    print(f"\nВектор cB: {cB}")
    print(f"\nВектор потенциалов u: {u}")
    print(f"\nВектор оценок Δ: {delta}")

    if j0 is not None:
        print(f"\nВходящая переменная j₀: {j0 + 1}")
    if z is not None:
        print(f"Вектор z: {z}")
    if theta is not None:
        print(f"Вектор θ: {theta}")
    if theta0 is not None:
        print(f"θ₀ = {theta0}")
    if k is not None and j_star is not None:
        print(f"Покидающая переменная k: {k + 1}")
        print(f"j* = {j_star + 1}")
    if B_new is not None:
        B_new_int = [int(b + 1) for b in B_new]
        print(f"Новый базис B: {B_new_int}")
    if x_new is not None:
        print(f"Новый план x: {x_new}")


def simplex_main_phase(c, A, x_initial, B_initial):
    """Основная фаза симплекс-метода."""
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    x = np.array(x_initial, dtype=float)
    B = [b_idx - 1 for b_idx in B_initial]
    m, n = A.shape
    iteration = 1

    AB = A[:, B]
    x_B = x[B]
    b = AB @ x_B

    while True:
        AB = A[:, B]
        try:
            AB_inv = np.linalg.inv(AB)
        except np.linalg.LinAlgError:
            print("AB необратима. Завершение метода.")
            return None

        cB = c[B]
        u = cB @ AB_inv
        delta = u @ A - c

        if np.all(delta >= -1e-10):
            print_iteration(
                iteration,
                AB,
                AB_inv,
                cB,
                u,
                delta,
                j0=None,
                z=None,
                theta=None,
                theta0=None,
                k=None,
                j_star=None,
                B_new=None,
                x_new=None,
            )
            return x

        j0_candidates = np.where(delta < -1e-10)[0]
        if len(j0_candidates) == 0:
            print_iteration(
                iteration,
                AB,
                AB_inv,
                cB,
                u,
                delta,
                j0=None,
                z=None,
                theta=None,
                theta0=None,
                k=None,
                j_star=None,
                B_new=None,
                x_new=None,
            )
            return x
        j0 = j0_candidates[0]

        Aj0 = A[:, j0]
        z = AB_inv @ Aj0

        theta = np.array([x[B[i]] / z[i] if z[i] > 1e-10 else np.inf for i in range(m)])
        theta0 = np.min(theta)

        if theta0 == np.inf:
            print("\nФункция не ограничена сверху.")
            return None

        k = np.where(theta == theta0)[0][0]
        j_star = B[k]
        B_new = B.copy()
        B_new[k] = j0

        x_new = x.copy()
        x_new[j0] = theta0
        for i in range(m):
            if i != k:
                x_new[B[i]] -= theta0 * z[i]
        x_new[j_star] = 0

        print_iteration(
            iteration,
            AB,
            AB_inv,
            cB,
            u,
            delta,
            j0,
            z,
            theta,
            theta0,
            k,
            j_star,
            B_new,
            x_new,
        )

        B = B_new
        x = x_new
        iteration += 1


def get_input(prompt, type_func, condition=lambda x: True, error_msg="Неверный ввод."):
    """Универсальная функция для считывания и проверки ввода."""
    while True:
        try:
            value = type_func(input(prompt))
            if not condition(value):
                print(error_msg)
                continue
            return value
        except ValueError:
            print(error_msg)


def get_vector(prompt, length, type_func=float):
    """Считывает вектор из консоли."""
    while True:
        try:
            values = input(prompt).strip().split()
            if len(values) != length:
                print(f"Необходимо ввести ровно {length} элементов.")
                continue
            vector = [type_func(val) for val in values]
            return vector
        except ValueError:
            print("Необходимо ввести числовые значения.")


def main():

    n = get_input(
        "Введите количество переменных (n): ",
        int,
        lambda x: x > 0,
        "Введите положительное целое число.",
    )
    m = get_input(
        "Введите количество ограничений (m): ",
        int,
        lambda x: x > 0,
        "Введите положительное целое число.",
    )

    print(f"\nВведите вектор c (размер {n}):")
    c = get_vector("c: ", n)

    print(f"\nВведите матрицу A (размер {m}x{n}):")
    A = []
    for i in range(1, m + 1):
        row = get_vector(f"A[{i}]: ", n)
        A.append(row)

    print(f"\nВведите начальный допустимый план x (размер {n}):")
    x_initial = get_vector("x: ", n)

    print(f"\nВведите начальный базис B (размер {m}, индексы от 1 до {n}):")
    while True:
        B_initial = get_vector("B: ", m, int)
        if all(1 <= idx <= n for idx in B_initial) and len(set(B_initial)) == m:
            break
        else:
            print("Индексы должны быть уникальными и в диапазоне от 1 до n.")

    print("\nИсходные данные:")
    print(f"Целевая функция: {c}")
    print("\nМатрица A:")
    A = np.array(A)
    print(A)
    print(f"\nНачальный план x: {x_initial}")
    print(f"Начальный базис B: {B_initial}")

    optimal_x = simplex_main_phase(c, A, x_initial, B_initial)

    if optimal_x is not None:
        if np.all(np.mod(optimal_x, 1) == 0):
            optimal_x = optimal_x.astype(int)
        print("\nОптимальный план:")
        print(optimal_x)
    else:
        print("\nОптимальный план отсутствует или функция не ограничена.")


if __name__ == "__main__":
    main()
