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
    df = r.var_pheno_ann
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
        phenotype =r[3]
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
    df1 = pd.read_csv(os.path.join(processed_folder, "variant.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    R = []
    for r in df.values:
        vaid = r[0]
        var_hap = r[1]
        gene = r[2]
        phenotype = r[3]
        significance = r[4]
        chemical = r[5]
        for i, var_name in enumerate(df1["variant"].tolist()):
            if var_hap == var_name:
                vid = df1["vid"].loc[i]
                var = var_hap
                hid = None
                hap = None
                r_ = [vaid, vid, var, hid, hap, gene, phenotype, significance, chemical]
        for i, hap_name in enumerate(df2["haplotype"].tolist()):
            if var_hap == hap_name:
                hid = df2["hid"].loc[i]
                hap = var_hap
                vid = None
                var = None
                r_ = [vaid, vid, var, hid, hap, gene, phenotype, significance, chemical]
        R += [r_]
    cols = [
        "vaid",
        "vid", "variant",
        "hid", "haplotype",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data

def append_study(df):
    df["vaid"] = df["vaid"].astype(str)
    df_ = pd.read_csv(os.path.join(processed_folder, "study_parameters.csv"))
    df_["vaid"] = df_["vaid"].astype(str)
    data = pd.merge(df, df_, on="vaid", how="left")
    return data


if __name__ == "__main__":
    df = get_raw_files()
    df = deconv_chemical(df)
    df = deconv_pheno(df)
    df = deconv_gene(df)
    df = deconv_variant(df)
    df = sep_var(df)
    df = append_study(df)
    df.to_csv(os.path.join(processed_folder, "var_pheno_ann.csv"), index=False)