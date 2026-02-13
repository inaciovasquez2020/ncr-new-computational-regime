import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open("analysis/results_rankk.json") as f:
    res = json.load(f)

Z = np.load("analysis/pred_resid_rankk.npz", allow_pickle=True)
eps_vals = Z["eps_vals"].astype(float)
q2_vals  = Z["q2_vals"].astype(float)
M = Z["M"].astype(float)
S = Z["S"].astype(float)
mask = Z["mask"].astype(bool)
pred1 = Z["pred1"].astype(float)
resid1 = Z["resid1"].astype(float)
pred2 = Z["pred2"].astype(float)
resid2 = Z["resid2"].astype(float)

def save_heat(path, A, title):
    X, Y = np.meshgrid(q2_vals, eps_vals)
    plt.figure()
    C = np.where(mask, A, np.nan)
    plt.pcolormesh(X, Y, C, shading="auto")
    plt.xlabel("Q2 bin")
    plt.ylabel("epsilon bin")
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

save_heat("analysis/fig_deltaodd_observed.png", M, "Binned delta_odd (observed)")
save_heat("analysis/fig_rank1_pred.png", pred1, "Rank-1 fit prediction")
save_heat("analysis/fig_rank1_resid.png", resid1, "Rank-1 residual (observed - pred)")
save_heat("analysis/fig_rank2_pred.png", pred2, "Rank-2 fit prediction")
save_heat("analysis/fig_rank2_resid.png", resid2, "Rank-2 residual (observed - pred)")

table = pd.DataFrame([
    {"model":"k=1", "chi2":res["k1"]["chi2"], "dof":res["k1"]["dof"], "chi2_per_dof":res["k1"]["chi2_per_dof"],
     "relative_L2_residual":res["k1"]["relative_L2_residual"], "weighted_RMS_residual":res["k1"]["weighted_RMS_residual"]},
    {"model":"k=2", "chi2":res["k2"]["chi2"], "dof":res["k2"]["dof"], "chi2_per_dof":res["k2"]["chi2_per_dof"],
     "relative_L2_residual":res["k2"]["relative_L2_residual"], "weighted_RMS_residual":res["k2"]["weighted_RMS_residual"]},
    {"model":"delta", "chi2":res["delta"]["delta_chi2"], "dof":res["delta"]["delta_dof"], "chi2_per_dof":None,
     "relative_L2_residual":None, "weighted_RMS_residual":None},
])
table.to_csv("analysis/table_rankk_summary.csv", index=False)

print("wrote analysis/table_rankk_summary.csv")
print("wrote analysis/fig_*.png")
