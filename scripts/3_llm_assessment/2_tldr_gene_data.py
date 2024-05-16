import os
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root, "..", "..", "data")

sys.path.append(os.path.join(root, "..", "..", "src"))
from tldr import GeneTLDR

print("...Print getting the identifiers of the genes explored in this study...")
df = pd.read_csv(os.path.join(root, "..", "..", "data", "ml_datasets_pairs", "chemical_gene_pairs_prediction_input.csv"))

genes = []
for r in df[["gid", "gene"]].values:
    genes += [(r[0], r[1])]
genes = list(set(genes))

for i, g in enumerate(genes):
    print(i, g[0], g[1])
    file_name = os.path.join(data_dir, "tldr", "genes", "{0}.md".format(g[0]))
    if os.path.exists(file_name):
        continue
    tldr = GeneTLDR()
    text = tldr.get(g[1])
    with open(file_name, "w") as f:
        f.write(text)