from __future__ import annotations

import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "assignments/hw04/resources/data/leukemia/leukemia.csv"
OUT = ROOT / ".tmp/dimension-reduction/student-results"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(DATA)
    X = df.drop(columns=["sample_id", "original_split", "diagnosis"])
    y = df["diagnosis"].to_numpy()
    Z = StandardScaler().fit_transform(X)
    pca = PCA(svd_solver="full").fit(Z)
    scores = pca.transform(Z)
    raw_pca = PCA(svd_solver="full").fit(X)
    loadings = pd.Series(pca.components_[0], index=X.columns)
    raw_loadings = pd.Series(raw_pca.components_[0], index=X.columns)
    top5 = loadings.loc[loadings.abs().nlargest(5).index]
    raw_top5 = raw_loadings.loc[raw_loadings.abs().nlargest(5).index]
    evr = pca.explained_variance_ratio_

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(np.arange(1, len(evr) + 1), np.cumsum(evr), lw=1.2)
    ax.set(xlabel="Number of components", ylabel="Cumulative explained variance",
           title="PCA cumulative explained variance", ylim=(0, 1.02))
    ax.axhline(.8, color="gray", ls="--", lw=1)
    fig.tight_layout()
    fig.savefig(OUT / "pca-cumulative-variance.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    for label, color in [("ALL", "#387ca3"), ("AML", "#d57839")]:
        mask = y == label
        ax.scatter(scores[mask, 0], scores[mask, 1], c=color, s=42, label=label,
                   edgecolors="white", linewidths=.35)
    ax.set(xlabel=f"PC1 ({evr[0]:.1%})", ylabel=f"PC2 ({evr[1]:.1%})",
           title="Standardized PCA: all samples")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "pca-standardized.png", dpi=180)
    plt.close(fig)

    train = df["original_split"].eq("train").to_numpy()
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    methods = {
        "StandardScaler + 1-NN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1)),
        "StandardScaler + PCA(10) + 1-NN": make_pipeline(
            StandardScaler(), PCA(n_components=10, svd_solver="full"), KNeighborsClassifier(n_neighbors=1)
        ),
    }
    cv_results = {}
    for name, model in methods.items():
        values = cross_val_score(model, X.to_numpy()[train], y[train], cv=cv,
                                 scoring="balanced_accuracy")
        cv_results[name] = {"fold_scores": values.tolist(), "mean": float(values.mean())}

    result = {
        "shape": list(X.shape),
        "class_counts": df["diagnosis"].value_counts().to_dict(),
        "train_class_counts": df.loc[train, "diagnosis"].value_counts().to_dict(),
        "test_class_counts": df.loc[~train, "diagnosis"].value_counts().to_dict(),
        "zscore_max_abs_mean": float(np.abs(Z.mean(0)).max()),
        "zscore_max_abs_std_error": float(np.abs(Z.std(0, ddof=0) - 1).max()),
        "standardized_pca": {
            "evr": evr.tolist(), "pc1_pc2": float(evr[:2].sum()),
            "components_80_percent": int(np.searchsorted(np.cumsum(evr), .8) + 1),
            "top5_pc1_loadings": top5.to_dict(),
        },
        "raw_scale_pca": {
            "evr": raw_pca.explained_variance_ratio_.tolist(),
            "pc1_pc2": float(raw_pca.explained_variance_ratio_[:2].sum()),
            "top5_pc1_loadings": raw_top5.to_dict(),
        },
        "training_only_cv": cv_results,
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "sklearn": __import__("sklearn").__version__,
                     "matplotlib": matplotlib.__version__},
    }
    (OUT / "pca-cv-results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    pd.DataFrame({"sample_id": df.sample_id, "diagnosis": y,
                  "PC1": scores[:, 0], "PC2": scores[:, 1]}).to_csv(
                      OUT / "pca-sample-coordinates.csv", index=False)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
