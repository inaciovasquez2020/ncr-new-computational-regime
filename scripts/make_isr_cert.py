import json, pathlib

cert = {
  "meta": {
    "schema": "aiv-cert-v1",
    "claim": "ISR normalization failure",
    "expected_key_id": "",
  },
  "params": {
    "nvars": 10
  },
  "program": [
    {"op":"clause","a":[1,2,3],"b":[3,2,1]},
    {"op":"clause","a":[-1,2,3],"b":[3,2,-1]},
    {"op":"clause","a":[1,-2,3],"b":[3,-2,1]},
    {"op":"clause","a":[1,2,-3],"b":[-3,2,1]},
  ]
}

pathlib.Path("certs").mkdir(exist_ok=True)
with open("certs/ISR_NORM_FAIL_0001.json","w") as f:
    json.dump(cert,f,indent=2)

print("certs/ISR_NORM_FAIL_0001.json")
