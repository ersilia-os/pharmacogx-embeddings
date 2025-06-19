import pandas as pd
import os
import re
import numpy as np
from tqdm import tqdm

root = os.path.dirname(os.path.abspath(__file__))

results_dir = os.path.abspath(os.path.join(root, "..", "results", "results_pairs_ev2"))
results_dir_chunks = os.path.join(results_dir, "chunks")


class DynamicCalculator:
    def __init__(self):
        self.k = 0
        self.M_k = 0
        self.S_k = 0

    def add(self, x):
        self.k += 1
        old_M_k = self.M_k
        self.M_k += (x - old_M_k) / self.k
        self.S_k += (x - old_M_k) * (x - self.M_k)

    def mean(self):
        return self.M_k

    def variance(self):
        if self.k <= 1:
            return float("nan")
        return self.S_k / (self.k - 1)

    def std_dev(self):
        return self.variance() ** 0.5


df = pd.read_csv(
    os.path.join(
        results_dir,
        "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates.csv",
    )
)

print(df.columns)
print(df.shape)

y_hat_columns = [x for x in list(df.columns) if x.startswith("y_hat_")]

dynamic_calculators = [DynamicCalculator() for _ in range(len(y_hat_columns))]


def ends_with_number_and_csv(filename):
    pattern = r".*_(\d+)\.csv$"
    return bool(re.match(pattern, filename))

for filename in tqdm(os.listdir(results_dir_chunks)):
    if ends_with_number_and_csv(filename):
        dc = pd.read_csv(os.path.join(results_dir_chunks, filename))
        for i, col in enumerate(y_hat_columns):
            for v in dc[col].tolist():
                dynamic_calculators[i].add(v)

means = [dc.mean() for dc in dynamic_calculators]
stds = [dc.std_dev() for dc in dynamic_calculators]

new_col_names = []
for i, c in enumerate(y_hat_columns):
    new_col_name = c + "_zscore"
    values = np.array(df[c].tolist())
    zscores = (values - means[i]) / stds[i]
    df[new_col_name] = list(zscores)
    new_col_names += [new_col_name]

# Get top 50 genes per chemical

weights = np.array([1, 2, 3])/6
consensus_zscores = []
for r in df[new_col_names].values:
    print(r)
    consensus_zscores += [np.average(r, weights=weights)]

df["consensus_zscore"] = consensus_zscores
df = df.sort_values("consensus_zscore", ascending=False).reset_index(drop=True)
cids = df["cid"].unique().tolist()
df_ = None
for cid in tqdm(cids):
    dh = df[df["cid"] == cid].head(50)
    if df_ is None:
        df_ = dh
    else:
        df_ = pd.concat([df_, dh])

df_.to_csv(
    os.path.join(
        results_dir,
        "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_top50_filter.csv",
    ),
    index=False,
)


# Filter out rows where any of the z-scores is above the threshold

# 95% confidence in z-score
threshold = 1.96
df_ = df[df[new_col_names].gt(threshold).any(axis=1)]
df_ = df_.sort_values(["cid", "consensus_zscore"], ascending=[True, False]).reset_index(drop=True)

df_.to_csv(
    os.path.join(
        results_dir,
        "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_zscore95_filter.csv",
    ),
    index=False,
)
