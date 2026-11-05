from __future__ import annotations

from pathlib import Path
import os
import tempfile

# Keep runtime cache in the course-designated, writable results directory.
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".tmp/dimension-reduction/student-results"
OUT.mkdir(parents=True, exist_ok=True)
os.environ["NUMBA_CACHE_DIR"] = str(OUT / "numba-cache")
tempfile.tempdir = str(OUT)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.manifold import trustworthiness
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from umap import UMAP


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "assignments/hw04/resources/data/leukemia/leukemia.csv"
OUT = ROOT / ".tmp/dimension-reduction/student-results"
OUT.mkdir(parents=True, exist_ok=True)


def neighbor_sets(coords, k=10):
    indices = NearestNeighbors(n_neighbors=k + 1).fit(coords).kneighbors(coords, return_distance=False)
    return [set(row[1:]) for row in indices]


def main():
    df = pd.read_csv(DATA)
    X = df.drop(columns=["sample_id", "original_split", "diagnosis"])
    labels = df["diagnosis"].to_numpy()
    Z = StandardScaler().fit_transform(X)
    settings = {
        "baseline": dict(n_neighbors=15, min_dist=.1, random_state=42),
        "neighbors5": dict(n_neighbors=5, min_dist=.1, random_state=42),
        "min_dist05": dict(n_neighbors=15, min_dist=.5, random_state=42),
        "seed7": dict(n_neighbors=15, min_dist=.1, random_state=7),
    }
    embeddings = {}
    for name, params in settings.items():
        print(f"Fitting {name}: {params}", flush=True)
        model = UMAP(n_components=2, metric="euclidean", n_jobs=1, **params)
        embeddings[name] = model.fit_transform(Z)
        print(f"Completed {name}", flush=True)

    rows = []
    for name, coords in embeddings.items():
        for i, sample_id in enumerate(df["sample_id"]):
            rows.append({"setting": name, "sample_id": sample_id, "diagnosis": labels[i],
                         "UMAP1": coords[i, 0], "UMAP2": coords[i, 1]})
    pd.DataFrame(rows).to_csv(OUT / "umap-sample-coordinates.csv", index=False)

    base = embeddings["baseline"]
    base_sets = neighbor_sets(base)
    stability = []
    for name, coords in embeddings.items():
        current = neighbor_sets(coords)
        overlap = np.mean([len(a & b) / 10 for a, b in zip(base_sets, current)])
        stability.append({
            "setting": name,
            "mean_10_neighbor_overlap_vs_baseline": float(overlap),
            "spearman_pairwise_distance_vs_baseline": float(spearmanr(pdist(base), pdist(coords)).statistic),
            "trustworthiness_k10": float(trustworthiness(Z, coords, n_neighbors=10)),
        })
    pd.DataFrame(stability).to_csv(OUT / "umap-stability.csv", index=False)

    pca_scores = PCA(svd_solver="full").fit_transform(Z)
    pca_model = PCA(svd_solver="full").fit(Z)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    for ax, coords, title in [(axes[0], pca_scores, "PCA"),
                              (axes[1], embeddings["baseline"], "UMAP baseline")]:
        for label, color in [("ALL", "#387ca3"), ("AML", "#d57839")]:
            mask = labels == label
            ax.scatter(coords[mask, 0], coords[mask, 1], c=color, s=36,
                       label=label, edgecolors="white", linewidths=.3)
        ax.set(title=title, xlabel=(f"PC1 ({pca_model.explained_variance_ratio_[0]:.1%})" if title == "PCA" else "UMAP1"),
               ylabel=(f"PC2 ({pca_model.explained_variance_ratio_[1]:.1%})" if title == "PCA" else "UMAP2"))
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "pca-umap-baseline.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (name, coords) in zip(axes.flat, embeddings.items()):
        for label, color in [("ALL", "#387ca3"), ("AML", "#d57839")]:
            mask = labels == label
            ax.scatter(coords[mask, 0], coords[mask, 1], c=color, s=30,
                       label=label, edgecolors="white", linewidths=.3)
        params = settings[name]
        ax.set(title=f"{name}: n_neighbors={params['n_neighbors']}, min_dist={params['min_dist']}, seed={params['random_state']}",
               xlabel="UMAP1", ylabel="UMAP2")
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "umap-parameter-checks.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
