import os
import sys
import pandas as pd
import numpy as np

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    df = r.var_drug_ann
    return df


def deconv_chemical(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        vaid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.stringify(r[2])
        phenotype = c.stringify(r[5])
        significance = c.stringify(r[6])
        if significance == "yes":
            significance = 1
        elif significance == "no":
            significance = -1
        elif significance == "not stated":
            significance = 0
        chemical = c.inline_comma_splitter_nospace(r[3])
        if chemical is not None:
            for ch in chemical:
                ch = ch.strip('""')
                r_ = [vaid, var_hap, gene, phenotype, significance, ch]
                R += [r_]
        else:
            r_ = [vaid, var_hap, gene, phenotype, significance, chemical]
            R += [r_]
    cols = [
        "vaid",
        "variant/haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_pheno(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        vaid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.stringify(r[2])
        phenotype = c.inline_comma_splitter(r[3])
        significance = r[4]
        chemical = r[5]
        if phenotype is not None:
            for ph in phenotype:
                ph = ph.strip('""')
                r_ = [vaid, var_hap, gene, ph, significance, chemical]
                R += [r_]
        else:
            r_ = [vaid, var_hap, gene, phenotype, significance, chemical]
            R += [r_]
    cols = [
        "vaid",
        "variant/haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        vaid = r[0]
        var_hap = c.stringify(r[1])
        gene = c.inline_comma_splitter(r[2])
        phenotype = r[3]
        significance = r[4]
        chemical = r[5]
        if gene is not None:
            for g in gene:
                g = g.strip('""')
                r_ = [vaid, var_hap, g, phenotype, significance, chemical]
                R += [r_]
        else:
            r_ = [vaid, var_hap, gene, phenotype, significance, chemical]
            R += [r_]
    cols = [
        "vaid",
        "variant/haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_variant(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        vaid = r[0]
        var_hap = c.inline_comma_splitter_space(r[1])
        gene = r[2]
        phenotype = r[3]
        significance = r[4]
        chemical = r[5]
        if var_hap is not None:
            for var in var_hap:
                r_ = [vaid, var, gene, phenotype, significance, chemical]
                R += [r_]
        else:
            r_ = [vaid, var_hap, gene, phenotype, significance, chemical]
            R += [r_]
    cols = [
        "vaid",
        "variant/haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def sep_var(df):
    df1 = pd.read_csv(os.path.join(processed_folder, "5_variant_complete.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "2_haplotype.csv"))
    R = []
    for r in df.values:
        vaid = r[0]
        var_hap = r[1]
        gene = r[2]
        phenotype = r[3]
        significance = r[4]
        chemical = r[5]
        if var_hap.startswith("HLA-"):
            var_hap = ":".join(var_hap.split(":")[:2])
        if var_hap == "G6PD B (wildtype)":
            var_hap = "G6PD B (reference)"
        g6pd_list1 = [
            "G6PD Mediterranean",
            "Dallas",
            "Panama",
            "Sassari",
            "Cagliari",
            "Birmingham",
        ]
        if var_hap in g6pd_list1:
            var_hap = (
                "G6PD Mediterranean, Dallas, Panama, Sassari, Cagliari, Birmingham"
            )
        g6pd_list2 = ["G6PD Canton", "Taiwan-Hakka", "Gifu-like", "Agrigento-like"]
        if var_hap in g6pd_list2:
            var_hap = "G6PD Canton, Taiwan-Hakka, Gifu-like, Agrigento-like"
        found_in_df1 = var_hap in df1["variant"].tolist()
        found_in_df2 = var_hap in df2["haplotype"].tolist()
        if not found_in_df1 and not found_in_df2:
            print(f"var_hap '{var_hap}' is not found in df1 or df2.")
        if found_in_df1:
            for i, var_name in enumerate(df1["variant"].tolist()):
                if var_hap == var_name:
                    vid = df1["vid"].loc[i]
                    var = var_hap
                    hid = None
                    hap = None
                    r_ = [
                        vaid,
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        phenotype,
                        significance,
                        chemical,
                    ]
                    R += [r_]
        if found_in_df2:
            for i, hap_name in enumerate(df2["haplotype"].tolist()):
                if var_hap == hap_name:
                    hid = df2["hid"].loc[i]
                    hap = var_hap
                    vid = None
                    var = None
                    r_ = [
                        vaid,
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        phenotype,
                        significance,
                        chemical,
                    ]
                    R += [r_]
    cols = [
        "vaid",
        "vid",
        "variant",
        "hid",
        "haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data


def append_study(df):
    df["vaid"] = df["vaid"].astype(str)
    df_ = pd.read_csv(os.path.join(processed_folder, "8_study_parameters.csv"))
    df_["vaid"] = df_["vaid"].astype(str)
    data = pd.merge(df, df_, on="vaid", how="left")
    print(data.shape)
    data = data.drop_duplicates(keep="first")
    print(data.shape)
    return data

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
    df_ = df_[["gene", "gid", "ensembl_id"]]
    data = pd.merge(df, df_, on="gene", how="left")
    return data


def add_cid_smiles(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "0_chemical.csv"))
    df_ = df_[["chemical", "cid", "smiles"]]
    data = pd.merge(df, df_, on="chemical", how="left")
    return data


def clean_haps(df):
    print(df.shape)
    df = df.drop(columns=["hid", "haplotype", "sid"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    return df


if __name__ == "__main__":
    df = get_raw_files()
    print(df.shape)
    df = deconv_chemical(df)
    print(df.shape)
    df = deconv_pheno(df)
    print(df.shape)
    df = deconv_gene(df)
    print(df.shape)
    df = deconv_variant(df)
    print(df.shape)
    df = sep_var(df)
    print(df.shape)
    df = append_study(df)
    print(df.shape)
    df = hap_to_var(df)
    df = add_gid_ensembl_id(df)
    df = add_cid_smiles(df)
    df = clean_haps(df)
    df.to_csv(os.path.join(processed_folder, "10_var_drug_ann.csv"), index=False)
