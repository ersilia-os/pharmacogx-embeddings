import os
import pandas as pd
from tqdm import tqdm
import collections
import numpy as np

root = os.path.dirname(os.path.abspath(__file__))

# create folder if it does not exist
folder_path = os.path.join(root, "..", "..", "data", "ml_datasets_matrix")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

folder_path_pairs = os.path.join(root, "..", "..", "data", "ml_datasets_pairs")
for l in tqdm(os.listdir(folder_path_pairs)):
    if l.startswith("df_"):
        df_ = pd.read_csv(os.path.join(folder_path_pairs, l))
        df_ = df_[list(df_.columns)[:6]]
        columns = list(df_.columns)
        d = collections.defaultdict(int)
        for r in df_.values:
            k = tuple(r)
            d[k] += 1
        R = []
        for k, v in d.items():
            R.append(list(k) + [v])
        df_ = pd.DataFrame(R, columns=columns + ["variants_count"])
        rows = sorted(set(df_["inchikey"]))
        cols = sorted(set(df_["uniprot_ac"]))
        values = {}
        for r in df_[["inchikey", "uniprot_ac", "variants_count"]].values:
            values[(r[0], r[1])] = r[2]
        M = np.zeros((len(rows), len(cols)), dtype=int)
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                if (r, c) in values:
                    M[i, j] = values[(r, c)]
        df = pd.DataFrame(M, index=rows, columns=cols)
        df.to_csv(os.path.join(folder_path, l), index=True)
