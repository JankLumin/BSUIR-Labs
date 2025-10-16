def example_data():
    V1 = ["a", "b", "c"]
    V2 = ["x", "y", "z"]
    E = [
        ("a", "x"),
        ("b", "x"),
        ("b", "y"),
        ("c", "y"),
        ("c", "z"),
    ]
    return V1, V2, E


def fmt_list(xs):
    return "[" + "; ".join(xs) + "]"


def path_str(p):
    return " -> ".join(p)


def build_G_star(V1, V2, E):
    s, t = "s", "t"
    G = {s: set(), t: set()}
    for u in V1 + V2:
        G[u] = set()
    for u in V1:
        G[s].add(u)
    for v in V2:
        G[v].add(t)
    for u, v in E:
        G[u].add(v)
    return G, s, t


def bfs_path(G, s, t):
    from collections import deque

    q = deque([s])
    prev = {s: None}
    while q:
        u = q.popleft()
        if u == t:
            break
        for w in G.get(u, ()):
            if w not in prev:
                prev[w] = u
                q.append(w)
    if t not in prev:
        return None
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def remove_arc(G, u, v):
    if u in G and v in G[u]:
        G[u].remove(v)


def add_arc(G, u, v):
    if u not in G:
        G[u] = set()
    G[u].add(v)


def arcs_between(G, A, B):
    res = []
    for u in A:
        for v in G[u]:
            if v in B:
                res.append((u, v))
    return res


def print_arc_orientation(G, V1, V2):
    ab = arcs_between(G, V1, V2)
    ba = arcs_between(G, V2, V1)
    if ab:
        print("  дуги V1→V2:", "[" + "; ".join(f"({u}->{v})" for u, v in ab) + "]")
    else:
        print("  дуги V1→V2:", "[]")
    if ba:
        print("  дуги V2→V1:", "[" + "; ".join(f"({v}->{u})" for v, u in ba) + "]")
    else:
        print("  дуги V2→V1:", "[]")


def matching_from_Gstar(G, V1, V2):
    M = []
    for v in V2:
        for u in G[v]:
            if u in V1:
                M.append((u, v))
    return M


def bipartite_matching():
    V1, V2, E = example_data()

    print("Шаг 1. Входные данные")
    print("  доля V1 =", fmt_list(V1))
    print("  доля V2 =", fmt_list(V2))
    print("  рёбра G =", "[" + "; ".join(f"{{{u},{v}}}" for u, v in E) + "]")

    print("\nШаг 2. Построение ориентированного графа G*")
    G, s, t = build_G_star(V1, V2, E)
    print("  добавлены вершины s и t")
    print("  дуги из s в V1:", "[" + "; ".join(f"(s->{u})" for u in V1) + "]")
    print("  дуги из V2 в t:", "[" + "; ".join(f"({v}->t)" for v in V2) + "]")
    print_arc_orientation(G, V1, V2)

    it = 0
    while True:
        it += 1
        print(f"\nШаг 3. Поиск (s,t)-пути, итерация {it}")
        P = bfs_path(G, s, t)
        if P is None:
            print("  путь не найден")
            print("\nШаг 4. Завершение")
            M = matching_from_Gstar(G, V1, V2)
            M_sorted = sorted(M, key=lambda e: (V1.index(e[0]), V2.index(e[1])))
            print(
                "  дуги V2→V1 в финальном G*:",
                "[" + "; ".join(f"({v}->{u})" for u, v in M_sorted) + "]",
            )
            print(
                "  максимальное паросочетание:",
                "[" + "; ".join(f"{{{u},{v}}}" for u, v in M_sorted) + "]",
            )
            print(f"  мощность |M| = {len(M_sorted)}")
            return

        print("  найден путь:", path_str(P))

        if len(P) < 4:
            print("  путь недостаточной длины для улучшения, прекращаем")
            print("\nШаг 4. Завершение")
            M = matching_from_Gstar(G, V1, V2)
            M_sorted = sorted(M, key=lambda e: (V1.index(e[0]), V2.index(e[1])))
            print(
                "  дуги V2→V1 в финальном G*:",
                "[" + "; ".join(f"({v}->{u})" for u, v in M_sorted) + "]",
            )
            print(
                "  максимальное паросочетание:",
                "[" + "; ".join(f"{{{u},{v}}}" for u, v in M_sorted) + "]",
            )
            print(f"  мощность |M| = {len(M_sorted)}")
            return

        print("\nШаг 5. Корректировка G* по найденному пути")
        u0, u1 = P[0], P[1]
        vL_1, vL = P[-2], P[-1]
        print(f"  удаляем крайние дуги: ({u0}->{u1}) и ({vL_1}->{vL})")
        remove_arc(G, u0, u1)
        remove_arc(G, vL_1, vL)

        middle = []
        for i in range(1, len(P) - 2):
            x, y = P[i], P[i + 1]
            middle.append((x, y))
        if middle:
            print(
                "  обращаем ориентацию промежуточных дуг:",
                "[" + "; ".join(f"({x}->{y})" for x, y in middle) + "]",
            )
        for x, y in middle:
            remove_arc(G, x, y)
            add_arc(G, y, x)

        print("  итоговая ориентация дуг между долями")
        print_arc_orientation(G, V1, V2)


if __name__ == "__main__":
    bipartite_matching()
