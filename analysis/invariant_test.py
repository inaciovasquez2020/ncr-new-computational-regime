import pandas as pd
import itertools

df = pd.read_csv("data/derived/all_delta_odd.csv")

def inv_report(sub):
    eps = sorted(sub["epsilon"].unique())
    q2s = sorted(sub["Q2"].unique())

    def delta(e,q):
        rows = sub[(sub["epsilon"]==e) & (sub["Q2"]==q)]
        if len(rows) != 1:
            return None
        return float(rows.iloc[0]["delta_odd"])

    printed = 0
    for e1,e2 in itertools.combinations(eps,2):
        for q1,q2 in itertools.combinations(q2s,2):
            d11 = delta(e1,q1)
            d12 = delta(e1,q2)
            d21 = delta(e2,q1)
            d22 = delta(e2,q2)
            if None in (d11,d12,d21,d22):
                continue
            if d12 == 0 or d21 == 0:
                continue
            I = (d11*d22)/(d12*d21)
            print("epsilon",e1,e2,"Q2",q1,q2,"I",I)
            printed += 1
    return printed

for exp in sorted(df["exp_id"].unique()):
    sub = df[df["exp_id"] == exp].copy()
    if len(sub) < 4:
        continue
    print("exp_id =", exp)
    printed = inv_report(sub)
    if printed == 0:
        print("no_2x2_subgrids")
