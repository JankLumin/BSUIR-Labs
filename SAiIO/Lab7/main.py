from fractions import Fraction

def example_data():
    C = [
        [7, 2, 1, 9, 4],
        [9, 6, 9, 5, 5],
        [3, 8, 3, 1, 8],
        [7, 9, 4, 2, 2],
        [8, 4, 7, 4, 8],
    ]
    return C

def fmt_vec(v):
    return "[" + "; ".join(str(x) for x in v) + "]"

def fmt_mat(M):
    lines = []
    for r in M:
        lines.append("  [" + "; ".join(str(x) for x in r) + "]")
    return "[\n" + "\n".join(lines) + "\n]"

def transpose(M):
    n = len(M)
    m = len(M[0]) if n else 0
    return [[M[i][j] for i in range(n)] for j in range(m)]

def argmin(lst):
    best = None
    idx = None
    for i, v in enumerate(lst):
        if best is None or v < best:
            best = v
            idx = i
    return idx, best

def build_Jeq(C, alpha, beta):
    n = len(C)
    Jeq = []
    Jlt = []
    for i in range(n):
        for j in range(n):
            s = alpha[i] + beta[j]
            cij = Fraction(C[i][j])
            if s == cij:
                Jeq.append((i, j))
            elif s < cij:
                Jlt.append((i, j))
    return Jeq, Jlt

def max_matching_with_reachable(n, edges):
    adjU = [[] for _ in range(n)]
    for (i, j) in edges:
        adjU[i].append(j)

    pairU = [-1] * n
    pairV = [-1] * n

    from collections import deque

    def bfs_find_path():
        q = deque()
        parentU = [-1] * n
        parentV = [-1] * n
        inQ_u = [False] * n
        inQ_v = [False] * n

        for u in range(n):
            if pairU[u] == -1:
                q.append(('U', u))
                inQ_u[u] = True
                parentU[u] = -2

        targetV = -1

        while q:
            side, node = q.popleft()
            if side == 'U':
                u = node
                for v in adjU[u]:
                    if not inQ_v[v]:
                        inQ_v[v] = True
                        parentV[v] = u
                        if pairV[v] == -1:
                            targetV = v
                            path = []
                            cur_v = v
                            while cur_v != -1:
                                pu = parentV[cur_v]
                                path.append((pu, cur_v))
                                if parentU[pu] == -2:
                                    break
                                cur_u = parentU[pu]
                                cur_v = cur_u
                            break
                        else:
                            u2 = pairV[v]
                            if not inQ_u[u2]:
                                inQ_u[u2] = True
                                parentU[u2] = v
                                q.append(('U', u2))
                if targetV != -1:
                    break
            else:
                pass

        if targetV == -1:
            return None, parentU, parentV

        aug = []
        v = targetV
        while True:
            u = parentV[v]
            aug.append((u, v))
            if parentU[u] == -2:
                break
            v = parentU[u]
        aug.reverse()
        return aug, parentU, parentV

    while True:
        aug, parentU, parentV = bfs_find_path()
        if aug is None:
            visitedU = [False] * n
            visitedV = [False] * n
            dq = deque()
            for u in range(n):
                if pairU[u] == -1:
                    dq.append(('U', u))
                    visitedU[u] = True
            while dq:
                side, node = dq.popleft()
                if side == 'U':
                    u = node
                    for v in adjU[u]:
                        if not visitedV[v] and pairU[u] != v:
                            visitedV[v] = True
                            dq.append(('V', v))
                else:
                    v = node
                    u2 = pairV[v]
                    if u2 != -1 and not visitedU[u2]:
                        visitedU[u2] = True
                        dq.append(('U', u2))
            M = [(i, pairU[i]) for i in range(n) if pairU[i] != -1]
            reachableU = {i for i in range(n) if visitedU[i]}
            reachableV = {j for j in range(n) if visitedV[j]}
            return M, reachableU, reachableV

        for (u, v) in aug:
            if pairU[u] == v:
                pairU[u] = -1
                pairV[v] = -1
            else:
                if pairU[u] != -1:
                    oldv = pairU[u]
                    pairV[oldv] = -1
                if pairV[v] != -1:
                    oldu = pairV[v]
                    pairU[oldu] = -1
                pairU[u] = v
                pairV[v] = u

