import os
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(root, "..", "..", "src"))
from tldr import DrugTLDR

data_dir = os.path.join(root, "..", "..", "data")

print("Mapping DrugBank to any of our identifiers...")
print("...Print getting the identifiers of the drugs explored in this study...")
df = pd.read_csv(os.path.join(root, "..", "..", "data", "ml_datasets_pairs", "chemical_gene_pairs_prediction_input.csv"))

drugs = []
for r in df[["cid", "chemical"]].values:
    drugs += [(r[0], r[1])]
drugs = list(set(drugs))

print("... Getting TLDRs for the {0} drugs...".format(len(drugs)))

print("Reading drugbank identifiers")
cid2dbid = {}
df = pd.read_csv(os.path.join(data_dir, "drugbank", "cid2drugbank.csv"))
for r in df[["cid", "drugbank_id"]].values:
    cid2dbid[r[0]] = r[1]

tldr = DrugTLDR()

for i, drug in enumerate(drugs):
    cid = drug[0]
    drug_name = drug[1]
    file_name = os.path.join(data_dir, "tldr", "drugs", "{0}.md".format(cid))
    if os.path.exists(file_name):
        continue
    if cid in cid2dbid:
        dbid = cid2dbid[cid]
        print(i, dbid)
        text = tldr.get(dbid)
    else:
        text = tldr.get(drug_name)
        print(i, drug_name)
    with open(file_name, "w") as f:
        f.write(text)
