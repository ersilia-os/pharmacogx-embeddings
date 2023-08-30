import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

dl = pd.read_csv(os.path.join(processed_folder, "drug_labels.csv"))

dl = dl[["chemical", "gene", "variant", "haplotype"]]


def hap_to_var(df):
    h2v = pd.read_csv(os.path.join(processed_folder, "hid_vid_complete.csv"))
    h2v = h2v[["hid", "haplotype", "vid", "variant"]]
    df_vid_only = df[df["haplotype"].isna()]
    df_hid_only = df[~df["haplotype"].isna()]
    df_hid_only = df_hid_only.drop(columns=["variant"])
    print(h2v.columns)
    merged_df = pd.merge(df_hid_only, h2v, on=["haplotype"], how="left")
    print(merged_df.columns)
    data = pd.concat([df_vid_only, merged_df], axis=0)
    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data


def add_gid_ensembl_id(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    df_ = df_[["gene", "gid", "ensembl_id"]]
    data = pd.merge(df, df_, on="gene", how="left")
    return data


def add_cid_smiles(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "chemical.csv"))
    df_ = df_[["chemical", "cid", "smiles"]]
    data = pd.merge(df, df_, on="chemical", how="left")
    return data


def clean_haps(df):
    print(df.shape)
    df = df.drop(columns=["hid", "haplotype"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    return data


def add_empty_cols(df):
    df["evidence"] = None
    df["phenotype"] = None
    df["did"] = None
    df["disease"] = None
    df["significance"] = 1
    df["biogroup"] = None
    df["vaid"] = None
    df["caid"] = None
    return df


if __name__ == "__main__":
    dl = pd.read_csv(os.path.join(processed_folder, "drug_labels.csv"))
    print(dl.shape)
    dl = dl[["chemical", "gene", "variant", "haplotype"]]
    dl.drop_duplicates(keep="first", inplace=True)
    print(dl.shape)
    data = hap_to_var(dl)
    data = add_gid_ensembl_id(data)
    data = add_cid_smiles(data)
    data = clean_haps(data)
    data = add_empty_cols(data)
    data = data[
        [
            "cid",
            "chemical",
            "smiles",
            "gid",
            "gene",
            "ensembl_id",
            "vid",
            "variant",
            "evidence",
            "significance",
            "phenotype",
            "did",
            "disease",
            "biogroup",
            "caid",
            "vaid",
        ]
    ]
    data.to_csv(
        os.path.join(processed_folder, "final_tables", "drug_label.csv"), index=False
    )
