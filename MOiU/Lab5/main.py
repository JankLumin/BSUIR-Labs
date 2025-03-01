import numpy as np
from copy import deepcopy


def clean_matrix(matrix):
    """
    Заменяет значения, близкие к нулю, на 0.0 для лучшей читаемости.
    """
    cleaned = matrix.copy()
    cleaned[np.isclose(cleaned, 0.0)] = 0.0
    return cleaned


def place_marks_on_B(B_marks, basis):
    """
    Рекурсивно определяет знаки ("+" для True, "-" для False)
    для ячеек базиса в цикле.

    B_marks: словарь, где ключи — кортежи (i, j) базисных ячеек,
             а значения — их знак (True для "+", False для "-", None – не определено).
    basis: кортеж (i, j), стартовая ячейка, для которой знак уже задан.
    """
    current_sign = not B_marks[basis]
    for (i, j) in B_marks.keys():
        if basis[0] == i or basis[1] == j:
            if B_marks[(i, j)] is None:
                B_marks[(i, j)] = current_sign
                place_marks_on_B(B_marks, (i, j))


def potentials_method(supply, demand, cost):
    """
    Решает транспортную задачу методом потенциалов.

    supply: вектор поставок (numpy.array)
    demand: вектор спроса (numpy.array)
    cost: матрица затрат (numpy.array)
    """
    total_supply = np.sum(supply)
    total_demand = np.sum(demand)
    if total_supply > total_demand:
        demand = np.append(demand, total_supply - total_demand)
        cost = np.hstack((cost, np.zeros((len(supply), 1))))
        print("Балансировка: добавлен фиктивный столбец (спрос)")
    elif total_supply < total_demand:
        supply = np.append(supply, total_demand - total_supply)
        cost = np.vstack((cost, np.zeros((1, len(demand)))))
        print("Балансировка: добавлена фиктивная строка (поставки)")

    m = len(supply)
    n = len(demand)
    # Построение начального решения методом северо‑западного угла
    x = np.zeros((m, n))
    basis = []  # базисные ячейки в виде кортежей (i, j)
    i = 0
    j = 0
    supply_left = supply.copy()
    demand_left = demand.copy()

    while i < m and j < n:
        allocation = min(supply_left[i], demand_left[j])
        x[i, j] = allocation
        basis.append((i, j))
        supply_left[i] -= allocation
        demand_left[j] -= allocation

        # Если достигли последнего источника и последнего пункта, завершаем цикл
        if i == m - 1 and j == n - 1:
            break

        if np.isclose(supply_left[i], 0) and i < m - 1:
            i += 1
        elif np.isclose(demand_left[j], 0) and j < n - 1:
            j += 1
        else:
            if i < m - 1:
                i += 1
            if j < n - 1:
                j += 1

    print("\nНачальное решение:")
    print("Матрица x:")
    print(clean_matrix(x))
    print("Начальный базис:", basis)

    iteration = 0
    while True:
        iteration += 1
        print("\n" + "=" * 50)
        print(f"Итерация {iteration}")
        print("=" * 50)

        # Формирование системы уравнений для потенциалов: u[i] + v[j] = cost[i, j] для всех (i, j) из базиса
        A_eq = []
        b_eq = []
        for (i_cell, j_cell) in basis:
            row = [0] * (m + n)
            row[i_cell] = 1
            row[m + j_cell] = 1
            A_eq.append(row)
            b_eq.append(cost[i_cell, j_cell])
        # Дополнительное уравнение: u[0] = 0
        eq_fix = [0] * (m + n)
        eq_fix[0] = 1
        A_eq.append(eq_fix)
        b_eq.append(0)

        A_eq = np.array(A_eq, dtype=float)
        b_eq = np.array(b_eq, dtype=float)

        potentials = np.linalg.solve(A_eq, b_eq)
        u = potentials[:m]
        v = potentials[m:]

        print("\nПотенциалы u:", u)
        print("Потенциалы v:", v)

        # Поиск кандидата для улучшения плана:
        candidate = None
        for i_cell in range(m):
            for j_cell in range(n):
                if (i_cell, j_cell) not in basis and (u[i_cell] + v[j_cell] - cost[i_cell, j_cell]) > 1e-10:
                    candidate = (i_cell, j_cell)
                    break
            if candidate is not None:
                break

        if candidate is None:
            print("\nОптимальный план найден:")
            print(clean_matrix(x))
            return

        print("\nКандидат для включения в базис:", candidate)

        # Включаем кандидата в базис и формируем цикл перераспределения
        basis.append(candidate)
        basis.sort()
        cycle = deepcopy(basis)
        # Отбираем те ячейки, где по строке или столбцу более одной базисной позиции
        for i_cell in range(m):
            count = sum(1 for (p, q) in cycle if p == i_cell)
            if count <= 1:
                cycle = [cell for cell in cycle if cell[0] != i_cell]
        for j_cell in range(n):
            count = sum(1 for (p, q) in cycle if q == j_cell)
            if count <= 1:
                cycle = [cell for cell in cycle if cell[1] != j_cell]

        # Назначаем знаки ячейкам цикла: кандидат получает знак "+"
        cycle_marks = {cell: None for cell in cycle}
        cycle_marks[candidate] = True
        place_marks_on_B(cycle_marks, candidate)

        # Вычисляем параметр θ — минимальное значение среди ячеек с отрицательным знаком
        theta = np.inf
        for cell, sign in cycle_marks.items():
            if sign is False:
                i_cell, j_cell = cell
                if x[i_cell, j_cell] < theta:
                    theta = x[i_cell, j_cell]
        print("\nПараметр θ =", theta)

        # Корректировка плана: увеличиваем значения по ячейкам с "+" и уменьшаем с "-"
        for cell, sign in cycle_marks.items():
            i_cell, j_cell = cell
            if sign:
                x[i_cell, j_cell] += theta
            else:
                x[i_cell, j_cell] -= theta

        # Если какая-либо базисная ячейка стала равна 0, удаляем её из базиса (кроме кандидата)
        for cell in basis:
            i_cell, j_cell = cell
            if np.isclose(x[i_cell, j_cell], 0) and cell != candidate:
                print("Удаляем из базиса ячейку:", cell)
                basis.remove(cell)
                break

        print("\nОбновленный план (x):")
        print(clean_matrix(x))
        print("Текущий базис:", basis)


