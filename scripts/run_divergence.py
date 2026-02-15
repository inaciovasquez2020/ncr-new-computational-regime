from model.isr import ISR

def run(n=10):
    A = ISR.init_universe(n, mode="isr")
    B = ISR.init_universe(n, mode="isr")

    clauses = [
        [1,2,3],
        [-1,2,3],
        [1,-2,3],
        [1,2,-3],
    ]

    for c in clauses:
        A.apply_clause(c)
        B.apply_clause(c[::-1])

    return A, B

if __name__ == "__main__":
    A, B = run()
    print("A.state =", A.state)
    print("B.state =", B.state)
    print("A.trace =", [t.count for t in A.trace])
    print("B.trace =", [t.count for t in B.trace])
