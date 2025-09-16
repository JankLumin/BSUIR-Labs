from typing import List, Tuple, Optional
import math

TOL = 1e-9


def mat_copy(M: List[List[float]]) -> List[List[float]]:
    return [row[:] for row in M]


def eye(n: int) -> List[List[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def mat_vec(A: List[List[float]], x: List[float]) -> List[float]:
    m, n = len(A), len(A[0])
    assert len(x) == n
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]


def vec_add(a: List[float], b: List[float]) -> List[float]:
    return [ai + bi for ai, bi in zip(a, b)]


def vec_sub(a: List[float], b: List[float]) -> List[float]:
    return [ai - bi for ai, bi in zip(a, b)]


def vec_dot(a: List[float], b: List[float]) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))


def mat_cols(A: List[List[float]], idxs: List[int]) -> List[List[float]]:
    return [[A[i][j] for j in idxs] for i in range(len(A))]


def gauss_jordan_inverse(A: List[List[float]]) -> Optional[List[List[float]]]:
    n = len(A)
    assert all(len(row) == n for row in A)
    M = [row[:] + e[:] for row, e in zip(A, eye(n))]
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, n):
            if abs(M[i][c]) > TOL:
                pivot = i
                break
        if pivot is None:
            return None
        if pivot != r:
            M[r], M[pivot] = M[pivot], M[r]
        div = M[r][c]
        for j in range(2 * n):
            M[r][j] /= div
        for i in range(n):
            if i == r:
                continue
            f = M[i][c]
            if abs(f) > TOL:
                for j in range(2 * n):
                    M[i][j] -= f * M[r][j]
        r += 1
    return [row[n:] for row in M]


def fractional_part(x: float) -> float:
    return x - math.floor(x + 1e-12)


def is_integer(x: float) -> bool:
    return abs(x - round(x)) <= 1e-9


class SimplexResult:
    def __init__(
        self,
        status: str,
        x: Optional[List[float]] = None,
        B: Optional[List[int]] = None,
        obj: float = 0.0,
    ):
        self.status = status
        self.x = x
        self.B = B
        self.obj = obj


def primal_simplex(
    A: List[List[float]],
    b: List[float],
    c: List[float],
    B_init: List[int],
    var_costs: List[float],
) -> SimplexResult:

    m, n = len(A), len(A[0])
    B = B_init[:]
    N = [j for j in range(n) if j not in B]

    while True:
        AB = mat_cols(A, B)
        invAB = gauss_jordan_inverse(AB)
        if invAB is None:
            return SimplexResult("infeasible")
        xB = mat_vec(invAB, b)
        if min(xB) < -1e-8:
            return SimplexResult("infeasible")

        cB = [var_costs[j] for j in B]
        y = [sum(cB[i] * invAB[i][r] for i in range(m)) for r in range(m)]
        rN = []
        for j in N:
            col = [A[i][j] for i in range(m)]
            rj = var_costs[j] - sum(y[i] * col[i] for i in range(m))
            rN.append((j, rj))
        if all(rj <= 1e-12 for (_, rj) in rN):
            x = [0.0] * n
            for k, idx in enumerate(B):
                x[idx] = max(0.0, xB[k])
            obj = vec_dot(var_costs, x)
            return SimplexResult("optimal", x=x, B=B, obj=obj)
        enter_candidates = [(j, rj) for (j, rj) in rN if rj > 1e-12]
        enter_candidates.sort(key=lambda t: (-t[1], t[0]))
        j_enter = enter_candidates[0][0]

        Aj = [A[i][j_enter] for i in range(m)]
        dB = mat_vec(invAB, Aj)
        if all(di <= 1e-12 for di in dB):
            return SimplexResult("unbounded")

        theta = float("inf")
        leave_pos = None
        for i in range(m):
            if dB[i] > 1e-12:
                t = xB[i] / dB[i]
                if t < theta - 1e-12 or (
                    abs(t - theta) <= 1e-12
                    and B[i] < (B[leave_pos] if leave_pos is not None else 1 << 60)
                ):
                    theta = t
                    leave_pos = i
        if leave_pos is None:
            return SimplexResult("unbounded")

        out = B[leave_pos]
        B[leave_pos] = j_enter
        N = [j for j in range(n) if j not in B]


def two_phase_simplex_equalities(
    A: List[List[float]], b: List[float], c: List[float]
) -> SimplexResult:
    m, n = len(A), len(A[0])

    A_e = [row[:] + [0.0] * m for row in A]
    for i in range(m):
        A_e[i][n + i] = 1.0
    c_phase1 = [0.0] * n + [-1.0] * m
    B0 = list(range(n, n + m))

    print("\n--- Фаза I: начальный базис — искусственные переменные ---")
    print("A_e (m x (n+m)):")
    for i in range(m):
        print("  ", A_e[i], "|", b[i])
    print("Цель Фазы I: maximize -sum(a)")

    res1 = primal_simplex(A_e, b, c_phase1, B0, c_phase1)
    if res1.status == "infeasible":
        print("Фаза I: несовместно → исходная задача несовместна.")
        return SimplexResult("infeasible")
    if res1.status == "unbounded":
        print("Фаза I: неограничена (нетипично).")
        return SimplexResult("infeasible")

    if res1.obj < -1e-8:
        print("Фаза I: optimum < 0 → несовместно.")
        return SimplexResult("infeasible")

    B_phase2 = []
    for idx in res1.B:
        if idx < n:
            B_phase2.append(idx)
        else:
            row_idx = len(B_phase2)
            pass

    if len(B_phase2) != m:
        B_phase2 = [i for i in range(min(n, m))]

    print("\n--- Фаза II: цель исходной задачи ---")
    print("max c^T x,   Ax = b, x>=0")
    print("c =", c)

    res2 = primal_simplex(A, b, c, B_phase2, c)
    return res2


