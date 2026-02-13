import json
import numpy as np
import pandas as pd

DF_PATH = "data/derived/binned_delta_odd.csv"
RIDGE = 1e-12

def build_matrix(df):
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
    return eps_vals, q2_vals, M, S, mask

def als_rank1(M, S, mask, iters=800):
    I, J = M.shape
    W = np.zeros_like(M)
    W[mask] = 1.0 / (S[mask] ** 2)

    a = np.ones(I)
    b = np.ones(J)

    for _ in range(iters):
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
    chi2 = float(np.sum(W[mask] * resid[mask]**2))
    return pred, resid, chi2

def als_rank2(M, S, mask, iters=1200):
    I, J = M.shape
    W = np.zeros_like(M)
    W[mask] = 1.0 / (S[mask] ** 2)

    A = np.random.default_rng(0).normal(size=(I,2))
    B = np.random.default_rng(1).normal(size=(J,2))

    for _ in range(iters):
        for i in range(I):
            m = mask[i,:]
            if not np.any(m):
                continue
            X = B[m,:]
            w = W[i,m]
            y = M[i,m]
            G = (X.T * w) @ X
            rhs = (X.T * w) @ y
            if np.linalg.matrix_rank(G) < 2:
                continue
            A[i,:] = np.linalg.solve(G + RIDGE*np.eye(2), rhs)

        for j in range(J):
            m = mask[:,j]
            if not np.any(m):
                continue
            X = A[m,:]
            w = W[m,j]
            y = M[m,j]
            G = (X.T * w) @ X
            rhs = (X.T * w) @ y
            if np.linalg.matrix_rank(G) < 2:
                continue
            B[j,:] = np.linalg.solve(G + RIDGE*np.eye(2), rhs)

    pred = A @ B.T
    resid = M - pred
    chi2 = float(np.sum(W[mask] * resid[mask]**2))
    return pred, resid, chi2

def main():
    df = pd.read_csv(DF_PATH)
    eps_vals, q2_vals, M, S, mask = build_matrix(df)
    nobs = int(mask.sum())

    pred1, resid1, chi2_1 = als_rank1(M,S,mask)
    pred2, resid2, chi2_2 = als_rank2(M,S,mask)

    p1 = len(eps_vals) + len(q2_vals) - 1
    p2 = 2*(len(eps_vals) + len(q2_vals)) - 4
    dof1 = nobs - p1
    dof2 = nobs - p2

    out = {
        "observed": nobs,
        "k1": {"chi2": chi2_1, "dof": dof1},
        "k2": {"chi2": chi2_2, "dof": dof2},
        "delta": {"delta_chi2": chi2_1 - chi2_2, "delta_dof": dof1 - dof2}
    }

    with open("analysis/results_rankk.json","w") as f:
        json.dump(out, f, indent=2)

    print("k=1 chi2", chi2_1, "dof", dof1)
    print("k=2 chi2", chi2_2, "dof", dof2)
    print("delta chi2", chi2_1 - chi2_2)

if __name__ == "__main__":
    main()
