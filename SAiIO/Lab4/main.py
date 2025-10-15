from fractions import Fraction


def example_data():
    v = [2, 3, 4, 5]
    c = [3, 4, 5, 8]
    B = 8
    return v, c, B


def fmt_q(q):
    return (
        str(q)
        if not isinstance(q, Fraction) or q.denominator != 1
        else str(q.numerator)
    )


def fmt_vec(v):
    return "[" + "; ".join(fmt_q(x) for x in v) + "]"


def fmt_mat(M):
    return "[\n  " + "\n  ".join(fmt_vec(row) for row in M) + "\n]"


def knapsack():
    v, c, B = example_data()
    n = len(v)

    print("Шаг 1. Входные данные")
    print("  количество предметов n =", n, "вместимость B =", B)
    print("  объёмы v =", fmt_vec(v))
    print("  ценности c =", fmt_vec(c))

    OPT = [[0] * (B + 1) for _ in range(n)]
    X = [[0] * (B + 1) for _ in range(n)]

    print("\nШаг 2. Заполнение строки k = 1")
    k = 1
    for b in range(B + 1):
        if v[0] <= b:
            OPT[0][b] = c[0]
            X[0][b] = 1
            print(f"  b = {b}: v1={v[0]} ≤ b ⇒ OPT(1,{b}) = c1 = {c[0]}, x(1,{b}) = 1")
        else:
            OPT[0][b] = 0
            X[0][b] = 0
            print(f"  b = {b}: v1={v[0]} > b ⇒ OPT(1,{b}) = 0, x(1,{b}) = 0")
    print("  OPT(1, ·) =", fmt_vec(OPT[0]))
    print("  x(1, ·) =", fmt_vec(X[0]))

    step = 3
    for k in range(2, n + 1):
        print(f"\nШаг {step}. Заполнение строки k = {k}")
        for b in range(B + 1):
            not_take = OPT[k - 2][b]
            if v[k - 1] <= b:
                take = OPT[k - 2][b - v[k - 1]] + c[k - 1]
                chosen = "выбрать k" if take > not_take else "не выбирать k"
                if take > not_take:
                    OPT[k - 1][b] = take
                    X[k - 1][b] = 1
                else:
                    OPT[k - 1][b] = not_take
                    X[k - 1][b] = 0
                print(
                    f"  b = {b}: max(OPT({k-1},{b})={not_take}, OPT({k-1},{b}-{v[k-1]})+c{k}={OPT[k-2][b - v[k-1]]}+{c[k-1]}={take}) ⇒ {chosen}, OPT({k},{b}) = {OPT[k-1][b]}, x({k},{b}) = {X[k-1][b]}"
                )
            else:
                OPT[k - 1][b] = not_take
                X[k - 1][b] = 0
                print(
                    f"  b = {b}: v{k}={v[k-1]} > b ⇒ OPT({k},{b}) = OPT({k-1},{b}) = {not_take}, x({k},{b}) = 0"
                )
        print(f"  OPT({k}, ·) =", fmt_vec(OPT[k - 1]))
        print(f"  x({k}, ·) =", fmt_vec(X[k - 1]))
        step += 1

    print(f"\nШаг {step}. Максимальная суммарная ценность")
    print("  OPT(n, B) =", OPT[n - 1][B])
    step += 1

    print(f"\nШаг {step}. Обратный ход")
    x = [0] * n
    used_capacity = 0
    b_cur = B
    for k in range(n, 0, -1):
        choose = X[k - 1][b_cur]
        x[k - 1] = choose
        if choose == 1:
            print(
                f"  k = {k}, b = {b_cur}: x{k} = 1, берём предмет k, v{k} = {v[k-1]}, c{k} = {c[k-1]}, новый b → {b_cur - v[k-1]}"
            )
            used_capacity += v[k - 1]
            b_cur -= v[k - 1]
        else:
            print(f"  k = {k}, b = {b_cur}: x{k} = 0, предмет k не берём")
    total_value = sum(c[i] * x[i] for i in range(n))

    print("\nИтоговое решение")
    print("  вектор решений x =", fmt_vec(x))
    print("  использованный объём =", used_capacity, "из", B)
    print("  суммарная ценность =", total_value)


if __name__ == "__main__":
    knapsack()
