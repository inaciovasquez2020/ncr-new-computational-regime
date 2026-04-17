#!/usr/bin/env python3
from pathlib import Path
import sys

required = [
    "README.md",
    "CITATION.cff",
    "docs",
    "infra",
    "manuscript",
    "model",
    "schema",
    "scripts",
    "tests",
    "certs",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print({"valid": False, "missing": missing})
    sys.exit(1)

readme = Path("README.md").read_text(errors="ignore").lower()

checks = {
    "mentions_ncr_or_isr": (
        "new computational regime" in readme or "ncr" in readme or "isr" in readme
    ),
    "mentions_normalization_resistance": "normalization" in readme,
    "mentions_scope_boundary": (
        "does not" in readme and "p vs np" in readme
    ),
    "mentions_non_certified_boundary": (
        "non-certified" in readme or "non certified" in readme
    ),
    "mentions_decision_diagram_model": (
        "decision diagram" in readme or "decision-diagram" in readme
    ),
}

failed = [k for k, v in checks.items() if not v]
if failed:
    print({"valid": False, "failed_checks": failed, "checks": checks})
    sys.exit(1)

print({"valid": True, "checked": required, "checks": checks})
