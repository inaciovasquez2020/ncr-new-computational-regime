[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18651031.svg)](https://doi.org/10.5281/zenodo.18651031)
## Manuscript
- manuscript/ISR_as_a_Normalization_Resistant_Polynomial_Regime.md
## Manuscript
A minimal structural note documenting the normalization-resistant ISR regime is included:
- manuscript/ISR_Normalization_Resistance.md

NCR — New Computational Regime (ISR)

ISR = Implicit Superposition Register
Discrete, deterministic model whose state is a reduced ordered decision diagram representing an exponentially large set of assignments.
Updates apply constraints by symbolic conjunction without enumerating assignments.

<<<<<<< HEAD
Artifacts
docs/MODEL.md
docs/INVARIANTS.md
model/isr.py
scripts/run_isr_demo.py
scripts/normalization_attempt.py
scripts/oracle_audit.py
tests/
=======
## Canonical Registry
This repository is a registered module of the Vasquez Index. Stable references, reproducibility links, and deployment status can be found at:
* [Vasquez Index Dashboard](https://inaciovasquez2020.github.io/vasquez-index/dashboard.html)

## Repository Status
* **Registry Handle:** inaciovasquez2020/radiative-rigidity
* **Stability:** Refer to the Vasquez Index for the latest stable DOI.
* **Infrastructure:** [scientific-infrastructure](https://github.com/inaciovasquez2020/scientific-infrastructure)

---
Physics statement

The core physics claim supported by this repository is stated cleanly and independently of the verification machinery here:

docs/PHYSICS_STATEMENT.md

Readers interested in the physics result should start there. This repository exists to make that claim checkable and reproducible.

## Documentation
- Radiative Rigidity overview: https://inaciovasquez2020.github.io
- Verification status: https://inaciovasquez2020.github.io/vasquez-index/dashboard.html


## Technical Notes
* **Reproducibility:** To ensure consistent results, follow the environment configurations defined in the `scientific-infrastructure` module.
* **Integration:** This repository is intended to work in conjunction with `chronos-urf-rr` and `urf-core`.

## Citation
If you use this research or the associated implementation in your work, please cite it as follows:

```bibtex
@manual{Vasquez_Radiative_Rigidity_2026,
  author = {Vasquez, Inacio F.},
  title  = {Radiative Rigidity: Research Implementation and Analysis},
  year   = {2026},
  url    = {[https://github.com/inaciovasquez2020/radiative-rigidity](https://github.com/inaciovasquez2020/radiative-rigidity)}
}

## Quickstart (60 seconds)

```bash
./scripts/radius check
```

URF Radiative Rigidity Certification (Physics Infrastructure Tier)

This repository includes URF Certification Artifacts.

A certification release is not a software release.
It makes no performance guarantees, no completeness claims,
and no implications beyond explicitly stated theoretical boundaries.

Certification artifacts are declarative, cryptographically signed,
immutable, and inert with respect to CI and runtime behavior.

Claims apply only within the declared perturbative and theoretical regime.
All non-claims and excluded regimes are explicitly listed in the certification files.

## Certification Boundary

This repository is NON-CERTIFIED under URF.
Only NEGATIVE certification artifacts may be present.
No positive NCR claim is asserted.
All results are research or infrastructure-only.
>>>>>>> e791fa3 (cert(ncr): add NEG-only certification skeleton and README boundary)
