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
    
    cols = list(df.columns)
    key_columns=[
        "genomic_variation",
        "vid",
        "hid",
        "gene",
        "gid",
        "chemical",
        "cid",
        "pd_phenotype",
        "pk_phenotype",
    ]
    value_columns = [
        "aid",
        "evidence",
        "association"
    ]

    clinical_evidences = set(["1A", "1B", "2A", "2B", "3", "4"])
    key_col_idxs = [i for i,k in enumerate(cols) if k in key_columns]
    val_col_idxs = [i for i,k in enumerate(cols) if k in value_columns]
    data = collections.defaultdict(list)
    for v in df.values:
        ks = tuple(list(v[key_col_idxs]))
        vs = list(v[val_col_idxs])
        data[ks] += [vs]
    
    data_ = {}
    for k,v in data.items():
        evid = None
        asso = None
        cann = None
        vann = None
        aann = None
        for x in v:
            if str(x[1]) in clinical_evidences:
                evid = str(x[1])
                asso = int(x[2])
            if x[0] in all_cann:
                cann = x[0]
            if x[0] in all_vann:
                vann = x[0]
            if x[0] in all_aann:
                aann = x[0]
        if evid is None:
            for x in v:
                if evid is None:
                    evid = str(x[1])
                    asso = int(x[2])
                else:
                    if int(str(x[1])[0]) > int(evid[0]):
                        evid = str(x[1])
                        asso = int(x[2])
        data_[k] = (cann, vann, aann, evid, asso)


    print(df.shape[0], len(data))

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
    #df.to_csv(os.path.join(processed_folder, "pgx_relation.csv"), index=False)


if __name__ == "__main__":
    create_table()
