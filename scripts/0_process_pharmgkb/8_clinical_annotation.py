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
    df = r.clinical_annotations
    return df


def deconv_disease(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        caid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.stringify(r[2])
        evidence = c.stringify(r[3])
        score = c.stringify(r[6])
        phenotype = c.stringify(r[7])
        chemical = c.stringify(r[10])
        disease = c.inline_semicolon_splitter_nospace(r[11])
        if disease is not None:
            for d in disease:
                r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, d]
                R += [r_]
        else:
            r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, disease]
            R += [r_]
    cols = [
        "caid",
        "variant/haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_chemical(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        caid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.stringify(r[2])
        evidence = c.stringify(r[3])
        score = c.stringify(r[4])
        phenotype = c.stringify(r[5])
        chemical = c.inline_semicolon_splitter_nospace(r[6])
        disease = c.stringify(r[7])
        if chemical is not None:
            for ch in chemical:
                r_ = [caid, var_hap, gene, evidence, score, phenotype, ch, disease]
                R += [r_]
        else:
            r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, disease]
            R += [r_]
    cols = [
        "caid",
        "variant/haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_pheno(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        caid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.stringify(r[2])
        evidence = c.stringify(r[3])
        score = c.stringify(r[4])
        phenotype = c.inline_semicolon_splitter(r[5])
        chemical = c.stringify(r[6])
        disease = c.stringify(r[7])
        if phenotype is not None:
            for ph in phenotype:
                r_ = [caid, var_hap, gene, evidence, score, ph, chemical, disease]
                R += [r_]
        else:
            r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, disease]
            R += [r_]
    cols = [
        "caid",
        "variant/haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        caid = c.stringify(r[0])
        var_hap = c.stringify(r[1])
        gene = c.inline_semicolon_splitter(r[2])
        evidence = c.stringify(r[3])
        score = c.stringify(r[4])
        phenotype = c.stringify(r[5])
        chemical = c.stringify(r[6])
        disease = c.stringify(r[7])
        if gene is not None:
            for g in gene:
                r_ = [caid, var_hap, g, evidence, score, phenotype, chemical, disease]
                R += [r_]
        else:
            r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, disease]
            R += [r_]
    cols = [
        "caid",
        "variant/haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_variant(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        caid = c.stringify(r[0])
        var_hap = c.inline_comma_splitter_space(r[1])
        gene = c.stringify(r[2])
        evidence = c.stringify(r[3])
        score = c.stringify(r[4])
        phenotype = c.stringify(r[5])
        chemical = c.stringify(r[6])
        disease = c.stringify(r[7])
        if var_hap is not None:
            for var in var_hap:
                r_ = [caid, var, gene, evidence, score, phenotype, chemical, disease]
                R += [r_]
        else:
            r_ = [caid, var_hap, gene, evidence, score, phenotype, chemical, disease]
            R += [r_]
    cols = [
        "caid",
        "variant/haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def sep_var(df):
    df1 = pd.read_csv(os.path.join(processed_folder, "5_variant_complete.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "2_haplotype.csv"))
    R = []
    for r in df.values:
        caid = r[0]
        var_hap = r[1]
        gene = r[2]
        evidence = r[3]
        score = r[4]
        phenotype = r[5]
        chemical = r[6]
        disease = r[7]
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
                        caid,
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        evidence,
                        score,
                        phenotype,
                        chemical,
                        disease,
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
                        caid,
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        evidence,
                        score,
                        phenotype,
                        chemical,
                        disease,
                    ]
                    R += [r_]
    cols = [
        "caid",
        "vid",
        "variant",
        "hid",
        "haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    data = data.drop_duplicates(keep="first")
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


def add_did(df):
    df_ = pd.read_csv(os.path.join(processed_folder, "0_disease.csv"))
    data = pd.merge(df, df_, on="disease", how="left")
    return data


def clean_haps(df):
    print(df.shape)
    df = df.drop(columns=["hid", "haplotype"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    return df

if __name__ == "__main__":
    df = get_raw_files()
    print(df.shape)
    df = deconv_disease(df)
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
    df = hap_to_var(df)
    df = add_gid_ensembl_id(df)
    df = add_cid_smiles(df)
    df = add_did(df)
    df = clean_haps(df)
    df.to_csv(os.path.join(processed_folder, "6_clinical_annotation.csv"), index=False)
