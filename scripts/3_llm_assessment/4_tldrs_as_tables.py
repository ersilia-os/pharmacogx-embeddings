import os
import pandas as pd
from tqdm import tqdm

root = os.path.dirname(os.path.abspath(__file__))

results_dir = os.path.join(root, "..", "..", "results", "results_pairs")
genes_tldrs_dir = os.path.join(root, "..", "..", "data", "tldr_explanations", "genes")
drugs_tldrs_dir = os.path.join(root, "..", "..", "data", "tldr_explanations", "drugs")

R = []
for fn in tqdm(os.listdir(drugs_tldrs_dir)):
    if fn.endswith(".md"):
        cid = fn.replace(".md", "")
        with open(os.path.join(drugs_tldrs_dir, fn), "r") as f:
            text = f.read()
        R += [(cid, text.lstrip().rstrip())]
df = pd.DataFrame(R, columns=["cid", "tldr"])
df.to_csv(os.path.join(results_dir, "cid_tldrs.csv"), index=False)

R = []
for fn in tqdm(os.listdir(genes_tldrs_dir)):
    if fn.endswith(".md"):
        gid = fn.replace(".md", "")
        with open(os.path.join(genes_tldrs_dir, fn), "r") as f:
            text = f.read()
        R += [(gid, text.lstrip().rstrip())]
df = pd.DataFrame(R, columns=["gid", "tldr"])
df.to_csv(os.path.join(results_dir, "gid_tldrs.csv"), index=False)