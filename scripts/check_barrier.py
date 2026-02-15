from __future__ import annotations
import json
import math
import sys
from typing import Any, Dict, List

def p0(count: int) -> float:
    if count <= 0:
        return float("inf")
    return math.log2(count)

def check_use_lb(counts: List[int], K: float) -> Dict[str, Any]:
    P = [p0(c) for c in counts]
    worst = -float("inf")
    worst_t = None
    for t in range(len(P)-1):
        d = P[t] - P[t+1]
        if d > worst:
            worst = d
            worst_t = t
        if d > K + 1e-12:
            return {
                "ok": False,
                "K": K,
                "violation_step": t,
                "delta": d,
                "p0_t": P[t],
                "p0_t1": P[t+1],
                "count_t": counts[t],
                "count_t1": counts[t+1],
                "worst_delta": worst,
                "worst_step": worst_t,
            }
    return {
        "ok": True,
        "K": K,
        "worst_delta": worst,
        "worst_step": worst_t,
        "steps": max(0, len(P)-1),
    }

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 scripts/check_barrier.py <trace.json> [K]")
    path = sys.argv[1]
    K = float(sys.argv[2]) if len(sys.argv) >= 3 else 8.0
    obj = json.load(open(path, "r"))
    counts = [int(s["count"]) for s in obj["trace"]]
    out = check_use_lb(counts, K)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
