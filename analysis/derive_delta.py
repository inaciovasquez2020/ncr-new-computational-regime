import pandas as pd

def derive(df):
    r = df["R"].astype(float)
    df = df.copy()
    df["delta_odd"] = (1.0 - r) / (1.0 + r)
    df["delta_stat_err"] = (2.0 / (1.0 + r) ** 2) * df["stat_err"].astype(float)
    df["delta_syst_err"] = (2.0 / (1.0 + r) ** 2) * df["syst_err"].astype(float)
    df["delta_err"] = (df["delta_stat_err"]**2 + df["delta_syst_err"]**2) ** 0.5
    return df

frames = []
for path in ["data/raw/vepp3.csv","data/raw/clas.csv","data/raw/olympus.csv"]:
    df = pd.read_csv(path)
    frames.append(derive(df))

out = pd.concat(frames, ignore_index=True)
out.to_csv("data/derived/all_delta_odd.csv", index=False)
print("wrote data/derived/all_delta_odd.csv")
