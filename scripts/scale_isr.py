from __future__ import annotations
import csv
import json
import math
from dataclasses import asdict
from typing import Dict, Any, List, Tuple
from model.isr import ISR

def ladder_xor_family(n: int) -> Tuple[ISR, List[Dict[str, Any]]]:
    isr = ISR.init_universe(n)
    for i in range(n - 1):
        isr.apply_xor2(i, i + 1, (i & 1))
    for i in range(0, n, 3):
        a = i + 1
        b = (i + 2) % n + 1
        c = (i + 3) % n + 1
        isr.apply_clause([+a, -b, +c])
    trace = [s.__dict__ for s in isr.trace]
    return isr, trace

def summarize(isr: ISR) -> Dict[str, Any]:
    cnt = isr.bdd.count(isr.state)
    nodes = len(isr.bdd.nodes)
    p0 = float("-inf") if cnt <= 0 else math.log2(cnt)
    steps = max(0, len(isr.trace) - 1)
    return {"n": isr.nvars, "final_count": cnt, "final_nodes": nodes, "final_p0": p0, "steps": steps}

def main() -> None:
    Ns = [16, 24, 32, 40, 48, 64, 80, 96, 128]
    rows = []
    traces_dir = "data/traces"
    import os
    os.makedirs(traces_dir, exist_ok=True)

    for n in Ns:
        isr, trace = ladder_xor_family(n)
        summ = summarize(isr)
        rows.append(summ)
        out = {"n": n, "summary": summ, "trace": trace}
        with open(f"{traces_dir}/isr_trace_n{n}.json", "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)

    with open("data/scale_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n", "final_count", "final_nodes", "final_p0", "steps"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    def slope(xs, ys):
        lx = [math.log(x) for x in xs]
        ly = [math.log(max(y, 1e-12)) for y in ys]
        mx = sum(lx)/len(lx); my = sum(ly)/len(ly)
        num = sum((a-mx)*(b-my) for a,b in zip(lx,ly))
        den = sum((a-mx)*(a-mx) for a in lx)
        return num/den if den != 0 else float("nan")

    Ns2 = [r["n"] for r in rows]
    p0s = [max(r["final_p0"], 1e-12) for r in rows]
    nodes = [max(r["final_nodes"], 1e-12) for r in rows]
    out2 = {
        "Ns": Ns2,
        "p0": p0s,
        "nodes": nodes,
        "loglog_slope_p0_vs_n": slope(Ns2, p0s),
        "loglog_slope_nodes_vs_n": slope(Ns2, nodes),
    }
    with open("data/scale_fit.json", "w") as f:
        json.dump(out2, f, indent=2, sort_keys=True)

    print(json.dumps(out2, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
