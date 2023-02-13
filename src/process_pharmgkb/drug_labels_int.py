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
    df = r.drug_labels
    return df

def deconv_chemical():
    c = CsvCleaner()
    df = get_raw_files()
    ch = pd.read_csv(os.path.join(processed_folder, "chemical.csv"))
    ch_name = ch["chemical"].tolist()
    ch_id = ch["cid"].tolist()
    R = []
    for r in df.values:
        aid = c.stringify(r[0])
        evidence = c.stringify(r[4])
        if evidence == "Actionable PGx":
            evidence = "0A"
        elif evidence == "Informative PGx":
            evidence = "0B"
        elif evidence == "Testing recommended":
            evidence = "0C"
        elif evidence == "Testing required":
            evidence = "0D"
        gene = c.stringify(r[11])
        genomic_variation = c.stringify(r[12])
        vid = "nan"
        hid = "nan"
        pd_phenotype = "nan"
        pk_phenotype = "nan"
        association = 1 #YES
        chemical = c.inline_quote_splitter(r[10])
        cid = "nan"
        for chem in chemical:
            if chem in ch_name:
                i = ch_name.index(chem)
                cid = ch_id[i]
            r = [aid, genomic_variation, vid, hid, gene, chem, cid, pd_phenotype, pk_phenotype, evidence, association]
        R += [r]
    cols = ["aid", "genomic_variation", "vid", "hid", "gene", "chemical", "cid", "pd_phenotype", "pk_phenotype", "evidence", "association"]
    data = pd.DataFrame(R, columns=cols)
    return data

def deconv_gene():
    c = CsvCleaner()
    data = deconv_chemical()
    gene = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    gene_name = gene["gene"].tolist()
    gene_id = gene["gid"].tolist()
    R = []
    for r in data.values:
        aid = c.stringify(r[0])
        genomic_variation = c.stringify(r[1])
        vid = c.stringify(r[2])
        hid = c.stringify(r[3])
        chemical = c.stringify(r[5])
        cid = c.stringify(r[6])
        pd_phenotype = c.stringify(r[7])
        pk_phenotype = c.stringify(r[8])
        evidence = c.stringify(r[9])
        association = c.stringify(r[10])

        gene = c.inline_quote_splitter(r[4])
        gid = "nan"
        for g in gene:
            if g in gene_name:
                i = gene_name.index(g)
                gid = gene_id[i]

            r = [aid, genomic_variation, vid, hid, g, gid, chemical, cid, pd_phenotype, pk_phenotype, evidence, association]
        R += [r]
    cols = ["aid", "genomic_variation", "vid", "hid", "gene", "gid", "chemical", "cid", "pd_phenotype", "pk_phenotype", "evidence", "association"]
    data = pd.DataFrame(R, columns=cols)
    return data

def create_table():
    data  = deconv_gene()
    data.to_csv(os.path.join(processed_folder, "pgx_relation_int", "drug_labels_int.csv"), index=False)
    
if __name__ == "__main__":
    create_table()