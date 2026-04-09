# Witness Tightening Conditional Scope (2026-04)

## Status
Conditional.

## Repository-compatible scope
This note preserves the repository boundary:
1. structural regime documentation only;
2. no positive URF certification claim;
3. no claim of algorithmic speedup or complexity-class resolution.

## Missing executable strengthening
The weakest next artifact is a tightened witness extractor emitting:
1. a minimal divergence index \(t_\ast\);
2. a transcript-collision record at budget \(B\);
3. a deterministic replay certificate linking the collision to next-step divergence.

## Conditional schema
Assume a normalization map
\[
N_B : \mathcal S \to \{0,1\}^{\le B}
\]
for each step budget \(B\), and update operator
\[
U : \mathcal S \times \mathcal I \to \mathcal S.
\]

A normalization-failure witness is a tuple
\[
W=(s,s',i,t_\ast)
\]
such that
\[
s\neq s',\qquad N_B(s)=N_B(s'),
\]
but
\[
N_B(U(s,i)) \neq N_B(U(s',i)).
\]

## Conditional consequence
If such a deterministic witness \(W\) is emitted and replay-verifiable, then bounded-per-step transcript injectivization fails for the witnessed budget class.

## Label
This note is CONDITIONAL.
It does not assert any positive NCR certification claim.
