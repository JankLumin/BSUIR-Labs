from collections import deque


def example_data():
    V = ["s", "a", "b", "t"]
    A = [
        ("s", "a", 3),
        ("s", "b", 2),
        ("a", "b", 2),
        ("a", "t", 1),
        ("b", "t", 2),
        ("a", "s", 0),
        ("b", "s", 0),
        ("b", "a", 0),
        ("t", "a", 0),
        ("t", "b", 0),
    ]
    s = "s"
    t = "t"
    return V, A, s, t


def fmt_vec(v):
    return "[" + "; ".join(v) + "]"


def fmt_arcs(arcs):
    return "[" + "; ".join(f"({u}→{v}, c={c})" for u, v, c in arcs) + "]"


def build_capacities(V, A):
    C = {u: {} for u in V}
    for u, v, c in A:
        C[u][v] = c
    for u in V:
        for v in V:
            if u == v:
                continue
            if v not in C[u]:
                C[u][v] = 0
    return C


def build_flow(V):
    F = {u: {} for u in V}
    for u in V:
        for v in V:
            F[u][v] = 0
    return F


def residual_capacity(u, v, C, F):
    return C[u][v] - F[u][v] + F[v][u]


def build_residual_nonzero(V, C, F):
    R = []
    for u in V:
        for v in V:
            if u == v:
                continue
            cf = residual_capacity(u, v, C, F)
            if cf > 0:
                R.append((u, v, cf))
    return R


def label_bfs(V, C, F, s, t):
    parent = {v: None for v in V}
    q = deque()
    q.append(s)
    parent[s] = ("SRC", None)
    while q:
        v = q.popleft()
        for u in V:
            if u == v:
                continue
            if parent[u] is not None:
                continue
            cf = residual_capacity(v, u, C, F)
            if cf > 0:
                parent[u] = (v, cf)
                if u == t:
                    path = []
                    cur = t
                    theta = None
                    while True:
                        pv, cf_e = parent[cur]
                        if pv == "SRC":
                            break
                        path.append((pv, cur))
                        theta = cf_e if theta is None else min(theta, cf_e)
                        cur = pv
                    path.reverse()
                    return True, path, theta, parent
                q.append(u)
    return False, [], 0, parent


def apply_augmentation(path, theta, C, F):
    for u, v in path:
        forward_res = C[u][v] - F[u][v]
        if forward_res > 0:
            F[u][v] += theta
        else:
            F[v][u] -= theta


def flow_value(F, s):
    return sum(F[s].values())


def min_cut_from_labels(parent):
    X = [v for v, p in parent.items() if p is not None]
    return X


def main():
    V, A, s, t = example_data()
    print("Шаг 1. Входные данные")
    print("  вершины =", fmt_vec(V))
    print("  дуги с пропускными способностями =", fmt_arcs(A))
    C = build_capacities(V, A)
    F = build_flow(V)
    print("\nШаг 2. Инициализация нулевого потока")
    print("  f(a) = 0 для всех дуг")
    it = 0
    while True:
        it += 1
        print(f"\nШаг 3. Построение вспомогательной сети Gf, итерация {it}")
        R = build_residual_nonzero(V, C, F)
        print(
            "  ненулевые дуги Gf =",
            "[" + "; ".join(f"({u}→{v}, cf={cf})" for u, v, cf in R) + "]",
        )
        print("\nШаг 4. Поиск (s,t)-пути методом пометок")
        found, path, theta, parent = label_bfs(V, C, F, s, t)
        if not found:
            print("  путь не найден")
            X = min_cut_from_labels(parent)
            print("  множество достижимых вершин X =", fmt_vec(X))
            print("  максимальный поток =", flow_value(F, s))
            all_flow_arcs = []
            for u in V:
                for v in V:
                    if u != v and (F[u][v] != 0 or C[u][v] != 0):
                        all_flow_arcs.append((u, v, F[u][v], C[u][v]))
            all_flow_arcs_s = (
                "["
                + "; ".join(f"({u}→{v}: {f}/{c})" for u, v, f, c in all_flow_arcs)
                + "]"
            )
            print("  поток на дугах (f/c) =", all_flow_arcs_s)
            return
        path_str = " -> ".join([s] + [v for _, v in path])
        print(f"  найден путь: {path_str}")
        print(f"  θ = min cf по дугам пути = {theta}")
        print("\nШаг 5. Увеличение потока вдоль пути на θ")
        before = flow_value(F, s)
        apply_augmentation(path, theta, C, F)
        after = flow_value(F, s)
        print(
            "  обновлённый поток на дугах пути = "
            + "["
            + "; ".join(f"({u}→{v}: +{theta})" for u, v in path)
            + "]"
        )
        print(f"  мощность потока: было {before} → стало {after}")
        print("\nШаг 6. Обновление пропускных способностей во вспомогательной сети")
        R2 = build_residual_nonzero(V, C, F)
        print(
            "  новые ненулевые дуги Gf =",
            "[" + "; ".join(f"({u}→{v}, cf={cf})" for u, v, cf in R2) + "]",
        )
        print("\nШаг 7. Переход к следующему поиску (s,t)-пути")


if __name__ == "__main__":
    main()
