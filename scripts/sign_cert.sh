#!/usr/bin/env bash
set -euo pipefail

CERT="$1"
HASH="${CERT%.json}.hash"
SIG="${CERT%.json}.hash.minisig"

python3 - <<PY > "$HASH"
import hashlib
with open("$CERT","rb") as f:
    print(hashlib.sha256(f.read()).hexdigest())
PY

minisign -Sm "$HASH" -s scripts/keys/active.key -x "$SIG"
