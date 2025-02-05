import numpy as np


def clean_matrix(matrix):
    """Заменяет значения, близкие к нулю, на 0.0 для лучшей читаемости."""
    cleaned = matrix.copy()
    cleaned[np.isclose(cleaned, 0.0)] = 0.0
    return cleaned


def print_iteration(
    phase,
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
    """Выводит информацию об итерации симплекс-метода."""
    print(f"\n{phase}. Итерация {iteration}")
    print("-" * 40)
    print("Базисная матрица:")
    print(clean_matrix(AB))
    print("\nОбратная матрица:")
    print(clean_matrix(AB_inv))
    print("\ncB: ", cB)
    print("u:  ", u)
    print("Δ:  ", delta)
    if j0 is not None:
        print(f"\nВходящая переменная: {j0 + 1}")
    if z is not None:
        print(f"z: {clean_matrix(z.reshape(-1, 1))}")
    if theta is not None:
        print(f"θ: {theta}")
    if theta0 is not None:
        print(f"θ₀: {theta0}")
    if k is not None and j_star is not None:
        print(f"Покидающая переменная: {k + 1} (j*: {j_star + 1})")
    if B_new is not None:
        B_new_int = [int(b) + 1 for b in B_new]
        print(f"Новый базис: {B_new_int}")
    if x_new is not None:
        print(f"Новый план: {x_new}")
    print("-" * 40)


def simplex_main_phase_with_basis(
    c, A, x_initial, B_initial, phase_label="Основная фаза"
):
    """
    Основная фаза симплекс-метода с подробным выводом.
    """
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    x = np.array(x_initial, dtype=float)
    B = [b_idx - 1 for b_idx in B_initial]
    m, n = A.shape
    iteration = 1

    while True:
        AB = A[:, B]
        try:
            AB_inv = np.linalg.inv(AB)
        except np.linalg.LinAlgError:
            print("Ошибка: Базисная матрица AB необратима.")
            return None, None, None

        cB = c[B]
        u = cB @ AB_inv
        delta = u @ A - c

        print_iteration(phase_label, iteration, AB, AB_inv, cB, u, delta)

        if np.all(delta >= -1e-10):
            return x, B, AB_inv

        j0_candidates = np.where(delta < -1e-10)[0]
        if len(j0_candidates) == 0:
            return x, B, AB_inv

        j0 = j0_candidates[0]
        Aj0 = A[:, j0]
        z = AB_inv @ Aj0

        theta = [x[B[i]] / z[i] if z[i] > 1e-10 else np.inf for i in range(m)]
        theta0 = np.min(theta)
        if theta0 == np.inf:
            print("Ошибка: Функция не ограничена.")
            return None, None, None

        k = np.where(np.array(theta) == theta0)[0][0]
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
            phase_label,
            iteration,
            AB,
            AB_inv,
            cB,
            u,
            delta,
            j0=j0,
            z=z,
            theta=theta,
            theta0=theta0,
            k=k,
            j_star=j_star,
            B_new=B_new,
            x_new=x_new,
        )

        B = B_new
        x = x_new
        iteration += 1


