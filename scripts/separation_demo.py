from model.isr import ISR


def run_separation_demo(nvars: int = 20):
    print("ISR separation demo")
    print("nvars =", nvars)
    print()

    a = ISR.init_universe(nvars, mode="isr")
    b = ISR.init_universe(nvars, mode="isr")

    clauses = [
        [1, 2, 3],
        [-1, 4],
        [2, -5, 6],
        [-3, -4],
        [7],
        [-2, 8]
    ]

    print("Applying identical prefix")
    for c in clauses[:3]:
        a.apply_clause(c)
        b.apply_clause(c)
        print("state =", a.state)

    print()
    print("Applying sign-divergent clause")
    a.apply_clause([1, 9])
    b.apply_clause([-1, 9])

    print("A state:", a.state)
    print("B state:", b.state)
    print()

    print("Trace comparison")
    for i, (sa, sb) in enumerate(zip(a.trace, b.trace)):
        print(
            i,
            "A(count,nodes)=",
            (sa.count, sa.nodes),
            "B(count,nodes)=",
            (sb.count, sb.nodes)
        )

    print()
    print("Result")
    if a.state != b.state:
        print("separation witnessed: fast evolution, non-normalizable")
    else:
        print("no separation observed")


if __name__ == "__main__":
    run_separation_demo()

