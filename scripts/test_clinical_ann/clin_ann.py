import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from variant_processing import VariantProcessor


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


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
    R = []
    p = VariantProcessor()
    for r in df.values:
        caid = r[0]
        var_hap = r[1]
        gene = r[2]
        evidence = r[3]
        score = r[4]
        phenotype = r[5]
        chemical = r[6]
        disease = r[7]
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
            for i, hap_name in enumerate(all_haps["haplotype"].tolist()):
                if var_hap == hap_name:
                    hid = all_haps["hid"].loc[i]
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

def eliminate_wt(df):
    #eliminates the WT allele as it is NOT a PGX association
    for i, row in df.iterrows():
        haplotype = row["haplotype"]
        if haplotype is not None and "reference" in haplotype:
            df.drop(i, inplace=True)
    return df

if __name__ == "__main__":
    filename = "clinical_ann_test"
    df = pd.read_csv("{}.csv".format(filename))
    p = VariantProcessor()
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
    df = eliminate_wt(df)
    print(df.shape)
    df = p.add_columns(df)
    print(df.shape)
    df.to_csv("{}_dec.csv".format(filename), index=False)