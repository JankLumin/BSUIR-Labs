def example_data():
    A = [
        [0, 1, 2, 3],
        [0, 0, 1, 2],
        [0, 2, 2, 3],
    ]
    return A


def fmt_vec(v):
    return "[" + "; ".join(str(x) for x in v) + "]"


def fmt_mat(M):
    return "[\n  " + "\n  ".join(fmt_vec(row) for row in M) + "\n]"


def resource_allocation():
    A = example_data()
    P = len(A)
    Q = len(A[0]) - 1

    print("Шаг 1. Входные данные")
    print("  P =", P, " Q =", Q)
    print("  A =", fmt_mat(A))

    B = [[0] * (Q + 1) for _ in range(P)]
    C = [[0] * (Q + 1) for _ in range(P)]

    print("\nШаг 2. Заполнение строки p = 1")
    for q in range(Q + 1):
        B[0][q] = A[0][q]
        C[0][q] = q
        print(f"  q = {q}: B(1,{q}) = A1[{q}] = {A[0][q]}  ⇒  выбираем i* = {q}")
    print("  B(1, ·) =", fmt_vec(B[0]))
    print("  C(1, ·) =", fmt_vec(C[0]))

    step = 3
    for p in range(2, P + 1):
        print(f"\nШаг {step}. Заполнение строки p = {p}")
        for q in range(Q + 1):
            best_val = None
            best_i = 0
            parts = []
            for i in range(q + 1):
                val = A[p - 1][i] + B[p - 2][q - i]
                parts.append(f"{i}:{val}")
                if best_val is None or val > best_val:
                    best_val = val
                    best_i = i
            B[p - 1][q] = best_val
            C[p - 1][q] = best_i
            print(
                f"  q = {q}: варианты i=0..{q} → [{', '.join(parts)}]  ⇒  i* = {best_i}, B({p},{q}) = {best_val}"
            )
        print(f"  B({p}, ·) =", fmt_vec(B[p - 1]))
        print(f"  C({p}, ·) =", fmt_vec(C[p - 1]))
        step += 1

    print(f"\nШаг {step}. Максимальная прибыль")
    print("  B(P, Q) =", B[P - 1][Q])
    step += 1

    print(f"\nШаг {step}. Обратный ход")
    allocation = [0] * P
    contribs = [0] * P
    p = P
    q = Q
    while p > 0:
        give = C[p - 1][q]
        allocation[p - 1] = give
        gain = A[p - 1][give]
        contribs[p - 1] = gain
        print(
            f"  p = {p}, q = {q}: x{p} = {give}, вклад = A{p}[{give}] = {gain}, остаток ресурса → {q - give}"
        )
        q -= give
        p -= 1

    print("\nШаг", step + 1, "Проверка результата")
    print("  сумма x =", sum(allocation), "из", Q)
    print("  сумма вкладов =", sum(contribs), "должна равняться B(P,Q) =", B[P - 1][Q])

    print("\nИтоговое распределение")
    print("  x =", fmt_vec(allocation))
    print("  вклад по проектам =", fmt_vec(contribs))
    print("  суммарная прибыль =", B[P - 1][Q])


if __name__ == "__main__":
    resource_allocation()
