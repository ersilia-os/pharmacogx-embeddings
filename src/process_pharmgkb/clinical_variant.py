import os
import sys
import pandas as pd
import numpy as np

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner
from pharmgkb import RawData

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    df = r.clinical_variants
    return df


def deconv_disease(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        variant = c.stringify(r[0])
        gene = c.stringify(r[1])
        phenotype = c.stringify(r[2])
        evidence = c.stringify(r[3])
        chemical = c.stringify(r[4])
        disease = c.inline_comma_splitter_nospace(r[5])
        if disease is not None:
            for d in disease:
                r_ = [variant, gene, phenotype, evidence, chemical, d]
                R += [r_]
        else:
            r_ = [variant, gene, phenotype, evidence, chemical, disease]
            R += [r_]
    cols = [
        "variant/haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_chemical(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        variant = c.stringify(r[0])
        gene = c.stringify(r[1])
        phenotype = c.stringify(r[2])
        evidence = c.stringify(r[3])
        chemical = c.inline_comma_splitter_nospace(r[4])
        disease = c.stringify(r[5])
        if chemical is not None:
            for ch in chemical:
                r_ = [variant, gene, phenotype, evidence, ch, disease]
                R += [r_]
        else:
            r_ = [variant, gene, phenotype, evidence, chemical, disease]
            R += [r_]
    cols = [
        "variant/haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_pheno(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        variant = c.stringify(r[0])
        gene = c.stringify(r[1])
        phenotype = c.inline_comma_splitter(r[2])
        evidence = c.stringify(r[3])
        chemical = c.stringify(r[4])
        disease = c.stringify(r[5])
        if phenotype is not None:
            for ph in phenotype:
                r_ = [variant, gene, ph, evidence, chemical, disease]
                R += [r_]
        else:
            r_ = [variant, gene, phenotype, evidence, chemical, disease]
            R += [r_]
    cols = [
        "variant/haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        variant = c.stringify(r[0])
        gene = c.inline_comma_splitter(r[1])
        phenotype = c.stringify(r[2])
        evidence = c.stringify(r[3])
        chemical = c.stringify(r[4])
        disease = c.stringify(r[5])
        if gene is not None:
            for g in gene:
                r_ = [variant, g, phenotype, evidence, chemical, disease]
                R += [r_]
        else:
            r_ = [variant, gene, phenotype, evidence, chemical, disease]
            R += [r_]
    cols = [
        "variant/haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_variant(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        variant = c.inline_comma_splitter_space(r[0])
        gene = c.stringify(r[1])
        phenotype = c.stringify(r[2])
        evidence = c.stringify(r[3])
        chemical = c.stringify(r[4])
        disease = c.stringify(r[5])
        if variant is not None:
            for var in variant:
                r_ = [var, gene, phenotype, evidence, chemical, disease]
                R += [r_]
        else:
            r_ = [variant, gene, phenotype, evidence, chemical, disease]
            R += [r_]
    cols = [
        "variant/haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def sep_var(df):
    df1 = pd.read_csv(os.path.join(processed_folder, "variant_complete.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    R = []
    for r in df.values:
        gene = r[1]
        phenotype = r[2]
        evidence = r[3]
        chemical = r[4]
        disease = r[5]
        var_hap = r[0]
        if var_hap.startswith("HLA-"):
            var_hap =':'.join(var_hap.split(':')[:2])
        if var_hap == "G6PD B (wildtype)":
            var_hap = "G6PD B (reference)"
        g6pd_list1 = ["G6PD Mediterranean", "Dallas", "Panama", "Sassari", "Cagliari", "Birmingham", ]
        if var_hap in g6pd_list1:
            var_hap = "G6PD Mediterranean, Dallas, Panama, Sassari, Cagliari, Birmingham"
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
                    r_ = [vid, var, hid, hap, gene, phenotype, evidence, chemical, disease]
                    R += [r_]
        if found_in_df2:
            for i, hap_name in enumerate(df2["haplotype"].tolist()):
                if var_hap == hap_name:
                    hid = df2["hid"].loc[i]
                    hap = var_hap
                    vid = None
                    var = None
                    r_ = [vid, var, hid, hap, gene, phenotype, evidence, chemical, disease]
                    R += [r_]
    cols = [
        "vid",
        "variant",
        "hid",
        "haplotype",
        "gene",
        "phenotype",
        "evidence",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    print(data.shape)
    data = data.drop_duplicates(keep = "first")
    print(data.shape)
    return data


if __name__ == "__main__":
    df = get_raw_files()
    df = deconv_disease(df)
    df = deconv_chemical(df)
    df = deconv_pheno(df)
    df = deconv_gene(df)
    df = deconv_variant(df)
    df = sep_var(df)
    df.to_csv(os.path.join(processed_folder, "clinical_variant.csv"), index=False)
