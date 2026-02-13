import pandas as pd
import glob
import os

def derive(df):
    r = df["R"].astype(float)
    df = df.copy()
    df["delta_odd"] = (1.0 - r) / (1.0 + r)
    df["delta_stat_err"] = (2.0 / (1.0 + r) ** 2) * df["stat_err"].astype(float)
    df["delta_syst_err"] = (2.0 / (1.0 + r) ** 2) * df["syst_err"].astype(float)
    df["delta_err"] = (df["delta_stat_err"]**2 + df["delta_syst_err"]**2) ** 0.5
    return df

frames = []

for path in sorted(glob.glob("data/raw/*.csv")):
    if os.path.basename(path).startswith("TEMPLATE"):
        continue
    df = pd.read_csv(path)
    required = ["epsilon","Q2","R","stat_err","syst_err","exp_id","norm_group"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"{path}: missing columns {missing}")
    if len(df) == 0:
        continue
    frames.append(derive(df))

if not frames:
    raise SystemExit("no usable raw data files found")

out = pd.concat(frames, ignore_index=True)
out.to_csv("data/derived/all_delta_odd.csv", index=False)
print("wrote data/derived/all_delta_odd.csv")
