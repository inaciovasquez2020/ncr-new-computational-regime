from __future__ import annotations
import json
from model.isr import ISR

def main() -> None:
    isr = ISR.init_universe(16)
    isr.apply_clause([+1, +2, +3])
    isr.apply_clause([-1, +4])
    isr.apply_xor2(0, 1, 1)
    isr.apply_xor2(2, 3, 0)

    out = {
        "nvars": isr.nvars,
        "final_count": isr.bdd.count(isr.state),
        "final_nodes": len(isr.bdd.nodes),
        "trace": [s.__dict__ for s in isr.trace],
    }
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
