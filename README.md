[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18651031.svg)](https://doi.org/10.5281/zenodo.18651031)

# NCR — New Computational Regime (ISR)

This repository documents the **New Computational Regime (NCR)** based on the **Implicit Superposition Register (ISR)** model.

ISR is a discrete, deterministic computational model whose state is a reduced ordered decision diagram representing an exponentially large set of assignments. Updates apply constraints by symbolic conjunction, without enumerating assignments.

The regime is designed to study **normalization-resistant computation**: systems where standard polynomial normalization techniques fail structurally.

---

## Manuscripts

Primary manuscript:
- manuscript/ISR_as_a_Normalization_Resistant_Polynomial_Regime.md

Supplementary note:
- manuscript/ISR_Normalization_Resistance.md

---

## Model Overview

**ISR = Implicit Superposition Register**

- Symbolic representation of exponential assignment space
- Deterministic constraint conjunction
- No enumeration of assignments
- Polynomial-time operations over implicit state

This repository concerns structural properties only.

---

## Artifacts

- docs/MODEL.md
- docs/INVARIANTS.md
- model/isr.py
- scripts/run_isr_demo.py
- scripts/normalization_attempt.py
- scripts/oracle_audit.py
- tests/

---

## Scope

This repository:
- Documents a computational regime
- Demonstrates normalization resistance structurally

This repository does **not**:
- Claim algorithmic speedups
- Resolve P vs NP
- Assert empirical performance dominance

---

## Certification Boundary

This repository is **NON-CERTIFIED under URF**.

Only **NEGATIVE certification artifacts** may be present.
No positive NCR claim is asserted.
All results are research or infrastructure-only.

Certification artifacts are declarative, cryptographically signed, and inert with respect to CI and runtime behavior.
