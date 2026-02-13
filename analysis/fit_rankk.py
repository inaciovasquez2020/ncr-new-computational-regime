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

def residual_metrics(M, S, pred, mask):
    resid = M - pred
    W = np.zeros_like(M)
    W[mask] = 1.0 / (S[mask] ** 2)
    chi2 = float(np.sum(W[mask] * resid[mask]**2))
    rel_L2 = float(np.linalg.norm(resid[mask]) / np.linalg.norm(M[mask]))
    rms_w = float(np.sqrt(np.mean((resid[mask] / S[mask])**2)))
    return resid, chi2, rel_L2, rms_w

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
    return pred

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

    return A @ B.T

def main():
    df = pd.read_csv(DF_PATH)
    eps_vals, q2_vals, M, S, mask = build_matrix(df)
    nobs = int(mask.sum())
    if nobs < 4:
        raise SystemExit("insufficient data")

    pred1 = als_rank1(M,S,mask)
    resid1, chi2_1, rel1, rms1 = residual_metrics(M,S,pred1,mask)

    pred2 = als_rank2(M,S,mask)
    resid2, chi2_2, rel2, rms2 = residual_metrics(M,S,pred2,mask)

    p1 = len(eps_vals) + len(q2_vals) - 1
    p2 = 2*(len(eps_vals) + len(q2_vals)) - 4
    dof1 = nobs - p1
    dof2 = nobs - p2

    out = {
        "grid_I": len(eps_vals),
        "grid_J": len(q2_vals),
        "observed": nobs,
        "k1": {
            "chi2": chi2_1,
            "dof": dof1,
            "chi2_per_dof": chi2_1/dof1 if dof1>0 else None,
            "relative_L2_residual": rel1,
            "weighted_RMS_residual": rms1
        },
        "k2": {
            "chi2": chi2_2,
            "dof": dof2,
            "chi2_per_dof": chi2_2/dof2 if dof2>0 else None,
            "relative_L2_residual": rel2,
            "weighted_RMS_residual": rms2
        },
        "delta": {
            "delta_chi2": chi2_1 - chi2_2,
            "delta_dof": dof1 - dof2
        }
    }

    with open("analysis/results_rankk.json","w") as f:
        json.dump(out, f, indent=2)

    np.savez("analysis/pred_resid_rankk.npz",
             eps_vals=np.array(eps_vals),
             q2_vals=np.array(q2_vals),
             M=M, S=S, mask=mask,
             pred1=pred1, resid1=resid1,
             pred2=pred2, resid2=resid2)

    print("wrote analysis/results_rankk.json")
    print("wrote analysis/pred_resid_rankk.npz")

if __name__ == "__main__":
    main()
