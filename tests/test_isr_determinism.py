from model.isr import ISR

def test_isr_deterministic_trace():
    a = ISR.init_universe(12)
    a.apply_clause([+1, +2, +3])
    a.apply_clause([-1, +4])
    a.apply_xor2(0, 1, 1)

    b = ISR.init_universe(12)
    b.apply_clause([+1, +2, +3])
    b.apply_clause([-1, +4])
    b.apply_xor2(0, 1, 1)

    assert [s.count for s in a.trace] == [s.count for s in b.trace]
    assert [s.nodes for s in a.trace] == [s.nodes for s in b.trace]
