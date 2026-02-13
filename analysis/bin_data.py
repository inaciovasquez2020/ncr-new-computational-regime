import pandas as pd
import yaml
import numpy as np

with open("analysis/binning.yaml") as f:
    cfg = yaml.safe_load(f)

eps_bins = cfg["epsilon_bins"]
q2_bins  = cfg["Q2_bins"]

df = pd.read_csv("data/derived/all_delta_odd.csv")

def assign_bin(x, bins):
    for i in range(len(bins)-1):
        if bins[i] <= x < bins[i+1]:
            return 0.5*(bins[i]+bins[i+1])
    return None

df["eps_bin"] = df["epsilon"].apply(lambda x: assign_bin(x, eps_bins))
df["q2_bin"]  = df["Q2"].apply(lambda x: assign_bin(x, q2_bins))

df = df.dropna(subset=["eps_bin","q2_bin"])

out = (
    df.groupby(["eps_bin","q2_bin"])
      .apply(lambda g: pd.Series({
          "delta_odd": np.average(g["delta_odd"], weights=1/g["delta_err"]**2),
          "delta_err": np.sqrt(1.0 / np.sum(1/g["delta_err"]**2)),
          "n": len(g)
      }))
      .reset_index()
)

out.to_csv("data/derived/binned_delta_odd.csv", index=False)
print("wrote data/derived/binned_delta_odd.csv")
