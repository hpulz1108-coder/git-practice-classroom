"""High-dimensional data lab. Calculations only; interpretation belongs to learners.

Run: python scripts/experiments.py --output student-results
Use --output teacher-results for instructor reproduction.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import platform

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.feature_selection import SelectKBest, f_classif
from threadpoolctl import threadpool_limits

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
EXPECTED_SHA = '915bce00295ac470f6bd970a4032730a170a080642a5da53ab0bcb0545156f19'
DIST_DIMS = [2, 3, 10, 100, 1000, 7129]


def load_real():
    path = DATA / 'leukemia.csv'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED_SHA
    df = pd.read_csv(path)
    names = df.columns.drop(['sample_id', 'original_split', 'diagnosis'])
    X = df[names].to_numpy(dtype=float)
    assert X.shape == (72, 7129) and np.isfinite(X).all()
    return df, X, names


def distance_stats(X):
    pair = pdist(X, metric='euclidean')
    D = squareform(pair)
    far = D.max(axis=1)
    np.fill_diagonal(D, np.inf)
    near = D.min(axis=1)
    R = np.divide(far-near, near, out=np.full_like(near, np.nan), where=near > 0)
    return dict(mean=pair.mean(), sd=pair.std(ddof=0), cv=pair.std(ddof=0)/pair.mean(),
                near_median=np.median(near), far_median=np.median(far),
                gap_median=np.median(far-near), r_median=np.nanmedian(R),
                zero_nearest=int((near == 0).sum())), pair, near, far, R


def experiment_a(out):
    """Distances among the same 72 measured expression profiles."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    df, X, names = load_real()
    Z = StandardScaler().fit_transform(X)  # descriptive analysis, not model evaluation
    rows, point_rows, orders = [], [], {}
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    for seed in [42, 7, 2026]:
        order = np.random.default_rng(seed).permutation(X.shape[1])
        orders[str(seed)] = names[order]
        for j, p in enumerate(DIST_DIMS):
            stats, pair, near, far, R = distance_stats(Z[:, order[:p]])
            rows.append(dict(seed=seed, p=p, **stats))
            if seed == 42:
                for i in range(len(X)):
                    point_rows.append(dict(sample_id=df.sample_id.iloc[i], p=p, near=near[i], far=far[i], R=R[i]))
                axes.flat[j].hist(pair / pair.mean(), bins=30, color='#326b91')
                axes.flat[j].set(title=f'p={p}', xlabel='Distance / mean distance', ylabel='Pairs', xlim=(0, 9))
    fig.tight_layout(); fig.savefig(out/'A-distance-distributions.png', dpi=160); plt.close(fig)
    fig = plt.figure(figsize=(11, 4.5))
    ax2 = fig.add_subplot(121); ax3 = fig.add_subplot(122, projection='3d')
    order = np.random.default_rng(42).permutation(X.shape[1])[:3]
    for label,color in [('ALL','#326b91'),('AML','#c16b32')]:
        mask = df.diagnosis.eq(label).to_numpy()
        ax2.scatter(Z[mask,order[0]],Z[mask,order[1]],s=20,c=color,label=label)
        ax3.scatter(Z[mask,order[0]],Z[mask,order[1]],Z[mask,order[2]],s=20,c=color)
    ax2.set(xlabel='Probe 1 (z)',ylabel='Probe 2 (z)',title='72 measured samples: two probes')
    ax3.set(xlabel='Probe 1 (z)',ylabel='Probe 2 (z)',zlabel='Probe 3 (z)',title='Same samples: three probes')
    ax2.legend()
    fig.tight_layout(); fig.savefig(out/'A-scatter-2D-3D.png',dpi=160); plt.close(fig)
    pd.DataFrame(orders).to_csv(out/'A-probe-orders.csv',index=False)
    pd.DataFrame(point_rows).to_csv(out/'A-neighbors-seed42.csv',index=False)
    table = pd.DataFrame(rows); table.to_csv(out/'A-real-distances.csv',index=False)
    return table


