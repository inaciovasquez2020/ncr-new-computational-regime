Title: ISR as a Normalization-Resistant Polynomial Regime

Abstract.
We exhibit a toy computational regime (ISR) that evolves under local, polynomial-time updates yet resists normalization into URF-admissible transcripts under bounded per-step information. The obstruction is structural, not empirical, and is witnessed by a failed normalization attempt recorded as a signed certificate.

1. Model.
ISR is a compressed decision-diagram update system maintaining a hidden state S_t with monotone lower-bound proxy P(S_t). Updates are local and deterministic.

2. Barrier Property.
Define P as a proxy for implicit dimension. Under URF-admissible refinement, P is monotone and admits an O(1) upper bound on entropy loss per step.

3. Separation.
Empirically, ISR traces exhibit P(S_t)=Ω(n^α) growth on a parameterized family, while any URF normalization attempt respecting transcript budgets fails to preserve trace invariants.

4. Certificate.
Normalization failure is recorded as an executable, signed certificate produced by scripts/normalization_attempt.py.

5. Conclusion.
ISR constitutes a polynomial-time regime that is verification-friendly but normalization-resistant, separating execution from compressible explanation.

