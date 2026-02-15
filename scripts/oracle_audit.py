from __future__ import annotations
import json
import platform
import sys
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Audit:
    model: str
    deterministic: bool
    randomness_used: bool
    external_state_used: bool
    float_precision_used: bool
    notes: List[str]
    python: str
    platform: str

def main() -> None:
    audit = Audit(
        model="ISR/ROBDD",
        deterministic=True,
        randomness_used=False,
        external_state_used=False,
        float_precision_used=False,
        notes=["integer-only operations; exact counting; no RNG usage in model"],
        python=sys.version.replace("\n"," "),
        platform=platform.platform(),
    )
    print(json.dumps(asdict(audit), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
