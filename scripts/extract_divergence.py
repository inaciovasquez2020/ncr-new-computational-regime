from __future__ import annotations
import json
import argparse
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TraceState:
    count: int
    nodes: int


def load_trace(path: str) -> List[TraceState]:
    with open(path, "r") as f:
        data = json.load(f)

    trace = data.get("trace") or data.get("witness", {}).get("trace")
    if trace is None:
        raise ValueError("no trace found in certificate")

    out: List[TraceState] = []
    for s in trace:
        if "count" not in s:
            raise ValueError("trace state missing count")
        out.append(
            TraceState(
                count=int(s["count"]),
                nodes=int(s.get("nodes", 0)),
            )
        )
    return out


def find_min_divergence(a: List[TraceState], b: List[TraceState]) -> Optional[int]:
    m = min(len(a), len(b))
    for i in range(m):
        if a[i].count != b[i].count or a[i].nodes != b[i].nodes:
            return i
    if len(a) != len(b):
        return m
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True, help="ISR normalization-failure cert")
    ap.add_argument("--out", required=True, help="output cert with min divergence")
    args = ap.parse_args()

    with open(args.trace, "r") as f:
        cert = json.load(f)

    witness = cert.get("witness")
    if witness is None:
        raise ValueError("certificate has no witness section")

    traces = witness.get("traces")
    if not traces or len(traces) != 2:
        raise ValueError("expected exactly two traces in witness")

    trace_a = load_trace_from_obj(traces[0])
    trace_b = load_trace_from_obj(traces[1])

    idx = find_min_divergence(trace_a, trace_b)

    cert.setdefault("witness", {})
    cert["witness"]["min_divergence_index"] = idx
    cert["witness"]["min_divergence_reason"] = (
        "count_or_nodes_mismatch" if idx is not None else "no_divergence_detected"
    )

    with open(args.out, "w") as f:
        json.dump(cert, f, indent=2, sort_keys=True)


def load_trace_from_obj(obj) -> List[TraceState]:
    if "trace" not in obj:
        raise ValueError("trace object missing trace field")
    out: List[TraceState] = []
    for s in obj["trace"]:
        out.append(
            TraceState(
                count=int(s["count"]),
                nodes=int(s.get("nodes", 0)),
            )
        )
    return out


if __name__ == "__main__":
    main()

