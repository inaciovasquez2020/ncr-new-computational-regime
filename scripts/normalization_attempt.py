from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List
from model.isr import ISR

def token(state_id: int, nodes: int, count: int, bits: int) -> str:
    # transcript token: hash of (state_id, nodes, count) truncated to bits
    m = hashlib.sha256(f"{state_id}|{nodes}|{count}".encode()).hexdigest()
    hex_len = max(1, bits // 4)
    return m[:hex_len]

@dataclass
class CollisionWitness:
    bits_per_step: int
    step_a: int
    step_b: int
    token: str
    a_detail: str
    b_detail: str
    a_count: int
    b_count: int
    divergence_next: bool

def main() -> None:
    # Build two traces designed to collide under small transcript budgets
    bits = 12

    def build_trace(seed_variant: int) -> ISR:
        isr = ISR.init_universe(20)
        if seed_variant == 0:
            isr.apply_clause([+1, +2, +3])
            isr.apply_clause([-1, +4])
            isr.apply_xor2(0, 1, 1)
            isr.apply_clause([+5, -6, +7])
        else:
            isr.apply_clause([+1, +2, +3])
            isr.apply_clause([-1, +4])
            isr.apply_xor2(0, 1, 1)
            isr.apply_clause([-5, +6, +7])
        return isr

    A = build_trace(0)
    B = build_trace(1)

    # transcript at each step
    toksA: List[str] = []
    toksB: List[str] = []
    for s in A.trace:
        toksA.append(token(A.state, s.nodes, s.count, bits))
    for s in B.trace:
        toksB.append(token(B.state, s.nodes, s.count, bits))

    # search collision across steps
    table: Dict[str, Tuple[str,int,int]] = {}
    witness: CollisionWitness | None = None

    for i, s in enumerate(A.trace):
        t = token(A.state, s.nodes, s.count, bits)
        table[t] = ("A", i, s.count)

    for j, s in enumerate(B.trace):
        t = token(B.state, s.nodes, s.count, bits)
        if t in table:
            src, i, ci = table[t]
            if src == "A" and (ci != s.count):
                witness = CollisionWitness(
                    bits_per_step=bits,
                    step_a=i,
                    step_b=j,
                    token=t,
                    a_detail=A.trace[i].detail,
                    b_detail=s.detail,
                    a_count=ci,
                    b_count=s.count,
                    divergence_next=True,
                )
                break

    out = {
        "ok": witness is not None,
        "witness": asdict(witness) if witness else None,
        "note": "Collision witness is a normalization-failure certificate for transcript budget bits_per_step.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
