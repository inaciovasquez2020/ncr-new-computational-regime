import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("data/delta_ns.csv")
X = df[["Z", "A", "delta_NS"]].values

# Standardize
X = StandardScaler().fit_transform(X)

# PCA
pca = PCA()
pca.fit(X)

print("Explained variance ratio:")
print(pca.explained_variance_ratio_)

# Plot spectrum
plt.figure()
plt.plot(pca.explained_variance_ratio_, marker='o')
plt.title("Radiative Rigidity Test: PCA Spectrum")
plt.xlabel("Component")
plt.ylabel("Explained Variance Ratio")
plt.savefig("figures/pca_spectrum.png")
plt.show()

