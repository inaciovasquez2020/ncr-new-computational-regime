import json, sys
from model.isr import ISR

cert = json.load(open(sys.argv[1]))

A = ISR.init_universe(cert["params"]["nvars"], mode="isr")
B = ISR.init_universe(cert["params"]["nvars"], mode="isr")

for step in cert["program"]:
    if step["op"] == "clause":
        A.apply_clause(step["a"])
        B.apply_clause(step["b"])

if A.state == B.state:
    print("no divergence; invariant not witnessed")
    sys.exit(1)

print("DIVERGENCE WITNESSED")
print("A.state =", A.state)
print("B.state =", B.state)
