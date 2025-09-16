import math
from typing import List, Tuple

TOL = 1e-9
INT_TOL = 1e-7
MAX_ITERS = 5000


def gauss_jordan_inverse(A: List[List[float]]):
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, n):
            if abs(M[i][c]) > TOL:
                piv = i
                break
        if piv is None:
            return None
        if piv != r:
            M[r], M[piv] = M[piv], M[r]
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


def mat_mul(A: List[List[float]], x: List[float]) -> List[float]:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def vec_dot(a: List[float], b: List[float]) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))


def vec_sub(a: List[float], b: List[float]) -> List[float]:
    return [ai - bi for ai, bi in zip(a, b)]


class LPSolution:
    def __init__(self, x, obj, status):
        self.x = x
        self.obj = obj
        self.status = status


def dual_simplex(A, b, c, basis) -> LPSolution:
    m, n = len(A), len(A[0])
    B = basis[:]
    N = [j for j in range(n) if j not in B]

    for _ in range(MAX_ITERS):
        AB = [[A[i][j] for j in B] for i in range(m)]
        AB_inv = gauss_jordan_inverse(AB)
        if AB_inv is None:
            return LPSolution(None, -1e18, "dual_infeasible")

        xB = mat_mul(AB_inv, b)
        if min(xB) >= -TOL:
            x = [0.0] * n
            for k, j in enumerate(B):
                x[j] = max(0.0, xB[k])
            return LPSolution(x, vec_dot(c, x), "optimal")

        min_val = min(xB)
        cand_leave = [k for k, val in enumerate(xB) if abs(val - min_val) <= 1e-12]
        p = min(cand_leave)
        v = AB_inv[p][:]

        cB = [c[j] for j in B]
        y = [sum(cB[i] * AB_inv[i][r] for i in range(m)) for r in range(m)]

        AN = [[A[i][j] for j in N] for i in range(m)]
        rN = []
        for col in range(len(N)):
            rj = c[N[col]] - sum(y[i] * AN[i][col] for i in range(m))
            if 0 < rj < 1e-12:
                rj = 0.0
            rN.append(rj)
        wN = [sum(v[i] * AN[i][col] for i in range(m)) for col in range(len(N))]

        ratios = []
        for t in range(len(N)):
            if wN[t] < -TOL:
                theta = rN[t] / wN[t]
                ratios.append((theta, N[t], t))
        if not ratios:
            return LPSolution(None, -1e18, "infeasible")

        ratios.sort(key=lambda z: (z[0], z[1]))
        _, _, t = ratios[0]

        B[p], N[t] = N[t], B[p]
    return LPSolution(None, -1e18, "iters_exceeded")


def step1_make_c_nonpos(c, A, dminus, dplus):
    print(
        "\nШаг 1: Преобразование так, чтобы c <= 0 (инвертируем столбцы A и меняем d-, d+ местами со знаком)"
    )
    n, m = len(c), len(A)
    flipped = [False] * n
    for i in range(n):
        if c[i] > 0:
            flipped[i] = True
            c[i] = -c[i]
            for r in range(m):
                A[r][i] = -A[r][i]
            dminus[i], dplus[i] = -dplus[i], -dminus[i]
    print("c =", c)
    print("A =", A)
    print("d- =", dminus, " d+ =", dplus)
    return c, A, dminus, dplus, flipped


def build_augmented(c, A, b, dplus):
    n, m = len(c), len(A)
    rows, cols = m + n, n + m + n
    Aaug = [[0.0] * cols for _ in range(rows)]
    for i in range(m):
        for j in range(n):
            Aaug[i][j] = float(A[i][j])
        Aaug[i][n + i] = 1.0
    for i in range(n):
        Aaug[m + i][i] = 1.0
        Aaug[m + i][n + m + i] = 1.0
    baug = [float(x) for x in b] + [float(x) for x in dplus]
    caug = [float(x) for x in c] + [0.0] * m + [0.0] * n
    return Aaug, baug, caug


def is_int(x: float) -> bool:
    return abs(x - round(x)) <= INT_TOL