@threadpool_limits.wrap(limits=1)
def experiment_b(out):
    """Training, test performance and training-only feature selection on measured data."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    df, X, names = load_real()
    train = df.original_split.eq('train').to_numpy()
    y = df.diagnosis.to_numpy()
    order = np.random.default_rng(42).permutation(X.shape[1])
    rows, predictions = [], []
    for p in [2, 10, 100, 1000, 7129]:
        A = X[:, order[:p]]
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
        model.fit(A[train], y[train])
        pred = model.predict(A[~train])
        rows.append(dict(p=p, train_ba=balanced_accuracy_score(y[train], model.predict(A[train])),
                         test_ba=balanced_accuracy_score(y[~train], pred),
                         ALL_correct=int(((pred == 'ALL') & (y[~train] == 'ALL')).sum()),
                         AML_correct=int(((pred == 'AML') & (y[~train] == 'AML')).sum())))
        for sid,true,guess in zip(df.sample_id[~train],y[~train],pred):
            predictions.append(dict(sample_id=sid,p=p,true=true,prediction=guess))
    scores = pd.DataFrame(rows); scores.to_csv(out/'B-original-split.csv', index=False)
    pd.DataFrame(predictions).to_csv(out/'B-test-predictions.csv', index=False)
    # Repeat validation only inside original training records. No test-based tuning.
    folds = list(RepeatedStratifiedKFold(n_splits=3,n_repeats=3,random_state=42).split(X[train],y[train]))
    cvrows, selected, foldmap = [], [], []
    for split,(itr,iva) in enumerate(folds):
        repeat,fold = split//3+1,split%3+1
        Xt,yt = X[train],y[train]
        for index in iva:
            foldmap.append(dict(repeat=repeat,fold=fold,sample_id=df.sample_id[train].iloc[index],role='validation'))
        for use_select in [False, True]:
            steps = [StandardScaler()]
            if use_select: steps.append(SelectKBest(f_classif,k=20))
            steps.append(KNeighborsClassifier(n_neighbors=1))
            model = make_pipeline(*steps); model.fit(Xt[itr],yt[itr])
            cvrows.append(dict(repeat=repeat,fold=fold,method='select20' if use_select else 'all7129',
                               train_n=len(itr),validation_n=len(iva),
                               train_ba=balanced_accuracy_score(yt[itr],model.predict(Xt[itr])),
                               validation_ba=balanced_accuracy_score(yt[iva],model.predict(Xt[iva]))))
            if use_select:
                selected.append(set(names[model.named_steps['selectkbest'].get_support()]))
    cvtable = pd.DataFrame(cvrows); cvtable.to_csv(out/'B-training-only-cv.csv',index=False)
    pd.DataFrame(foldmap).to_csv(out/'B-validation-folds.csv',index=False)
    pd.DataFrame([dict(split=i+1,probe=p) for i,s in enumerate(selected) for p in sorted(s)]).to_csv(out/'B-selected-probes.csv',index=False)
    jaccard = []
    for a in range(9):
        for b in range(a+1,9):
            jaccard.append(dict(split_a=a+1,split_b=b+1,intersection=len(selected[a]&selected[b]),
                                jaccard=len(selected[a]&selected[b])/len(selected[a]|selected[b])))
    pd.DataFrame(jaccard).to_csv(out/'B-selection-stability.csv',index=False)
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(scores.p,scores.train_ba,'o-',label='Training BA')
    ax.plot(scores.p,scores.test_ba,'o-',label='Test BA')
    ax.axhline(.5,ls='--',color='gray',label='Always ALL baseline')
    ax.set(xscale='log',xlabel='Measured probes p',ylabel='Balanced accuracy',ylim=(0,1.05))
    ax.legend(); fig.tight_layout(); fig.savefig(out/'B-generalization.png',dpi=160); plt.close(fig)
    return scores,cvtable


def run_all(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for name, fn in [('A',experiment_a),('B',experiment_b)]:
        print(f'Running {name}',flush=True); fn(out)
    df,X,names = load_real()
    audit = dict(date='2026-10-13',python=platform.python_version(),
                 packages={k:importlib.metadata.version(k) for k in ['numpy','pandas','scipy','scikit-learn','matplotlib','threadpoolctl']},
                 real_csv_sha256=EXPECTED_SHA, n=len(X),p=len(names),
                 class_counts=df.diagnosis.value_counts().to_dict(),
                 nonfinite=int((~np.isfinite(X)).sum()),constant_features=int((X.std(0)==0).sum()),
                 negatives=int((X<0).sum()),zeros=int((X==0).sum()),
                 duplicate_feature_rows=int(pd.DataFrame(X).duplicated().sum()))
    (out/'run-manifest.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('Finished',flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',default='student-results')
    args = parser.parse_args()
    target = Path(args.output)
    run_all(target if target.is_absolute() else BASE/target)
