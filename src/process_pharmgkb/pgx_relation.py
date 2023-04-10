import os
import sys
import pandas as pd
import collections


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner
from pharmgkb import RawData


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def create_table():
    # files to be joined
    int_files = [
        "autom_ann_int.csv",
        "clinical_ann_int.csv",
        "drug_labels_int.csv",
        "var_drug_ann_int.csv",
        "var_fa_ann_int.csv",
        "var_pheno_ann_int.csv",
    ]
    df = pd.DataFrame(
        columns=[
            "aid",
            "genomic_variation",
            "vid",
            "hid",
            "gene",
            "gid",
            "chemical",
            "cid",
            "pd_phenotype",
            "pk_phenotype",
            "evidence",
            "association",
        ]
    )
    for f in int_files:
        df_ = pd.read_csv(os.path.join(processed_folder, "pgx_relation_int", f))
        df = pd.concat([df, df_])
    # add bioG group
    study = pd.read_csv(os.path.join(processed_folder, "study_bio_group.csv"))
    aid2g = collections.defaultdict(list)
    for r in study[["aid", "bid"]].values:
        if str(r[1]) == "nan" or str(r[0]) == "nan":
            continue
        aid2g[r[0]] += [r[1]]
    R = []
    for r in df.values:
        r = list(r)
        if r[0] in aid2g:
            for x in aid2g[r[0]]:
                R += [r + [x]]
        else:
            R += [r + [""]]
    df = pd.DataFrame(R, columns=list(df.columns) + ["bid"])
    df.to_csv(os.path.join(processed_folder, "pgx_relation.csv"), index=False)


if __name__ == "__main__":
    create_table()
