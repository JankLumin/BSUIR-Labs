def example_data():
    L = [
        [None, None, None, None, None, None, None],
        [None, None, 2,    1,    None, None, None],
        [None, None, None, None, 3,    2,    None],
        [None, None, None, None, 5,    None, None],
        [None, None, None, None, None, None, 4   ],
        [None, None, None, None, None, None, 6   ],
        [None, None, None, None, None, None, None],
    ]
    n = 6
    k = 1
    ell = 6
    return n, L, k, ell


def fmt_vec(v):
    return "[" + "; ".join(v) + "]"


def fmt_vertices(n):
    return ["v" + str(i) for i in range(1, n + 1)]


def fmt_pred_list(preds):
    return "[" + "; ".join("v" + str(p) for p in preds) + "]" if preds else "[]"


def fmt_candidates(cands):
    return "[" + ", ".join(cands) + "]" if cands else "[]"


def neg_inf():
    return float("-inf")


def fmt_val(x):
    return "-∞" if x == float("-inf") else str(x)


def path_to_str(path):
    return " -> ".join("v" + str(i) for i in path)


def longest_path_dag():
    n, L, k, ell = example_data()

    print("Шаг 1. Входные данные")
    print("  число вершин n =", n)
    print("  топологический порядок V =", fmt_vec(fmt_vertices(n)))
    print("  выделенные вершины: s = v%d, t = v%d" % (k, ell))
    edges = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if L[i][j] is not None:
                edges.append(f"(v{i}→v{j}, ℓ={L[i][j]})")
    print("  дуги и длины =", "[" + "; ".join(edges) + "]")

    print("\nШаг 2. Предварительная проверка порядка s и t")
    if k > ell:
        print("  k >", "ℓ ⇒ все дуги слева направо, t недостижима из s")
        return
    if k == ell:
        print("  k = ℓ ⇒ s = t, длина пути 0, маршрут: v%d" % k)
        return
    print("  k <", "ℓ ⇒ продолжаем динамическое программирование")

    print("\nШаг 3. Прямой ход: вычисляем OPT(vi) для i = k..ℓ")
    OPT = [neg_inf()] * (n + 1)
    X = [None] * (n + 1)
    OPT[k] = 0
    X[k] = None
    print("  OPT(v%d) = 0" % k)
    for i in range(k + 1, ell + 1):
        preds = [p for p in range(k, i) if L[p][i] is not None]
        cand_str = []
        best_val = neg_inf()
        best_p = None
        for p in preds:
            val = OPT[p]
            if val != neg_inf():
                cur = val + L[p][i]
                cand_str.append(
                    f"v{p}→v{i}: OPT(v{p})+ℓ={fmt_val(val)}+{L[p][i]}={cur}"
                )
                if cur > best_val:
                    best_val = cur
                    best_p = p
            else:
                cand_str.append(
                    f"v{p}→v{i}: OPT(v{p})+ℓ={fmt_val(val)}+{L[p][i]}={fmt_val(neg_inf())}"
                )
        print(f"  v{i}: предшественники =", fmt_pred_list(preds))
        print("    варианты =", fmt_candidates(cand_str))
        if not preds or best_p is None:
            OPT[i] = neg_inf()
            X[i] = None
            print(f"    OPT(v{i}) = -∞, x(v{i}) = —")
        else:
            OPT[i] = best_val
            X[i] = best_p
            print(f"    OPT(v{i}) = {best_val}, x(v{i}) = v{best_p}")

    print("\nШаг 4. Максимальная длина пути")
    if OPT[ell] == neg_inf():
        print("  OPT(t) = -∞ ⇒ (s,t)-пути не существует")
        return
    else:
        print("  OPT(t) =", OPT[ell])

    print("\nШаг 5. Обратный ход: восстановление пути")
    path = []
    cur = ell
    while cur is not None and cur != k:
        path.append(cur)
        cur = X[cur]
    path.append(k)
    path = list(reversed(path))
    print("  маршрут =", path_to_str(path))
    print("  длина =", OPT[ell])


if __name__ == "__main__":
    longest_path_dag()
