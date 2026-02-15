# ISR as a Normalization-Resistant Polynomial Regime

## Abstract
We exhibit an explicit executable regime (ISR) whose updates are polynomial-time and locally specified, yet whose traces resist normalization into a bounded-per-step transcript model. The obstruction is witnessed by an automated normalization attempt that fails reproducibly and can be packaged as a signed certificate.

## 1. Setup
A normalization procedure seeks to map an execution trace to a canonical transcript under a fixed per-step budget (bits per step). We treat “URF-admissible transcript” as any transcript model that is:
- deterministic under fixed inputs,
- local/refinement-style,
- bounded in per-step information.

## 2. The ISR regime
ISR maintains an internal state and a structural trace consisting of at least:
- `count`: a proxy for surviving state-space mass,
- `nodes`: a proxy for internal representation complexity.

ISR updates are deterministic and run in time polynomial in the parameter size. A mode toggle distinguishes:
- `urf`: purely structural updates (baseline),
- `isr`: structural updates with an additional collision-inducing perturbation that is still deterministic but defeats transcript injectivity under fixed budget.

## 3. Barrier viewpoint
Define a proxy invariant `P` capturing implicit dimension / complexity of the evolving state. A URF-style refinement transcript with bounded information per step can only decrease uncertainty at a bounded rate, yielding an upper bound on per-step entropy loss. ISR traces can be constructed to collide under budgeted transcripts while diverging in internal evolution, producing a normalization obstruction.

## 4. Executable witness
The repository provides an executable normalization attempt:
- `scripts/normalization_attempt.py`

The attempt outputs a structured verdict (`ok: false`) and (when configured) a witness object pinpointing the collision/divergence mechanism. The failure is deterministic and CI-reproducible.

## 5. Regime separation claim (structural)
ISR demonstrates a separation between:
- *execution feasibility* (the regime runs efficiently and deterministically),
and
- *normalization feasibility* (a bounded-per-step transcript cannot preserve injective trace reconstruction).

This is a “normalization-resistant polynomial regime” phenomenon: efficient computation whose reasoning trace cannot be compressed into the targeted transcript class without losing distinguishing information.

## 6. Reproducibility
All claims in this note are tied to executable artifacts and CI logs in the repository. The intended next step is to freeze a signed witness certificate once the witness extractor is tightened to emit a minimal divergence index and transcript collision record.


