import numpy as np
from numpy.linalg import inv


def get_input_data_qp():
    """
    Считывает исходные данные для задачи квадратичного программирования
    """
    try:
        n = int(input("Введите число переменных (n): "))
        m = int(input("Введите число ограничений (m): "))
    except ValueError:
        print("Ошибка ввода: введите целые числа для n и m.")
        exit(1)

    print(f"\nВведите вектор c (размер {n}):")
    c_input = input("c: ").strip().split()
    if len(c_input) != n:
        print("Ошибка: количество элементов в векторе c не соответствует n.")
        exit(1)
    c = np.array([float(num) for num in c_input], dtype=float)

    print(f"\nВведите матрицу D (размер {n}x{n}):")
    D_list = []
    for i in range(n):
        row_input = input(f"Строка {i+1}: ").strip().split()
        if len(row_input) != n:
            print("Ошибка: количество элементов в строке не соответствует n.")
            exit(1)
        D_list.append([float(num) for num in row_input])
    D = np.array(D_list, dtype=float)

    print(f"\nВведите матрицу A (размер {m}x{n}):")
    A_list = []
    for i in range(m):
        row_input = input(f"Строка {i+1}: ").strip().split()
        if len(row_input) != n:
            print("Ошибка: количество элементов в строке не соответствует n.")
            exit(1)
        A_list.append([float(num) for num in row_input])
    A = np.array(A_list, dtype=float)

    print(f"\nВведите начальный план x (размер {n}):")
    x_input = input("x: ").strip().split()
    if len(x_input) != n:
        print("Ошибка: количество элементов в векторе x не соответствует n.")
        exit(1)
    x = np.array([float(num) for num in x_input], dtype=float)

    print("\nВведите базисные индексы Jb (через пробел, в 1‑индексированном виде):")
    Jb_input = input("Jb: ").strip().split()
    if len(Jb_input) == 0:
        print("Ошибка: базис не задан.")
        exit(1)
    Jb = [int(num) for num in Jb_input]

    print(
        "\nВведите индексы расширенной опоры Jb⁺ (через пробел, в 1‑индексированном виде):"
    )
    Jb_ext_input = input("Jb⁺: ").strip().split()
    if len(Jb_ext_input) == 0:
        print("Ошибка: расширенная опора не задана.")
        exit(1)
    Jb_ext = [int(num) for num in Jb_ext_input]

    # Вычисляем вектор правых частей b = A*x
    b = A.dot(x)

    return c, D, A, b, x, Jb, Jb_ext