def branch_and_bound(c0, A0, b0, dminus0, dplus0, verbose=True):
    c, A, dminus, dplus, flipped = step1_make_c_nonpos(
        c0[:], [row[:] for row in A0], dminus0[:], dplus0[:]
    )
    n, m = len(c), len(A)

    Aaug, baug, caug = build_augmented(c, A, b0, dplus)
    if verbose:
        print(
            "\nШаг 2: Каноническая форма (Ax=b, x>=0). Переменные: x(1..n), s(1..m), u(1..n). Всего 2n+m =",
            2 * n + m,
        )
        for i in range(m + n):
            print(f"  row {i+1} :", Aaug[i], " | ", baug[i])
        print("c_aug =", caug, "(последние m+n нулевые)")

    tot_vars = len(caug)
    basis0 = list(range(n, n + m + n))
    delta0 = [float(x) for x in dminus] + [0.0] * m + [0.0] * n
    alpha0 = vec_dot(caug, delta0)
    bprime0 = vec_sub(baug, mat_mul(Aaug, delta0))
    if verbose:
        print("\nШаг 3: Δ =", delta0)
        print("α' = α + c^T Δ =", alpha0)
        print("b' = b - AΔ =", bprime0)
        print("Начальный базис B =", [i + 1 for i in basis0], "(1-based)")

    stack = [(Aaug, bprime0, caug, alpha0, basis0, delta0)]
    best = None

    iter_no = 0
    while stack:
        Acur, bcur, ccur, alpha_cur, Bcur, Dcur = stack.pop()
        iter_no += 1
        if verbose:
            print(
                f"\nШаг 4 (итерация {iter_no}). Решаем LP (двойственный симплекс). α'={alpha_cur}, Δ={Dcur[:n]}"
            )
        sol = dual_simplex(Acur, bcur, ccur, Bcur)
        if sol.status != "optimal" or sol.x is None:
            if verbose:
                print("  -> Ветвь даёт LP: ", sol.status)
            continue

        x_can = sol.x[:]
        obj_can = sol.obj + alpha_cur
        if verbose:
            print("  Опт. план LP:", x_can, "  c^T x + α' =", obj_can)

        frac = next((i for i in range(n) if not is_int(x_can[i])), None)
        if frac is None:
            x_hat = [x_can[i] + Dcur[i] for i in range(tot_vars)]
            val = vec_dot(ccur, x_can) + alpha_cur
            if best is None or val > best[1] + 1e-12:
                best = (x_hat, val)
                if verbose:
                    print(
                        "  ЦЕЛОЕ решение в этой ветви. x_hat[:n] =",
                        x_hat[:n],
                        " r =",
                        val,
                    )
            continue

        xi = x_can[frac]
        floor_i, ceil_i = math.floor(xi + 1e-12), math.ceil(xi - 1e-12)

        ub = math.floor(vec_dot(ccur, x_can) + alpha_cur + 1e-12)
        if best is not None and ub <= math.floor(best[1] + 1e-12):
            if verbose:
                print(
                    f"  Отсечение по границе: ⌊c^T x + α'⌋={ub} ≤ ⌊r_best⌋={math.floor(best[1])}"
                )
            continue

        bL = bcur[:]
        bL[m + frac] = float(floor_i)
        if verbose:
            print(
                f"  → Левая ветвь: поставить b'[{m+frac+1}] = ⌊x[{frac+1}]⌋ = {floor_i}"
            )
        stack.append((Acur, bL, ccur, alpha_cur, Bcur[:], Dcur[:]))

        dminus2 = [0.0] * tot_vars
        dminus2[frac] = float(ceil_i)
        D2 = [Dcur[k] + dminus2[k] for k in range(tot_vars)]
        alpha2 = alpha_cur + vec_dot(ccur, dminus2)
        b2 = vec_sub(bcur, mat_mul(Acur, dminus2))
        if verbose:
            print(
                f"  → Правая ветвь: добавить d^- = e_{frac+1} * ⌈x[{frac+1}]⌉ = {ceil_i}"
            )
            print(f"     Новые α''={alpha2}, Δ''[:n]={D2[:n]}")
        stack.append((Acur, b2, ccur, alpha2, Bcur[:], D2))

    if best is None:
        return "infeasible", None, None

    x_hat, r_best = best
    x_step2 = x_hat[:n]
    x_orig = x_step2[:]

    def restore(c0_i, xi):
        return -xi if c0_i > 0 else xi

    x_orig = [int(round(restore(c0[i], x_step2[i]))) for i in range(n)]
    obj_orig = sum(c0[i] * x_orig[i] for i in range(n))
    if verbose:
        print("\nШаг 5: восстановление исходного плана по правилу из методички.")
        print("  x(после шага 2) =", [round(v, 6) for v in x_step2])
        print("  x(исходный)     =", x_orig)
        print("  значение цели    =", obj_orig)
    return "optimal", x_orig, obj_orig


def get_input():
    n = int(input("Введите число переменных n: ").strip())
    m = int(input("Введите число ограничений m: ").strip())
    print("Введите коэффициенты целевой функции c (n целых):")
    c = [int(x) for x in input().split()]
    print("Введите матрицу A построчно (m строк по n целых):")
    A = [[int(x) for x in input().split()] for _ in range(m)]
    print("Введите вектор b (m целых):")
    b = [int(x) for x in input().split()]
    print("Введите нижние границы d- (n целых):")
    dminus = [int(x) for x in input().split()]
    print("Введите верхние границы d+ (n целых):")
    dplus = [int(x) for x in input().split()]
    return c, A, b, dminus, dplus


def main():
    c, A, b, dminus, dplus = get_input()
    status, x_opt, obj = branch_and_bound(c, A, b, dminus, dplus, verbose=True)
    print("\nРЕЗУЛЬТАТ:")
    if status == "optimal":
        print("Оптимальный план исходной задачи:", x_opt)
        print("Значение цели исходной задачи:", obj)
    else:
        print("Задача несовместна")


if __name__ == "__main__":
    main()
