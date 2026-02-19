#!/usr/bin/env sh
set -e

KEY_ID="RWRYSQOcAPcPGowy2ls9e2xh9XL4UP/o5nvmERf6VVP4ssYOIGGvAl2L"

for f in certs/ncr-new-computational-regime/examples/*.json; do
  minisign -Vm "$f" -P "$KEY_ID"
done

echo "NCR NEG certification verified."