def assignment_cost(C, assignment):
    return sum(C[i][j] for (i, j) in assignment)

def hungarian():
    C = example_data()
    n = len(C)

    print("Шаг 1. Входные данные")
    print("  матрица стоимостей C =", fmt_mat(C))

    alpha = [Fraction(0) for _ in range(n)]
    beta = []
    Ct = transpose(C)
    for j in range(n):
        _, mn = argmin([Ct[j][i] for i in range(n)])
        beta.append(Fraction(mn))
    print("\nШаг 2. Начальный допустимый план двойственной задачи")
    print("  α =", fmt_vec(alpha))
    print("  β =", fmt_vec(beta))

    iter_no = 0
    while True:
        iter_no += 1
        print(f"\nИтерация {iter_no}. Формирование множеств J= и J<")
        Jeq, _ = build_Jeq(C, alpha, beta)
        print("  J= =", "[" + "; ".join(f"({i+1},{j+1})" for (i, j) in Jeq) + "]")

        print("  строим двудольный граф G по J=")
        M, Istar, Jstar = max_matching_with_reachable(n, Jeq)
        M_sorted = sorted(M)
        print("  найдено паросочетание M =", "[" + "; ".join(f"({i+1},{j+1})" for (i, j) in M_sorted) + f"]  |M|={len(M_sorted)}")

        if len(M_sorted) == n:
            print("\nШаг 3. Оптимальное назначение найдено")
            total = assignment_cost(C, M_sorted)
            print("  позиции =", "[" + "; ".join(f"(i={i+1}, j={j+1})" for (i, j) in M_sorted) + "]")
            print("  суммарная стоимость =", total)
            return

        print("\nШаг 4. Отметка достижимых вершин (из всех свободных u)")
        print("  I* =", fmt_vec([i+1 for i in sorted(Istar)]))
        print("  J* =", fmt_vec([j+1 for j in sorted(Jstar)]))

        print("\nШаг 5. Формируем знаковый план")
        alpha_sign = [Fraction(1) if i in Istar else Fraction(-1) for i in range(n)]
        beta_sign  = [Fraction(-1) if j in Jstar else Fraction(1)  for j in range(n)]
        print("  α_sign =", fmt_vec(alpha_sign))
        print("  β_sign =", fmt_vec(beta_sign))

        print("\nШаг 6. Вычисление θ")
        candidates = []
        for i in Istar:
            for j in range(n):
                if j not in Jstar:
                    val = (Fraction(C[i][j]) - alpha[i] - beta[j]) / 2
                    candidates.append((i, j, val))
        if not candidates:
            print("  нет допустимых пар (i∈I*, j∉J*) — завершение")
            return
        i_min, j_min, theta = min(candidates, key=lambda t: (t[2], t[0], t[1]))
        s_cands = ", ".join(
            f"(i={i+1},j={j+1}): (c_ij - α_i - β_j)/2 = ({C[i][j]} - {alpha[i]} - {beta[j]})/2 = {val}"
            for (i, j, val) in candidates
        )
        print("  кандидаты =", "[" + s_cands + "]")
        print(f"  θ = {theta}")

        print("\nШаг 7. Обновление текущего двойственного плана")
        alpha = [alpha[i] + theta * alpha_sign[i] for i in range(n)]
        beta  = [beta[j]  + theta * beta_sign[j]  for j in range(n)]
        print("  α ← α + θ·α_sign =", fmt_vec(alpha))
        print("  β ← β + θ·β_sign =", fmt_vec(beta))

if __name__ == "__main__":
    hungarian()
