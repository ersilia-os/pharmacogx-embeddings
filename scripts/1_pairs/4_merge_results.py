import pandas as pd
import os
import re
import numpy as np
from tqdm import tqdm

root = os.path.dirname(os.path.abspath(__file__))

results_dir = os.path.abspath(os.path.join(root, "..", "..", "results"))


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
    os.path.join(results_dir, "chemical_gene_pairs_prediction_output_focus.csv")
)

y_hat_columns = [x for x in list(df.columns) if x.startswith("y_hat_")]

dynamic_calculators = [DynamicCalculator() for _ in range(len(y_hat_columns))]


def ends_with_number_and_csv(filename):
    pattern = r".*_(\d+)\.csv$"
    return bool(re.match(pattern, filename))


for filename in tqdm(os.listdir(results_dir)):
    if ends_with_number_and_csv(filename):
        dc = pd.read_csv(os.path.join(results_dir, filename))
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

# 95% confidence in z-score
threshold = 1.96
df = df[df[new_col_names].gt(threshold).any(axis=1)]

df.to_csv(
    os.path.join(
        results_dir, "chemical_gene_pairs_prediction_with_zscore_and_filtered.csv"
    ),
    index=False,
)
