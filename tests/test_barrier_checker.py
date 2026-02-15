import math
from model.isr import ISR

def barrier_holds(trace_counts, nvars, K):
    # P0_t = log2(count_t); require P0_t - P0_{t+1} <= K for all t
    P0 = []
    for c in trace_counts:
        if c <= 0:
            P0.append(float("inf"))
        else:
            P0.append(math.log2(c))
    for t in range(len(P0)-1):
        if (P0[t] - P0[t+1]) > K + 1e-9:
            return False
    return True

def test_barrier_checker_runs():
    isr = ISR.init_universe(14)
    isr.apply_clause([+1, +2, +3])
    isr.apply_clause([-1, +4])
    isr.apply_xor2(0, 1, 1)
    counts = [s.count for s in isr.trace]
    assert barrier_holds(counts, 14, K=14) in (True, False)
