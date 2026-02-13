import numpy as np
import pandas as pd

df = pd.read_csv("data/derived/binned_delta_odd.csv")

eps_vals = sorted(df["eps_bin"].unique())
q2_vals  = sorted(df["q2_bin"].unique())

ei = {e:i for i,e in enumerate(eps_vals)}
qj = {q:j for j,q in enumerate(q2_vals)}

I = len(eps_vals)
J = len(q2_vals)

M = np.full((I,J), np.nan)
S = np.full((I,J), np.nan)

for _, r in df.iterrows():
    i = ei[float(r["eps_bin"])]
    j = qj[float(r["q2_bin"])]
    M[i,j] = float(r["delta_odd"])
    S[i,j] = float(r["delta_err"])

mask = np.isfinite(M) & np.isfinite(S) & (S > 0)
nobs = int(mask.sum())

if nobs < 4:
    raise SystemExit("insufficient overlapping data for rank-1 test")

W = np.zeros_like(M)
W[mask] = 1.0 / (S[mask] ** 2)

a = np.ones(I)
b = np.ones(J)

for _ in range(500):
    for i in range(I):
        m = mask[i,:]
        if not np.any(m):
            continue
        a[i] = np.sum(W[i,m] * M[i,m] * b[m]) / np.sum(W[i,m] * (b[m]**2))

    for j in range(J):
        m = mask[:,j]
        if not np.any(m):
            continue
        b[j] = np.sum(W[m,j] * M[m,j] * a[m]) / np.sum(W[m,j] * (a[m]**2))

pred = np.outer(a,b)
resid = M - pred

chi2 = np.sum(W[mask] * resid[mask]**2)
rel_l2 = np.linalg.norm(resid[mask]) / np.linalg.norm(M[mask])
rms_w  = np.sqrt(chi2 / nobs)

print("grid =", I, "x", J, "observed =", nobs)
print("relative_L2_residual =", rel_l2)
print("weighted_RMS_residual =", rms_w)
