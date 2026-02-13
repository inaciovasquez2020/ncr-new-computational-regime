Rank-1 falsification tests

The SVD and invariant tests require at least a 2x2 overlapping grid
in (epsilon, Q2), corresponding to >= 4 distinct points and >= 6
non-NaN matrix entries.

If the tests exit with:
  "insufficient overlapping data for rank-1 test"

this indicates that only placeholder or non-overlapping data are present.