def qp_method(c, D, A, b, x, Jb, Jb_ext, tol=1e-10, max_iter=10):
    """
    Реализует итерационный метод решения задачи квадратичного программирования:
        min { cᵀx + 1/2 * xᵀDx }
         s.t. A x = b,  x >= 0
    Исходный план x, базис Jb и расширенная опора Jb⁺ задаются в 1‑индексированном виде.
    Для работы с массивами используется 0‑индексированный вариант.
    """
    # Преобразуем базис и расширенную опору в 0‑индексированный вариант:
    Jb_py = [j - 1 for j in Jb]
    Jb_ext_py = [j - 1 for j in Jb_ext]

    print("\nИсходный план x⁰ =", x)
    print("Начальный базис Jb =", Jb)
    print("Начальная расширенная опора Jb⁺ =", Jb_ext)
    print("Вектор правых частей b =", b)

    iter_num = 1
    n = len(x)
    while iter_num <= max_iter:
        print("\n" + "=" * 50)
        print(f"Итерация {iter_num}")
        print("=" * 50)

        # ШАГ 1. Вычисляем c(x) = c + D*x
        cx = c + D.dot(x)
        print("\nc(x) = c + D*x =\n", cx)

        # ШАГ 2. Вычисляем двойственные переменные для базиса:
        A_B = A[:, Jb_py]
        cB = cx[Jb_py]
        u0 = -np.dot(cB, inv(A_B))
        print("\nu⁰(x) = -c_B(x) * (A_B)⁻¹ =\n", u0)

        # ШАГ 3. Вычисляем вектор оптимальности Δ(x) = u⁰(x)*A + c(x)
        Delta = np.dot(u0, A) + cx
        print("\nΔ(x) = u⁰(x)*A + c(x) =\n", Delta)

        # Если все компоненты Δ(x) >= 0, алгоритм завершает работу.
        if np.all(Delta >= -tol):
            print("\nОптимальность достигнута. Оптимальный план x* =", x)
            return x

        # ШАГ 4. Выбираем отрицательную компоненту Δ(x).
        j0_candidates = [j for j, d in enumerate(Delta) if d < -tol]
        if not j0_candidates:
            print("Все компоненты Δ(x) неотрицательны. Алгоритм завершён.")
            return x
        j0 = j0_candidates[0]
        print(f"\nВыбран j₀ = {j0+1} со значением Δ(x)[j₀] = {Delta[j0]}")

        # ШАГ 5. Формируем вектор направления l.
        # Составляем блочную матрицу H:
        D_ext = D[np.ix_(Jb_ext_py, Jb_ext_py)]
        A_ext = A[:, Jb_ext_py]
        zero_block = np.zeros((A.shape[0], A.shape[0]))
        H_top = np.hstack((D_ext, A_ext.T))
        H_bottom = np.hstack((A_ext, zero_block))
        H = np.vstack((H_top, H_bottom))
        print("\nМатрица H:\n", H)

        H_inv = inv(H)
        print("\nОбратная матрица H⁻¹:\n", H_inv)

        # Строим вектор b*:
        b_star_top = D[np.ix_(Jb_ext_py, [j0])].flatten()
        b_star_bottom = A[:, j0]
        b_star = np.concatenate((b_star_top, b_star_bottom))
        print("\nВектор b* (из элементов D и A для j₀):\n", b_star)

        l_ext = -H_inv.dot(b_star)
        print("\nl_ext = -H⁻¹ * b* =\n", l_ext)

        # Формируем полный вектор направления l (размер n).
        l = np.zeros(n)
        for idx, j in enumerate(Jb_ext_py):
            l[j] = l_ext[idx]
        if j0 not in Jb_ext_py:
            l[j0] = 1
        print("\nВектор направления l:\n", l)

        # ШАГ 6. Вычисляем величину δ = lᵀ·D·l.
        delta_val = l.dot(D.dot(l))
        print("\nδ = lᵀ·D·l =", delta_val)

        theta_j0 = abs(Delta[j0]) / delta_val if delta_val > tol else np.inf
        print("\nШаг по направлению j₀: θ(j₀) =", theta_j0)

        # Для каждого j из расширенной опоры (Jb_ext_py) вычисляем θ(j):
        theta_candidates = []
        for j in Jb_ext_py:
            if l[j] < -tol and x[j] > tol:
                theta_j = -x[j] / l[j]
            else:
                theta_j = np.inf
            theta_candidates.append((theta_j, j))
            print(f"θ для j = {j+1} равно {theta_j}")

        theta_candidates.append((theta_j0, j0))
        theta0, j_star = min(theta_candidates, key=lambda t: t[0])
        print(f"\nВыбранный шаг θ₀ = {theta0} при индексе j* = {j_star+1}")

        if theta0 == np.inf:
            print("Целевая функция не ограничена снизу на множестве допустимых планов.")
            return x
        if theta0 < tol:
            print(
                "Шаг равен 0 – возможна вырожденность или циклическое поведение. Прерывание алгоритма."
            )
            return x

        # ШАГ 7. Обновляем план: x = x + θ₀ * l.
        x = x + theta0 * l
        print("\nНовый допустимый план x после обновления:\n", x)

        # ШАГ 8. Обновляем опорные множества.
        # Если выбранный индекс j* совпадает с j₀, базис не меняется, а расширенная опора дополняется.
        if j_star == j0:
            if j0 not in Jb_ext_py:
                Jb_ext.append(j0 + 1)
                Jb_ext_py = [j - 1 for j in Jb_ext]
                print(f"\nОбновляем расширенную опору: добавляем j₀ = {j0+1} в Jb⁺.")
            else:
                print("\nОпорные множества не меняются (j₀ уже содержится в Jb⁺).")
        else:
            print(
                "\nОбновление базиса по правилам (2)–(4) не реализовано в данном примере."
            )

        print("Новый базис Jb =", Jb)
        print("Новая расширенная опора Jb⁺ =", Jb_ext)

        iter_num += 1

    print("\nМаксимальное число итераций достигнуто.")
    return x


def main():
    print("Входные данные для задачи квадратичного программирования:")
    # Считываем данные с консоли
    c, D, A, b, x, Jb, Jb_ext = get_input_data_qp()
    print("\n=== Решение задачи квадратичного программирования методом итераций ===")
    qp_method(c, D, A, b, x, Jb, Jb_ext)


if __name__ == "__main__":
    main()
