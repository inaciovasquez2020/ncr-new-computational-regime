import json

with open("analysis/results_rankk.json") as f:
    r = json.load(f)

k1 = r["k1"]
k2 = r["k2"]
d  = r["delta"]

txt = []
txt.append(r"\section{Results}")
txt.append("")
txt.append(rf"We project the combined CLAS, VEPP-3, and OLYMPUS beam-charge data onto a common $(\varepsilon,Q^2)$ binning and fit the binned observable $\delta_{{\mathrm{{odd}}}}=(1-R)/(1+R)$ with low-rank models.")
txt.append("")
txt.append(rf"For the rank-$1$ hypothesis $\delta_{{\mathrm{{odd}}}}(\varepsilon,Q^2)\approx a(Q^2)b(\varepsilon)$, the weighted least-squares fit yields $\chi^2={k1['chi2']:.3g}$ for ${k1['dof']}$ degrees of freedom (reduced $\chi^2={k1['chi2_per_dof']:.3g}$), with relative $\ell_2$ residual {k1['relative_L2_residual']:.3g}.")
txt.append("")
txt.append(rf"Allowing rank-$2$ structure reduces the fit statistic to $\chi^2={k2['chi2']:.3g}$ for ${k2['dof']}$ degrees of freedom (reduced $\chi^2={k2['chi2_per_dof']:.3g}$), corresponding to $\Delta\chi^2={d['delta_chi2']:.3g}$ for $\Delta\nu={d['delta_dof']}$.")
txt.append("")
txt.append(r"Figure~\ref{fig:rankfits} shows the observed binned $\delta_{\mathrm{odd}}$ and the rank-$1$ and rank-$2$ reconstructions and residuals. Table~\ref{tab:rankk} summarizes the model comparison.")
txt.append("")

open("analysis/results_section.tex","w").write("\n".join(txt) + "\n")
print("wrote analysis/results_section.tex")
