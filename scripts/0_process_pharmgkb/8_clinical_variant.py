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
    R = []
    for r in df.values:
        gene = r[1]
        phenotype = r[2]
        evidence = r[3]
        chemical = r[4]
        disease = r[5]
        var_hap = r[0]
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
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        evidence,
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
                        vid,
                        var,
                        hid,
                        hap,
                        gene,
                        evidence,
                        phenotype,
                        chemical,
                        disease,
                    ]
                    R += [r_]
    cols = [
        "vid",
        "variant",
        "hid",
        "haplotype",
        "gene",
        "evidence",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    data = data.drop_duplicates(keep="first")
    return data

def add_genes_to_vars(df):
    p = VariantProcessor()
    gene_vid_dict = p.gene_vid_pairs()
    R = []
    for i, row in df.iterrows():  
        vid = row['vid']
        var = row['variant']
        gene = row['gene']
        evidence = row["evidence"]
        phenotype = row["phenotype"]
        chemical = row['chemical']
        disease = row['disease']
        if gene is not None:
            if (gene, vid) not in gene_vid_dict:
                vid = None
                var = None
        R += [[
                        vid,
                        var,
                        gene,
                        evidence,
                        phenotype,
                        chemical,
                        disease,
                    ]]
    cols = [
        "vid",
        "variant",
        "gene",
        "evidence",
        "phenotype",
        "chemical",
        "disease",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data

if __name__ == "__main__":
    df = get_raw_files()
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
    df = p.eliminate_wt(df)
    print(df.shape)
    #df = p.eliminate_normal_function_allele(df)
    #print(df.shape)
    df = p.hap_to_var(df)
    print(df.shape)
    df = p.clean_dup_haps(df)
    print(df.shape)
    df = add_genes_to_vars(df)
    df = p.add_gid_cid_did(df)
    print(df.shape)
    df.to_csv(os.path.join(processed_folder, "7_clinical_variant.csv"), index=False)

