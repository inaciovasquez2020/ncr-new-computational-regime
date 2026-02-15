#!/usr/bin/env bash
set -euo pipefail

CERT="$1"
HASH="${CERT%.json}.hash"
SIG="${CERT%.json}.hash.minisig"

EXPECTED=$(jq -r '.meta.expected_key_id' "$CERT")
PUB_KID=$(minisign -p scripts/keys/active.pub -Q | sed -n 's/.*Key ID: //p')

if [[ "$EXPECTED" != "$PUB_KID" ]]; then
  echo "ERROR: expected KeyID $EXPECTED, verifier uses $PUB_KID"
  exit 1
fi

minisign -Vm "$HASH" -x "$SIG" -p scripts/keys/active.pub