def simplex_initial_phase(c, A, b):
    """
    Начальная фаза симплекс-метода.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    m, n = A.shape

    for i in range(m):
        if b[i] < 0:
            A[i, :] = -A[i, :]
            b[i] = -b[i]

    print("\n=== Приведение b к неотрицательному виду ===")
    print("A:")
    print(clean_matrix(A))
    print("b:")
    print(b)

    c_aux = np.hstack((np.zeros(n), -np.ones(m)))
    A_e = np.hstack((A, np.eye(m)))
    x_e_initial = np.concatenate((np.zeros(n), b))
    B_aux_initial = [i for i in range(n + 1, n + m + 1)]

    print("\n=== Формирование вспомогательной задачи ===")
    print("ec:")
    print(c_aux)
    print("Aₑ:")
    print(clean_matrix(A_e))
    print("xₑ:")
    print(x_e_initial)
    print("Bₑ:")
    print(B_aux_initial)

    print("\n=== Решение вспомогательной задачи ===")
    x_e_opt, B_aux, AB_inv = simplex_main_phase_with_basis(
        c_aux, A_e, x_e_initial, B_aux_initial, phase_label="Вспомогательная фаза"
    )
    if x_e_opt is None:
        print("Вспомогательная задача не имеет решения.")
        return None, None, None, None, None

    print("\nОптимальное решение вспомогательной задачи:")
    print("xₑ:")
    print(x_e_opt)
    print("Bₑ:")
    print([int(b) + 1 for b in B_aux])

    artificial_values = x_e_opt[n:]
    if not np.all(np.abs(artificial_values) < 1e-8):
        print(
            "\nОшибка: Искусственные переменные не обнулились. Допустимых планов нет."
        )
        return None, None, None, None, None

    x = x_e_opt[:n]
    print("\nДопустимый план для исходной задачи:")
    print("x:")
    print(x)

    while any(b_idx >= n for b_idx in B_aux):
        artificial_in_B = [b_idx for b_idx in B_aux if b_idx >= n]
        j_k = max(artificial_in_B)
        k = B_aux.index(j_k)
        i_row = j_k - n
        print(
            f"\nКорректировка: обнаружен искусственный базисный индекс {j_k + 1} (ограничение {i_row + 1})."
        )
        replaced = False
        for j in range(n):
            if j in B_aux:
                continue
            l_j = AB_inv @ A_e[:, j]
            if not np.isclose(l_j[k], 0.0):
                print(f"  Заменяем {j_k + 1} на {j + 1} (ℓ(j))[{k + 1}] = {l_j[k]:.4f}")
                B_aux[k] = j
                AB = A_e[:, B_aux]
                try:
                    AB_inv = np.linalg.inv(AB)
                except np.linalg.LinAlgError:
                    print("Ошибка: Базис после замены оказался необратим.")
                    return None, None, None, None, None
                replaced = True
                break
        if not replaced:
            print(
                f"  Все j ∉ B удовлетворяют условию (ℓ(j))[{k + 1}] = 0. Удаляем ограничение {i_row + 1}."
            )
            A = np.delete(A, i_row, axis=0)
            b = np.delete(b, i_row, axis=0)
            A_e = np.delete(A_e, i_row, axis=0)
            m -= 1
            del B_aux[k]
            if len(B_aux) > 0:
                AB = A_e[:, B_aux]
                try:
                    AB_inv = np.linalg.inv(AB)
                except np.linalg.LinAlgError:
                    print("Ошибка: Базис после удаления ограничений необратим.")
                    return None, None, None, None, None
            print("  Обновлённая матрица A:")
            print(clean_matrix(A))
            print("  Обновлённый вектор b:")
            print(b)
            print("  Новый базис Bₑ:")
            print([int(b) + 1 for b in B_aux])

    if m == 1 and np.isclose(b[0], 0.0):
        print("\nКорректировка: b[0] = 1")
        b[0] = 1

    B_final = [int(b_idx) + 1 for b_idx in B_aux]
    print("\n=== Итоговый результат начальной фазы ===")
    print("x:")
    print(x)
    print("B:")
    print(B_final)

    return x, B_aux, A, b, A_e


def get_input(prompt, type_func, condition=lambda x: True, error_msg="Неверный ввод."):
    """Универсальная функция ввода с проверкой корректности."""
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
                print(f"Введите ровно {length} элементов.")
                continue
            return [type_func(val) for val in values]
        except ValueError:
            print("Введите числовые значения.")


def get_matrix(prompt, m, n):
    """Считывает матрицу из консоли построчно."""
    print(prompt)
    matrix = []
    for i in range(1, m + 1):
        row = get_vector(f"Строка {i}: ", n)
        matrix.append(row)
    return matrix


def main():
    print("Входные данные для задачи линейного программирования:")
    n = get_input("Количество переменных (n): ", int, lambda x: x > 0)
    m = get_input("Количество ограничений (m): ", int, lambda x: x > 0)

    print(f"\nВведите вектор c (размер {n}):")
    c = get_vector("c: ", n)

    A = get_matrix(f"\nВведите матрицу A (размер {m}x{n}):", m, n)

    print(f"\nВведите вектор правых частей b (размер {m}):")
    b = get_vector("b: ", m)

    print("\nИсходные данные:")
    print("c:", c)
    print("A:")
    print(np.array(A))
    print("b:", b)

    result = simplex_initial_phase(c, A, b)
    if result[0] is None:
        print("\nДопустимых планов нет.")
    else:
        x, B, A_new, b_new, A_e_new = result
        B_print = [int(idx) + 1 for idx in B]
        print("\n=== Результат начальной фазы ===")
        print("x:", x)
        print("B:", B_print)
        print("A:")
        print(clean_matrix(A_new))
        print("b:", b_new)


if __name__ == "__main__":
    main()
