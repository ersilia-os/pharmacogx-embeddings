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

def deconv_genomic_var():
    c = CsvCleaner()
    df = get_raw_files()
    df = df[~(df["Gene Symbols"].isna())]
    R = []
    for r in df.values:
        aid = None
        cid = c.stringify(r[0])
        chemical = c.stringify(r[1])
        gid = c.stringify(r[7])
        gene = c.stringify(r[8])
        pd_phenotype = None
        pk_phenotype = None
        evidence = "6"
        association = 0 #not stated
        var_type = c.stringify(r[5])
        if var_type == "Variant":
            genomic_variation = c.stringify(r[4])
            vid = c.stringify(r[3])
            hid = None
        elif var_type == "Haplotype":
            genomic_variation = c.stringify(r[4])
            vid = None
            hid = c.stringify(r[3])
        r = [aid, genomic_variation, vid, hid, gene, gid, chemical, cid, pd_phenotype, pk_phenotype, evidence, association]
        R += [r]
    cols = ["aid", "genomic_variation", "vid", "hid", "gene", "gid", "chemical", "cid", "pd_phenotype", "pk_phenotype", "evidence", "association"]
    data = pd.DataFrame(R, columns=cols)
    return data

def deconv_gene():
    c = CsvCleaner()
    data = deconv_genomic_var()
    R = []
    for r in data.values:
        aid = c.stringify(r[0])
        genomic_variation = c.stringify(r[1])
        vid = c.stringify(r[2])
        hid = c.stringify(r[3])
        chemical = c.stringify(r[6])
        cid = c.stringify(r[7])
        pd_phenotype = c.stringify(r[8])
        pk_phenotype = c.stringify(r[9])
        evidence = c.stringify(r[10])
        association = c.stringify(r[11])
        gene = c.inline_quote_splitter(r[4])
        for i,g in enumerate(gene):
            gid = c.inline_quote_splitter(r[5])[i]
            r = [aid, genomic_variation, vid, hid, g, gid, chemical, cid, pd_phenotype, pk_phenotype, evidence, association]
        R += [r]
    cols = ["aid", "genomic_variation", "vid", "hid", "gene", "gid", "chemical", "cid", "pd_phenotype", "pk_phenotype", "evidence", "association"]
    data = pd.DataFrame(R, columns=cols)
    data.drop_duplicates(keep="first", inplace=True)
    return data

def create_table():
    data  = deconv_gene()
    data.to_csv(os.path.join(processed_folder, "pgx_relation_int", "autom_ann_int.csv"), index=False)
    

if __name__ == "__main__":
    create_table()