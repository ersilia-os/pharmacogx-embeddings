import os
import sys
import pandas as pd


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    autom_ann = r.automated_annotations
    return autom_ann


def deconv_genomic_var(df):
    c = CsvCleaner()
    R = []
    df = df[
        ~df["Gene Symbols"].isna()
    ]  # many automated annotations do not have an associated gene because they refer to viral or bacterial genes. These have been removed to avoid confusion
    for r in df.values:
        cid = c.stringify(r[0])
        chemical = c.stringify(r[1])
        gene = c.stringify(r[8])
        var_type = c.stringify(r[5])
        if var_type == "Variant":
            var = c.stringify(r[4])
            vid = c.stringify(r[3])
            hap = None
            hid = None
        elif var_type == "Haplotype":
            var = None
            hap = None
            hap = c.stringify(r[4])
            hid = c.stringify(r[3])
        r_ = [
            chemical,
            cid,
            gene,
            var,
            vid,
            hap,
            hid,
        ]
        R += [r_]
    cols = ["chemical", "cid", "gene", "variant", "vid", "haplotype", "hid"]
    data = pd.DataFrame(R, columns=cols)

    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data


def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        chemical = r[0]
        cid = r[1]
        gene = c.inline_comma_splitter(r[2])
        var = r[3]
        vid = r[4]
        hap = r[5]
        hid = r[6]
        for g in gene:
            r_ = [
                chemical,
                cid,
                g,
                var,
                vid,
                hap,
                hid,
            ]
            R += [r_]
    cols = ["chemical", "cid", "gene", "variant", "vid", "haplotype", "hid"]
    data = pd.DataFrame(R, columns=cols)
    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data


def add_gid(df):
    gene_df = pd.read_csv(os.path.join(processed_folder, "0_gene.csv"))
    mapping_dict = gene_df.set_index("gene")["gid"].to_dict()
    df["gid"] = df["gene"].map(mapping_dict)
    return df

def hap_to_var(df):
    print(df.shape)
    h2v = pd.read_csv(os.path.join(processed_folder, "3_hid_vid_complete.csv"))
    h2v = h2v[["hid", "haplotype", "vid", "variant"]]
    df_vid_only = df[df["hid"].isna()]
    df_hid_only = df[~df["hid"].isna()]
    df_hid_only = df_hid_only.drop(columns=["vid", "variant"])
    merged_df = pd.merge(df_hid_only, h2v, on=["haplotype", "hid"], how="left")
    data = pd.concat([df_vid_only, merged_df], axis=0)
    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data


def add_gid_ensembl_id(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "0_gene.csv"))
    df_ = df_[["gene", "ensembl_id"]]
    data = pd.merge(df, df_, on="gene", how="left")
    return data


def add_cid_smiles(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "0_chemical.csv"))
    df_ = df_[["chemical", "smiles"]]
    data = pd.merge(df, df_, on="chemical", how="left")
    return data


def clean_haps(df):
    print(df.shape)
    df = df.drop(columns=["hid", "haplotype"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    return df

if __name__ == "__main__":
    data = get_raw_files()
    print(data.shape)
    data = deconv_genomic_var(data)
    print(data.shape)
    data = deconv_gene(data)
    print(data.shape)
    data = add_gid(data)
    print(data.shape)
    data = hap_to_var(data)
    data = add_gid_ensembl_id(data)
    data = add_cid_smiles(data)
    data = clean_haps(data)
    data.to_csv(
        os.path.join(processed_folder, "12_autom_ann.csv"),
        index=False,
    )