def get_input_data():
    """
    Считывает входные данные для транспортной задачи:
      - число источников (m),
      - число пунктов назначения (n),
      - вектор поставок,
      - вектор спроса,
      - матрица затрат.
    """
    try:
        m = int(input("Введите количество источников (m): "))
        n = int(input("Введите количество пунктов назначения (n): "))
    except ValueError:
        print("Ошибка ввода: введите целые числа для m и n.")
        exit(1)

    print(f"\nВведите вектор поставок (размер {m}):")
    supply_input = input("Поставки: ").strip().split()
    if len(supply_input) != m:
        print("Ошибка: количество элементов не соответствует m.")
        exit(1)
    supply = np.array([float(num) for num in supply_input], dtype=float)

    print(f"\nВведите вектор спроса (размер {n}):")
    demand_input = input("Спрос: ").strip().split()
    if len(demand_input) != n:
        print("Ошибка: количество элементов не соответствует n.")
        exit(1)
    demand = np.array([float(num) for num in demand_input], dtype=float)

    print(f"\nВведите матрицу затрат (размер {m}x{n}):")
    cost = []
    for i in range(m):
        row_input = input(f"Строка {i + 1}: ").strip().split()
        if len(row_input) != n:
            print("Ошибка: количество элементов в строке не соответствует n.")
            exit(1)
        cost.append([float(num) for num in row_input])
    cost = np.array(cost, dtype=float)

    return supply, demand, cost


def main():
    print("Входные данные для транспортной задачи:")
    supply, demand, cost = get_input_data()
    print("\n=== Решение транспортной задачи методом потенциалов ===")
    potentials_method(supply, demand, cost)


if __name__ == '__main__':
    main()
