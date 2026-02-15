Invariant candidates

P0 (exact): Implicit Dimension
P0(S) := log2(|S|) where S ⊆ {0,1}^n is the current ISR state.

Proxy P (implementable): ROBDD complexity + exact count
P(S) := (log2(|S|), nodes(S))

URF-preserved barrier property (checker form)
Given step budget K >= 0, define:
BarrierK(trace) holds iff for all steps t:
  P0_t - P0_{t+1} <= K

This is a monotone-per-step entropy-loss bound; it is a certificate predicate on traces.

Normalization-attempt harness
Given a transcript budget B bits/step, attempt to map ISR states to B-bit tokens while preserving update consistency.
Failure witness: two distinct ISR states collide in token but yield divergent next-step tokens under same update.
