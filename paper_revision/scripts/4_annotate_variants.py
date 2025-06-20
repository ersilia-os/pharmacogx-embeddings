import os
import pandas as pd
import collections
import numpy as np
import sys

exp = sys.argv[1]

root = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    root,
    "..",
    "results",
    f"results_pairs_{exp}",
    "chemical_gene_pairs_prediction_output_focus.csv",
)

df = pd.read_csv(file_path)

uniprot_acs = set(df["uniprot_ac"])

uniprot_ensemble_mapping = pd.read_csv(
    os.path.join(
        root,
        "..",
        "..",
        "data",
        "variants",
        "uniprotac_gene_mapping",
        "ensembl_uniprot_mapping_of_variants.tsv",
    ),
    sep="\t",
)

gene_level_variants = pd.read_csv(
    os.path.join(
        root,
        "..",
        "..",
        "data",
        "variants",
        "1000_Genomes",
        "subset_snvs_protein_coding_1kGPhg38_gene_level.tsv",
    ),
    sep="\t",
)

data_ = collections.defaultdict(list)
for uniprot_ac in uniprot_acs:
    ensembl_subset = list(
        uniprot_ensemble_mapping[uniprot_ensemble_mapping["Entry"] == uniprot_ac][
            "From"
        ]
    )
    for g in ensembl_subset:
        gene_level_variants_subset = gene_level_variants[
            gene_level_variants["ensemble_id"] == g
        ]
        R = []
        for r in gene_level_variants_subset.values:
            R += [list(r)]
        data_[uniprot_ac] += R

data = {}
for k in uniprot_acs:
    if k not in data_:
        v = []
    else:
        v = data_[k]
    if len(v) == 0:
        data[k] = [0] * 12 + [""]
    else:
        R = []
        point_mutations = []
        for x in v:
            pm = x[-1]
            if str(pm) != "nan":
                point_mutations += [pm]
        point_mutations = sorted(set(point_mutations))
        for x in v:
            R += [x[2:-1]]
        R = np.array(R)
        data[k] = [int(x) for x in list(np.sum(R, axis=0))] + [";".join(point_mutations)]

R = []
for uniprot_ac in list(df["uniprot_ac"]):
    R += [data[uniprot_ac]]

s = "total_variants	intron_variants	missense_variants	other_variants	afr_abundant_variants	afr_abundant_intron_variants	afr_abundant_missense_variants	afr_abundant_other_variants	afr_specific_variants	afr_specific_intron_variants	afr_specific_missense_variants	afr_specific_other_variants	afr_specific_missense_variants_mutations"
list_of_strings = s.split()

columns = list(df.columns)
cut = columns.index("adme_gene") + 1
df_0 = df[columns[:cut]]
df_1 = pd.DataFrame(R, columns=list_of_strings)
df_2 = df[columns[cut:]]

df_final = pd.concat([df_0, df_1, df_2], axis=1)

df_final.to_csv(
    os.path.join(
        root,
        "..",
        "results",
        f"results_pairs_{exp}",
        "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates.csv",
    ),
    index=False,
)
