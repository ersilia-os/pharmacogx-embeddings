import os
import sys
import pandas as pd
import numpy as np

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", ".."))

data_folder = os.path.abspath(os.path.join(root, "..","..","..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
final_folder = os.path.join(data_folder, "pharmgkb_processed", "final_tables")

def hap_to_var(df):
    print(df.shape)
    h2v = pd.read_csv(os.path.join(processed_folder, "hid_vid_complete.csv"))
    h2v = h2v[["hid", "haplotype", "vid", "variant"]]
    df_vid_only = df[df["hid"].isna()]
    df_hid_only = df[~df["hid"].isna()]
    df_hid_only = df_hid_only.drop(columns=["vid", "variant"])
    merged_df = pd.merge(df_hid_only, h2v, on = ["haplotype", "hid"], how = "left")
    data = pd.concat([df_vid_only, merged_df], axis=0)
    print(data.shape)
    data = data.drop_duplicates(keep = "first")
    print(data.shape)
    return data

def add_gid_ensembl_id(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    df_ = df_[["gene",  "ensembl_id"]]
    data = pd.merge(df, df_, on="gene", how="left")
    return data
    
def add_cid_smiles(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "chemical.csv"))
    df_ = df_[["chemical", "smiles"]]
    data = pd.merge(df, df_, on="chemical", how="left")
    return data

def clean_haps(df):
    print(df.shape)
    df = df.drop(columns=["hid", "haplotype"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    return data

def add_empty_cols(df):
    df["disease"]= None
    df["did"] = None
    df["evidence"] = 5
    df["significance"] = None
    df["phenotype"] = None
    df["biogroup"] = None
    df["vaid"]= None
    df["caid"] = None
    return df



df = pd.read_csv(os.path.join(processed_folder, "autom_ann.csv"))
data = hap_to_var(df)
data = add_gid_ensembl_id(data)
data = add_cid_smiles(data)
data = clean_haps(data)
data = add_empty_cols(data)
data = data[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", "vid", "variant","evidence", 
             "significance", "phenotype","did", "disease","biogroup", "caid", "vaid"]]
data.to_csv(os.path.join(final_folder, "autom_ann.csv"), index=False)