import numpy as np
import pandas as pd

df = pd.read_csv("data/derived/all_delta_odd.csv")

def rank1_als(sub, iters=200, tol=1e-12):
    eps_vals = sorted(sub["epsilon"].unique())
    q2_vals  = sorted(sub["Q2"].unique())
    ei = {e:i for i,e in enumerate(eps_vals)}
    qj = {q:j for j,q in enumerate(q2_vals)}

    I = len(eps_vals)
    J = len(q2_vals)

    M = np.full((I,J), np.nan)
    S = np.full((I,J), np.nan)

    for _, r in sub.iterrows():
        i = ei[float(r["epsilon"])]
        j = qj[float(r["Q2"])]
        M[i,j] = float(r["delta_odd"])
        S[i,j] = float(r["delta_err"])

    mask = np.isfinite(M) & np.isfinite(S) & (S > 0)
    if mask.sum() < 4:
        raise SystemExit("insufficient overlapping data for rank-1 test")

    W = np.zeros_like(M)
    W[mask] = 1.0 / (S[mask] ** 2)

    b = np.ones(J)
    a = np.ones(I)

    last = None
    for _ in range(iters):
        for i in range(I):
            m = mask[i,:]
            if not np.any(m):
                continue
            num = np.sum(W[i,m] * M[i,m] * b[m])
            den = np.sum(W[i,m] * (b[m] ** 2))
            if den > 0:
                a[i] = num / den

        for j in range(J):
            m = mask[:,j]
            if not np.any(m):
                continue
            num = np.sum(W[m,j] * M[m,j] * a[m])
            den = np.sum(W[m,j] * (a[m] ** 2))
            if den > 0:
                b[j] = num / den

        pred = np.outer(a,b)
        resid = (M - pred)
        chi2 = np.sum(W[mask] * (resid[mask] ** 2))
        if last is not None and abs(last - chi2) <= tol * max(1.0, chi2):
            break
        last = chi2

    y = M[mask]
    yhat = pred[mask]
    rel_l2 = float(np.linalg.norm(y - yhat) / np.linalg.norm(y))
    rel_w = float(np.sqrt(chi2 / max(1.0, mask.sum())))

    return {
        "I": I, "J": J, "n": int(mask.sum()),
        "rel_l2": rel_l2,
        "rms_w": rel_w,
        "a": a, "b": b,
        "eps_vals": eps_vals, "q2_vals": q2_vals
    }

for exp in sorted(df["exp_id"].unique()):
    sub = df[df["exp_id"] == exp].copy()
    if len(sub) < 4:
        continue
    out = rank1_als(sub)
    print("exp_id =", exp)
    print("grid =", out["I"], "x", out["J"], "observed =", out["n"])
    print("rel_l2_residual =", out["rel_l2"])
    print("weighted_rms_residual =", out["rms_w"])
