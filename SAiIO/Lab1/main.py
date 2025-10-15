from fractions import Fraction


def example_data():
    c = [1, 1]
    A = [
        [5, 9],
        [9, 5],
    ]
    b = [63, 63]
    d_minus = [1, 1]
    d_plus = [6, 6]
    return A, b, c, d_minus, d_plus


def fmt_vec(v):
    def f(x):
        if isinstance(x, Fraction):
            return str(x) if x.denominator != 1 else str(x.numerator)
        return str(x)

    return "[" + "; ".join(f(x) for x in v) + "]"


def to_frac_vec(v):
    return [Fraction(int(x)) for x in v]


def to_frac_mat(M):
    return [[Fraction(int(x)) for x in row] for row in M]


def matmul_vec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def vec_add(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def vec_sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def vec_dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def build_extended_lp(A, b, c, d_minus, d_plus, verbose=True):
    A = to_frac_mat(A)
    b = to_frac_vec(b)
    c = to_frac_vec(c)
    d_minus = to_frac_vec(d_minus)
    d_plus = to_frac_vec(d_plus)
    m = len(A)
    n = len(A[0])
    if verbose:
        print("Шаг 1. Приведение знаков стоимостей")
    flipped = [False] * n
    for i in range(n):
        if c[i] > 0:
            c[i] = -c[i]
            for r in range(m):
                A[r][i] = -A[r][i]
            d_minus[i] = -d_minus[i]
            d_plus[i] = -d_plus[i]
            d_minus[i], d_plus[i] = d_plus[i], d_minus[i]
            flipped[i] = True
    if verbose:
        print("  c'   =", fmt_vec(c))
        print("  d-'  =", fmt_vec(d_minus), " d+' =", fmt_vec(d_plus))
        print("Шаг 2. Построение расширенной задачи")
    A_ext = []
    for r in range(m):
        row = []
        row += A[r]
        row += [Fraction(1) if r == k else Fraction(0) for k in range(m)]
        row += [Fraction(0) for _ in range(n)]
        A_ext.append(row)
    for i in range(n):
        row = []
        row += [Fraction(1) if i == j else Fraction(0) for j in range(n)]
        row += [Fraction(0) for _ in range(m)]
        row += [Fraction(1) if i == j else Fraction(0) for j in range(n)]
        A_ext.append(row)
    b_ext = b + d_plus
    c_ext = c + [Fraction(0)] * (m + n)
    dminus_ext = d_minus + [Fraction(0)] * (m + n)
    if verbose:
        print(f"  размерность x: {2*n+m}")
    B0 = list(range(n, n + m + n))
    return {
        "A_ext": A_ext,
        "b_ext": b_ext,
        "c_ext": c_ext,
        "dminus_ext": dminus_ext,
        "flipped": flipped,
        "m": m,
        "n": n,
        "B0": B0,
    }


def dual_simplex(A_ext, b_rhs, c_ext, B0, verbose=False, max_iter=1000):
    M = len(A_ext)
    N = len(A_ext[0])
    Abar = to_frac_mat(A_ext)
    bbar = to_frac_vec(b_rhs)
    B = B0[:]
    for k in range(M):
        jbas = B[k]
        piv = Abar[k][jbas]
        if piv == 0:
            swap = None
            for r in range(k + 1, M):
                if Abar[r][jbas] != 0:
                    swap = r
                    break
            if swap is None:
                return {"status": "infeasible"}
            Abar[k], Abar[swap] = Abar[swap], Abar[k]
            bbar[k], bbar[swap] = bbar[swap], bbar[k]
            piv = Abar[k][jbas]
        Abar[k] = [x / piv for x in Abar[k]]
        bbar[k] = bbar[k] / piv
        for r in range(M):
            if r == k:
                continue
            coef = Abar[r][jbas]
            if coef != 0:
                Abar[r] = [Abar[r][t] - coef * Abar[k][t] for t in range(N)]
                bbar[r] = bbar[r] - coef * bbar[k]

    def compute_reduced_costs():
        Bmat = [[A_ext[i][j] for j in B] for i in range(M)]
        cB = [c_ext[j] for j in B]
        Aug = [[Fraction(0)] * (M + 1) for _ in range(M)]
        for i in range(M):
            for j in range(M):
                Aug[i][j] = Bmat[j][i]
            Aug[i][M] = cB[i]
        for i in range(M):
            if Aug[i][i] == 0:
                swap = None
                for r in range(i + 1, M):
                    if Aug[r][i] != 0:
                        swap = r
                        break
                if swap is not None:
                    Aug[i], Aug[swap] = Aug[swap], Aug[i]
            piv = Aug[i][i]
            if piv != 0:
                for t in range(i, M + 1):
                    Aug[i][t] /= piv
                for r in range(M):
                    if r == i:
                        continue
                    coef = Aug[r][i]
                    if coef != 0:
                        for t in range(i, M + 1):
                            Aug[r][t] -= coef * Aug[i][t]
        pi = [Aug[i][M] for i in range(M)]
        cbar = [c_ext[j] - sum(pi[i] * A_ext[i][j] for i in range(M)) for j in range(N)]
        z = sum(c_ext[B[i]] * bbar[i] for i in range(M))
        return cbar, z

    it = 0
    while True:
        it += 1
        if it > max_iter:
            return {"status": "infeasible"}
        cbar, z = compute_reduced_costs()
        viol_rows = [i for i in range(M) if bbar[i] < 0]
        if not viol_rows:
            x = [Fraction(0) for _ in range(N)]
            for i in range(M):
                x[B[i]] = bbar[i]
            return {"status": "optimal", "x": x, "obj": z}
        r = min(viol_rows, key=lambda i: (bbar[i], i))
        candidates = []
        for j in range(N):
            if Abar[r][j] < 0:
                theta = cbar[j] / Abar[r][j]
                candidates.append((theta, j))
        if not candidates:
            return {"status": "infeasible"}
        _, j_in = min(candidates, key=lambda p: (p[0], p[1]))
        piv = Abar[r][j_in]
        Abar[r] = [x / piv for x in Abar[r]]
        bbar[r] = bbar[r] / piv
        for i in range(M):
            if i == r:
                continue
            coef = Abar[i][j_in]
            if coef != 0:
                Abar[i] = [Abar[i][t] - coef * Abar[r][t] for t in range(N)]
                bbar[i] = bbar[i] - coef * bbar[r]
        B[r] = j_in


def first_n_integer(x, n):
    for i in range(n):
        if x[i].denominator != 1:
            return False
    return True


def first_fractional_index(x, n):
    for i in range(n):
        if x[i].denominator != 1:
            return i
    return None


def floor_frac(q):
    return Fraction(q.numerator // q.denominator, 1)


def ceil_frac(q):
    return (
        q
        if q.denominator == 1
        else Fraction((q.numerator + q.denominator - 1) // q.denominator, 1)
    )


def branch_and_bound():
    A, b, c, d_minus, d_plus = example_data()
    data = build_extended_lp(A, b, c, d_minus, d_plus, verbose=True)
    A_ext = data["A_ext"]
    b_ext = data["b_ext"]
    c_ext = data["c_ext"]
    dminus_ext = data["dminus_ext"]
    flipped = data["flipped"]
    m = data["m"]
    n = data["n"]
    B0 = data["B0"]
    N = n + m + n
    print("Шаг 3. Инициализация стека")
    x_star = None
    r_best = None
    S = [(Fraction(0), b_ext[:], dminus_ext[:], dminus_ext[:])]
    print("  добавлена исходная вершина")
    k = 0
    while S:
        k += 1
        alpha_base, b_base, Delta_total, d_delta = S.pop()
        alpha_cur = alpha_base + vec_dot(c_ext, d_delta)
        b_cur = vec_sub(b_base, matmul_vec(A_ext, d_delta))
        print(f"\nШаг 4. Итерация {k}")
        print("  α' =", alpha_cur)
        res = dual_simplex(A_ext, b_cur, c_ext, B0, verbose=False)
        if res["status"] != "optimal":
            print("  несовместно — отсечение")
            continue
        xe = res["x"]
        value_node = res["obj"] + alpha_cur
        print("  значение узла =", value_node, "; x_e[1..n] =", fmt_vec(xe[:n]))
        if first_n_integer(xe, n):
            xhat = vec_add(xe, Delta_total)
            if x_star is None or value_node > r_best:
                x_star = xhat
                r_best = value_node
                print("  целочисленно ⇒ обновление лучшего решения: r =", r_best)
            else:
                print("  целочисленно, но без улучшения")
            continue
        i = first_fractional_index(xe, n)
        floor_i = floor_frac(xe[i])
        ceil_i = ceil_frac(xe[i])
        print(f"  дробная компонента x[{i+1}]={xe[i]} ⇒ [{floor_i}, {ceil_i}]")
        if (x_star is None) or (floor_frac(value_node) > r_best):
            b_child1 = b_cur[:]
            b_child1[m + i] = floor_i
            S.append((alpha_cur, b_child1, Delta_total[:], [Fraction(0)] * N))
            d2 = [Fraction(0)] * N
            d2[i] = ceil_i
            Delta2 = Delta_total[:]
            Delta2[i] += ceil_i
            S.append((alpha_cur, b_cur[:], Delta2, d2))
            print("  ветвимся на 2 узла")
        else:
            print("  отсечено по оценке")
    print("\nЗавершение")
    if x_star is None:
        print("Задача несовместна")
        return
    x_rec = []
    for i in range(n):
        xi = x_star[i]
        x_rec.append(-xi if flipped[i] else xi)
    c_orig = []
    for i in range(n):
        c_orig.append(-c_ext[i] if flipped[i] else c_ext[i])
    val_orig = vec_dot(c_orig, x_rec)
    print("Лучший расширенный план x* =", fmt_vec(x_star))
    print("Оптимальный план исходной задачи x =", fmt_vec(x_rec))
    print("c^T x =", val_orig)


if __name__ == "__main__":
    branch_and_bound()
