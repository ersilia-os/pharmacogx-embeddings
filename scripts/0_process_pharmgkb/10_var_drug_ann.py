import os
import sys
import pandas as pd
import numpy as np

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData
from variant_processing import VariantProcessor

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
    R = []
    p = VariantProcessor()
    for r in df.values:
        vaid = r[0]
        var_hap = r[1]
        gene = r[2]
        phenotype = r[3]
        significance = r[4]
        chemical = r[5]
        var_hap = p.clean_haps(var_hap)
        all_vars = p.all_vars
        all_haps = p.all_haps
        found_in_df1 = var_hap in all_vars["variant"].tolist()
        found_in_df2 = var_hap in all_haps["haplotype"].tolist()
        if not found_in_df1 and not found_in_df2:
            print(f"var_hap '{var_hap}' is not found in df1 or df2.")
        if found_in_df1:
            for i, var_name in enumerate(all_vars["variant"].tolist()):
                if var_hap == var_name:
                    vid = all_vars["vid"].loc[i]
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
            for i, hap_name in enumerate(all_haps["haplotype"].tolist()):
                if var_hap == hap_name:
                    hid = all_haps["hid"].loc[i]
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
    data = data.drop_duplicates(keep="first")
    return data

def add_genes_to_vars(df):
    p = VariantProcessor()
    gene_vid_dict = p.gene_vid_pairs()
    R = []
    for i, row in df.iterrows():
        vaid = row["vaid"]
        vid = row['vid']
        var = row['variant']
        gene = row['gene']
        phenotype = row["phenotype"]
        significance = row["significance"]
        chemical = row['chemical']
        if gene is not None:
            if (gene, vid) not in gene_vid_dict:
                vid = None
                var = None
        R += [[
                        vaid,
                        vid,
                        var,
                        gene,
                        phenotype,
                        significance,
                        chemical,
                    ]]
    cols = [
        "vaid",
        "vid",
        "variant",
        "gene",
        "phenotype",
        "significance",
        "chemical",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def append_study(df):
    df["vaid"] = df["vaid"].astype(str)
    df_ = pd.read_csv(os.path.join(processed_folder, "8_study_parameters.csv"))
    df_["vaid"] = df_["vaid"].astype(str)
    data = pd.merge(df, df_, on="vaid", how="left")
    data = data.drop_duplicates(keep="first")
    return data

if __name__ == "__main__":
    df = get_raw_files()
    p = VariantProcessor()
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
    df = p.eliminate_wt(df)
    print(df.shape)
    #df = p.eliminate_normal_function_allele(df)
    #print(df.shape)
    df = p.hap_to_var(df)
    print(df.shape)
    df = p.clean_dup_haps(df)
    print(df.shape)
    df = add_genes_to_vars(df)
    print(df.shape)
    df = p.add_cid_gid(df)
    print(df.shape)
    df = df.drop(columns=["vaid"])
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    #df = append_study(df)
    df.to_csv(os.path.join(processed_folder, "9_var_drug_ann.csv"), index=False)