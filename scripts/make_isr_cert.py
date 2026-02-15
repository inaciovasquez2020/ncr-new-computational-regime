import json, pathlib
from model.isr import ISR

nvars = 10

A = ISR.init_universe(nvars, mode="isr")
B = ISR.init_universe(nvars, mode="isr")

program = [
    {"op":"clause","a":[1,2,3],"b":[3,2,1]},
    {"op":"clause","a":[-1,2,3],"b":[3,2,-1]},
    {"op":"clause","a":[1,-2,3],"b":[3,-2,1]},
    {"op":"clause","a":[1,2,-3],"b":[-3,2,1]},
]

for step in program:
    if step["op"] == "clause":
        A.apply_clause(step["a"])
        B.apply_clause(step["b"])

def pack(isr):
    return {
        "trace": [
            {"count": s.count, "nodes": s.nodes}
            for s in isr.trace
        ]
    }

cert = {
    "meta": {
        "schema": "aiv-cert-v1",
        "claim": "ISR normalization failure",
        "expected_key_id": "",
    },
    "params": {
        "nvars": nvars
    },
    "program": program,
    "witness": {
        "traces": [pack(A), pack(B)]
    }
}

pathlib.Path("certs").mkdir(exist_ok=True)
with open("certs/ISR_NORM_FAIL_0001.json","w") as f:
    json.dump(cert,f,indent=2,sort_keys=True)

print("certs/ISR_NORM_FAIL_0001.json")

