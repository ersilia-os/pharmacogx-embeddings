import pandas as pd
import os
import collections

root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(root, "..", "..", "data"))

# load big dataset of pairs, only to extract proteins and genes data
df = pd.read_csv(os.path.join(data_dir, "ml_datasets_matrix", "chemical_gene_pairs_prediction_input.csv"))
compound_any = collections.defaultdict(int)
compound_pkpd_all = collections.defaultdict(int)
compound_pk_all = collections.defaultdict(int)
compound_pk_adme = collections.defaultdict(int)
gene_any = collections.defaultdict(int)
gene_pkpd_all = collections.defaultdict(int)
gene_pk_all = collections.defaultdict(int)
gene_pk_adme = collections.defaultdict(int)

for r in df.values:
    kc = tuple(r[0], r[1], r[2], r[6], r[8])
    kg = tuple(r[3], r[4], r[5], r[7], r[9])
    is_pkpd_all = r[10]
    is_pk_all = r[11]
    is_pk_adme = r[12]

# compounds
ik2smi = pd.read_csv(os.path.join(data_dir, "chemical_descriptors", "drug_molecules.csv"))
ik2smi = dict(zip(ik2smi["inchikey"], ik2smi["smiles"]))



# proteins