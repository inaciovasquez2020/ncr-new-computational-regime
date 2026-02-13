import numpy as np
import pandas as pd
from numpy.linalg import svd

df = pd.read_csv("data/derived/all_delta_odd.csv")

eps_vals = sorted(df["epsilon"].unique())
q2_vals = sorted(df["Q2"].unique())

e_index = {e:i for i,e in enumerate(eps_vals)}
q_index = {q:j for j,q in enumerate(q2_vals)}

M = np.full((len(eps_vals), len(q2_vals)), np.nan)
S = np.full((len(eps_vals), len(q2_vals)), np.nan)

for _, r in df.iterrows():
    i = e_index[r["epsilon"]]
    j = q_index[r["Q2"]]
    M[i,j] = r["delta_odd"]
    S[i,j] = r["delta_err"]

mask = np.isfinite(M) & np.isfinite(S) & (S > 0)

if mask.sum() < 6:
    raise SystemExit("insufficient overlapping data for rank-1 test")

W = np.zeros_like(M)
W[mask] = 1.0 / S[mask]

A = np.zeros_like(M)
A[mask] = W[mask] * M[mask]

U, sing, Vt = svd(A, full_matrices=False)

sigma1 = sing[0]
sigma2 = sing[1] if len(sing) > 1 else 0.0
rho = sigma2 / sigma1 if sigma1 > 0 else float("nan")

print("singular_values =", sing)
print("sigma2_over_sigma1 =", rho)
