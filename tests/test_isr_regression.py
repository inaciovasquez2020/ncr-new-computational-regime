from model.isr import ISR


def test_isr_regression_basic_determinism():
    a = ISR.init_universe(10, mode="isr")
    b = ISR.init_universe(10, mode="isr")

    a.apply_clause([1, 2, 3])
    b.apply_clause([1, 2, 3])

    a.apply_clause([-1, 4])
    b.apply_clause([-1, 4])

    assert a.state == b.state
    assert [s.count for s in a.trace] == [s.count for s in b.trace]
    assert [s.nodes for s in a.trace] == [s.nodes for s in b.trace]


def test_isr_regression_sign_sensitivity():
    a = ISR.init_universe(10, mode="isr")
    b = ISR.init_universe(10, mode="isr")

    a.apply_clause([1, 2, 3])
    b.apply_clause([-1, 2, 3])

    assert a.state != b.state
    assert a.trace[-1].count != b.trace[-1].count or \
           a.trace[-1].nodes != b.trace[-1].nodes


def test_isr_regression_xor_effect():
    a = ISR.init_universe(12, mode="isr")
    b = ISR.init_universe(12, mode="isr")

    a.apply_clause([1, 2, 3])
    b.apply_clause([1, 2, 3])

    a.apply_xor2(0, 1, 1)
    b.apply_xor2(0, 1, 0)

    assert a.state != b.state
    assert a.trace[-1].count != b.trace[-1].count or \
           a.trace[-1].nodes != b.trace[-1].nodes


def test_isr_trace_monotonicity():
    a = ISR.init_universe(14, mode="isr")

    for clause in ([1, 2], [-3, 4], [5, -6], [7]):
        a.apply_clause(clause)

    counts = [s.count for s in a.trace]
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))


def test_isr_trace_structural_presence():
    a = ISR.init_universe(8, mode="isr")
    a.apply_clause([1])
    a.apply_xor2(0, 1, 1)

    for s in a.trace:
        assert hasattr(s, "count")
        assert hasattr(s, "nodes")

