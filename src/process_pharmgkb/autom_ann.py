import os
import sys
import pandas as pd


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

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
    df = df[~df["Gene Symbols"].isna()] #many automated annotations do not have an associated gene because they refer to viral or bacterial genes. These have been removed to avoid confusion
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
        print(gene)
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
    return data

def add_gid(df):
    gene_df = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    mapping_dict = gene_df.set_index("gene")["gid"].to_dict()
    df["gid"] = df["gene"].map(mapping_dict)
    return df



if __name__ == "__main__":
    data = get_raw_files()
    data = deconv_genomic_var(data)
    print(data.head(5))
    data = deconv_gene(data)
    print(data.head(5))
    data = add_gid(data)
    data.to_csv(os.path.join(processed_folder, "autom_ann.csv"),index=False,)
