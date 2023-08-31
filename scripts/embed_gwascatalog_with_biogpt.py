import pandas as pd
import os
import numpy as np
from tqdm import tqdm
import collections
import sys
import h5py

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "src"))

from biogpt import BioGPTEmbedder

data_path = os.path.join(root, "..", "data", "gwas_ebi")

df = pd.read_csv(os.path.join(data_path, "gwas_catalog_v1.0.2-associations_e110_r2023-07-29.tsv"), sep="\t", low_memory=False)

columns = ["DISEASE/TRAIT", "MAPPED_TRAIT", "PVALUE_MLOG", "MAPPED_GENE", "REPORTED GENE(S)", "STRONGEST SNP-RISK ALLELE", "SNPS", "MERGED", "SNP_ID_CURRENT", "INTERGENIC"]
df = df[columns]
df = df[df["MAPPED_TRAIT"].notnull()]
df = df[df["PVALUE_MLOG"] >= 2]
df = df[df["INTERGENIC"] == 0]
df = df[df["SNPS"].notnull()]

snp2traits = collections.defaultdict(list)

for v in df[["SNPS", "MAPPED_TRAIT"]].values:
    snps = v[0].split(", ")
    traits = v[1].split(", ")
    for snp in snps:
        for trait in traits:
            snp2traits[snp] += [trait]

snp2traits = dict((k, list(set(v))) for k,v in snp2traits.items())

snp2genes = collections.defaultdict(list)

for v in df[["SNPS", "MAPPED_GENE"]].values:
    snps = v[0].split(", ")
    genes = v[1].split(", ")
    for snp in snps:
        for gene in genes:
            snp2genes[snp] += [gene]

snp2genes = dict((k, list(set(v))) for k,v in snp2genes.items())

all_snps = sorted(set([k for k,v in snp2traits.items()]))

texts = []
for snp in all_snps:
    g = snp2genes[snp]
    if len(g) == 1:
        text = "This variant occurs in gene {0} and ".format(g[0])
    else:
        text = "This variant occurs in genes {0} and ".format(", ".join(g))
    t = snp2traits[snp]
    if len(t) == 1:
        text += "is associated with trait {0}.".format(t[0])
    else:
        text += "is associated with traits {0}.".format(" and ".join(t))
    texts += [text]

dt = pd.DataFrame({"rs_id": all_snps, "text": texts})

embedder = BioGPTEmbedder()

X = np.zeros((dt.shape[0], 1024))

keys = []
for i, v in tqdm(enumerate(dt.values)):
    keys += [v[0]]
    X[i,:] = embedder.calculate([v[1]])[0]

h5_output = os.path.join(data_path, "gwas_catalog_biogpt_embeddings.h5")
with h5py.File(h5_output, "w") as f:
    f.create_dataset("keys", data=np.array(keys, dtype=h5py.string_dtype()))
    f.create_dataset("X", data=X)