def build_gomory_cut(
    A: List[List[float]],
    b: List[float],
    c: List[float],
    x_opt: List[float],
    B: List[int],
) -> Optional[Tuple[List[int], List[float], float, int]]:
    m, n = len(A), len(A[0])
    B_orig = [j for j in B if j < n]
    N_orig = [j for j in range(n) if j not in B_orig]
    if len(B_orig) < m:
        return None

    AB = mat_cols(A, B_orig)
    invAB = gauss_jordan_inverse(AB)
    if invAB is None:
        return None
    xB = mat_vec(invAB, b)

    k = None
    for idx, val in enumerate(xB):
        if not is_integer(val):
            k = idx
            break
    if k is None:
        return None

    basic_i = B_orig[k]
    AN = mat_cols(A, N_orig)
    rows, cols = len(invAB), len(AN[0]) if AN else 0
    Q = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            s = 0.0
            for t in range(m):
                s += invAB[i][t] * AN[t][j]
            Q[i][j] = s
    l_row = Q[k] if cols > 0 else []

    coeffs_frac = [fractional_part(v) for v in l_row]
    rhs_frac = fractional_part(xB[k])
    return (N_orig, coeffs_frac, rhs_frac, basic_i)


def read_input() -> Tuple[int, int, List[float], List[List[float]], List[float]]:
    n = int(input("Введите число переменных n: ").strip())
    m = int(input("Введите число ограничений m: ").strip())
    print("Введите коэффициенты целевой функции c (n чисел):")
    c = [float(x) for x in input().split()]
    if len(c) != n:
        raise ValueError("Ожидалось n чисел в c")
    print("Введите матрицу A построчно (m строк по n чисел):")
    A = []
    for i in range(m):
        row = [float(x) for x in input(f"Строка {i+1}: ").split()]
        if len(row) != n:
            raise ValueError("Неверное число значений в строке A")
        A.append(row)
    print("Введите вектор b (m чисел):")
    b = [float(x) for x in input().split()]
    if len(b) != m:
        raise ValueError("Ожидалось m чисел в b")
    return n, m, c, A, b


def main():
    n, m, c, A, b = read_input()

    print("\n--- Шаг 1. Решаем LP-расслабление (двухфазный симплекс) ---")
    res = two_phase_simplex_equalities(A, b, c)

    if res.status == "infeasible":
        print("\nШаг 2. Итог: задача (DP) несовместна.")
        return
    if res.status == "unbounded":
        print("\nШаг 2. Итог: целевая функция неограничена сверху.")
        return

    x = res.x
    B = res.B
    print("\nШаг 1 (результат): оптимальный план LP:")
    print("x* =", [round(v, 6) for v in x])
    print("Базис B =", [j + 1 for j in B], "(1-based)")
    print(f"Значение цели c^T x = {round(res.obj,6)}")

    if all(is_integer(xi) for xi in x[:n]):
        print("\nШаг 3. Все компоненты x целые → это оптимальный план задачи (DP).")
        print("Оптимальный план:", [int(round(xi)) for xi in x[:n]])
        print("Значение цели:", int(round(res.obj)))
        return

    print("\nШаг 4–11. Строим одно отсекающее ограничение Гомори.")
    cut = build_gomory_cut(A, b, c, x, B)
    if cut is None:
        print(
            "Не удалось построить отсечение (нет дробной базисной оригинальной переменной)."
        )
        return
    N_idx, coeffs, rhs, basic_i = cut

    print(f"Дробная базисная переменная: x{basic_i+1}")
    print("Небазисные переменные x_N:", [f"x{j+1}" for j in N_idx])

    terms = []
    for coef, j in zip(coeffs, N_idx):
        if abs(coef) > 1e-12:
            terms.append(f"{{{coef}}}*x{j+1}")
    left = " + ".join(terms) if terms else "0"
    print("Отсекающее ограничение Гомори:")
    print(f"{left} - s = {{{rhs}}}")

    print("\nКоэффициенты в виде вектора (по x1..xn, затем s):")
    coeffs_full = [0.0] * n
    for coef, j in zip(coeffs, N_idx):
        coeffs_full[j] = coef
    print(
        " ",
        [round(v, 6) for v in coeffs_full],
        "  и  -1 при s;  правая часть =",
        round(rhs, 6),
    )


if __name__ == "__main__":
    main()
