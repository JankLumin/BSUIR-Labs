from fractions import Fraction


def example_data():
    c = [0, 1, 0, 0]
    A = [
        [3, 2, 1, 0],
        [-3, 2, 0, 1],
    ]
    b = [6, 0]
    return A, b, c


def fmt_q(q):
    return str(q) if q.denominator != 1 else str(q.numerator)


def fmt_vec(v):
    return "[" + "; ".join(fmt_q(x) for x in v) + "]"


def fmt_mat(M):
    return "[\n  " + "\n  ".join(fmt_vec(r) for r in M) + "\n]"


def toF_vec(v):
    return [Fraction(int(x)) for x in v]


def toF_mat(M):
    return [[Fraction(int(x)) for x in row] for row in M]


def matmul(A, B):
    m, k, n = len(A), len(A[0]), len(B[0])
    R = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            s = Fraction(0)
            for t in range(k):
                s += A[i][t] * B[t][j]
            R[i][j] = s
    return R


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def inv_mat(A):
    n = len(A)
    M = [A[i][:] + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for i in range(n):
        if M[i][i] == 0:
            sw = None
            for r in range(i + 1, n):
                if M[r][i] != 0:
                    sw = r
                    break
            if sw is None:
                raise ValueError("Matrix not invertible")
            M[i], M[sw] = M[sw], M[i]
        piv = M[i][i]
        M[i] = [x / piv for x in M[i]]
        for r in range(n):
            if r == i:
                continue
            coef = M[r][i]
            if coef != 0:
                M[r] = [M[r][t] - coef * M[i][t] for t in range(2 * n)]
    return [row[n:] for row in M]


def fractional_part(q):
    return q - Fraction(q.numerator // q.denominator, 1)


def simplex_solve(A_in, b_in, c_in):
    A = toF_mat(A_in)
    b = toF_vec(b_in)
    c = toF_vec(c_in)
    m, n = len(A), len(A[0])
    A1 = [
        A[i] + [Fraction(1) if i == k else Fraction(0) for k in range(m)]
        for i in range(m)
    ]
    c1 = [Fraction(0) for _ in range(n)] + [Fraction(-1) for _ in range(m)]
    B = list(range(n, n + m))
    Binv = inv_mat([[A1[i][j] for j in B] for i in range(m)])
    Abar = matmul(Binv, A1)
    bbar = matvec(Binv, b)

    def phase(cvec, cols):
        nonlocal Abar, bbar, B
        while True:
            cB = [cvec[j] for j in B]
            cbar = [cvec[j] - sum(cB[i] * Abar[i][j] for i in range(m)) for j in cols]
            enter = None
            for j in cols:
                if j in B:
                    continue
                if cbar[j - cols[0]] > 0:
                    enter = j
                    break
            if enter is None:
                return sum(cB[i] * bbar[i] for i in range(m))
            col = [Abar[i][enter] for i in range(m)]
            pos = [(bbar[i] / col[i], i) for i in range(m) if col[i] > 0]
            if not pos:
                return None
            _, r = min(pos, key=lambda p: (p[0], p[1]))
            piv = Abar[r][enter]
            Abar[r] = [x / piv for x in Abar[r]]
            bbar[r] = bbar[r] / piv
            for i in range(m):
                if i == r:
                    continue
                coef = Abar[i][enter]
                if coef != 0:
                    Abar[i] = [
                        Abar[i][t] - coef * Abar[r][t] for t in range(len(Abar[i]))
                    ]
                    bbar[i] = bbar[i] - coef * bbar[r]
            B[r] = enter

    phase(c1, list(range(n + m)))
    Abar = [row[:n] for row in Abar]
    while True:
        cB = [c[j] for j in B]
        cbar = [c[j] - sum(cB[i] * Abar[i][j] for i in range(m)) for j in range(n)]
        enter = None
        for j in range(n):
            if j in B:
                continue
            if cbar[j] > 0:
                enter = j
                break
        if enter is None:
            x = [Fraction(0) for _ in range(n)]
            for i in range(m):
                x[B[i]] = bbar[i]
            print(
                "  оптимальный план LP найден:",
                fmt_vec(x),
                "; значение =",
                fmt_q(sum(cB[i] * bbar[i] for i in range(m))),
            )
            print("  базис B =", [j + 1 for j in B])
            return {"x": x, "B": B}
        col = [Abar[i][enter] for i in range(m)]
        pos = [(bbar[i] / col[i], i) for i in range(m) if col[i] > 0]
        if not pos:
            return {"x": None, "B": B}
        _, r = min(pos, key=lambda p: (p[0], p[1]))
        piv = Abar[r][enter]
        Abar[r] = [x / piv for x in Abar[r]]
        bbar[r] = bbar[r] / piv
        for i in range(m):
            if i == r:
                continue
            coef = Abar[i][enter]
            if coef != 0:
                Abar[i] = [Abar[i][t] - coef * Abar[r][t] for t in range(n)]
                bbar[i] = bbar[i] - coef * bbar[r]
        B[r] = enter


def gomory_cut(A_in, b_in, c_in):
    A = toF_mat(A_in)
    b = toF_vec(b_in)
    c = toF_vec(c_in)
    print("Шаг 1. Решаем задачу LP без целочисленности")
    lp = simplex_solve(A, b, c)
    x = lp["x"]
    B = lp["B"]
    all_int = all(xi.denominator == 1 for xi in x)
    if all_int:
        print("\nШаг 2. Все компоненты целые ⇒ найден оптимальный целочисленный план")
        print("  x =", fmt_vec(x))
        return
    print("\nШаг 2. План дробный ⇒ строим отсек Гомори")
    for k, j in enumerate(B):
        if x[j].denominator != 1:
            idx_frac = j
            k_pos = k
            break
    print(
        f"  дробная базисная компонента: x[{idx_frac+1}] = {fmt_q(x[idx_frac])}, позиция в B: k = {k_pos+1}"
    )
    m, n = len(A), len(A[0])
    Nidx = [j for j in range(n) if j not in B]
    AB = [[A[i][j] for j in B] for i in range(m)]
    AN = [[A[i][j] for j in Nidx] for i in range(m)]
    print("\nШаг 3. Формируем матрицы")
    print("  AB =", fmt_mat(AB))
    print("  AN =", fmt_mat(AN))
    AB_inv = inv_mat(AB)
    print("\nШаг 4. Находим A_B^{-1} =", fmt_mat(AB_inv))
    Q = matmul(AB_inv, AN)
    print("\nШаг 5. Находим Q = A_B^{-1} * A_N =", fmt_mat(Q))
    ell = Q[k_pos]
    print(f"\nШаг 6. Берём k-ю строку ℓ (k = {k_pos+1}) =", fmt_vec(ell))
    frac_ell = [fractional_part(v) for v in ell]
    rhs = fractional_part(x[idx_frac])
    print("\nШаг 7. Дробные части коэффициентов {ℓ} =", fmt_vec(frac_ell))
    print("  дробная часть {x_i} =", fmt_q(rhs))
    coeff = [Fraction(0) for _ in range(n + 1)]
    for p, j in enumerate(Nidx):
        coeff[j] = frac_ell[p]
    coeff[-1] = Fraction(-1)
    terms = [f"{fmt_q(coeff[j])}*x{j+1}" for j in range(n) if coeff[j] != 0]
    left = " + ".join(terms) + " - s"
    print("\nШаг 8. Отсекающее ограничение Гомори")
    print(f"  {left} = {fmt_q(rhs)}")
    print("  вектор коэффициентов:", fmt_vec(coeff))
    print("  свободный член:", fmt_q(rhs))


def main():
    A, b, c = example_data()
    gomory_cut(A, b, c)


if __name__ == "__main__":
    main()
