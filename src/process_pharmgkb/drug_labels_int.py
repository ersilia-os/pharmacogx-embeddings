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
        aid = c.stringify(r[0]) #drug labels are given a specific PharmGKB AID
        evidence = "1A" #all variants and haplotypes that have drug labels are classified as 1A
        association = 1  # By default, there is association
        gene = c.stringify(r[11]) #multiple genes can be associated to the same annotation
        genomic_variation = c.stringify(r[12]) #not all genes have an identified genomic variation
        vid = "nan" #will depend on the genomic variation
        hid = "nan" #will depend on the genomic variation
        pd_phenotype = "nan" #no phenotype available in the table
        pk_phenotype = "nan" #no phenotype available in the table
        
        chemical = c.stringify(r[10])
        cid = "nan"
        if chemical in ch_name:
            i = ch_name.index(chemical)
            cid = ch_id[i]
        r = [
            aid,
            genomic_variation,
            vid,
            hid,
            gene,
            chemical,
            cid,
            pd_phenotype,
            pk_phenotype,
            evidence,
            association,
        ]
        R += [r]
    cols = [
        "aid",
        "genomic_variation",
        "vid",
        "hid",
        "gene",
        "chemical",
        "cid",
        "pd_phenotype",
        "pk_phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data

def get_genes_from_vars():
    c = CsvCleaner()
    data = deconv_chemical()
    vars = pd.read_csv(os.path.join(processed_folder, "variant.csv"))
    haps = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    genes = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    variants = vars["variant"]
    haplotypes = haps["haplotype"]
    R = []
    for r in data.values:
        aid = c.stringify(r[0])
        genomic_variation = c.stringify(r[1])
        vid = "nan"
        hid = "nan"
        gene = c.stringify(r[4])
        chemical = c.stringify(r[5])
        cid = c.stringify(r[6])
        pd_phenotype = c.stringify(r[7])
        pk_phenotype = c.stringify(r[8])
        evidence = c.stringify(r[9])
        association = c.stringify(r[10])
        gid = "nan"
        for g in c.inline_semicolon_splitter_space(genomic_variation):
            if g in variants:
                i = variants.index(g)
                gid = vars.loc[i, "gid"]
                gene = genes.loc[genes["gid"]==gid, "gene"]
            elif g in haplotypes:
                i  = haplotypes.index(g)
                hid = haps.loc[i, "hid"]
                gid =  haps.loc[i, "gid"]
                gene = genes.loc[genes["gid"]==gid, "gene"]
            r = [
                aid,
                genomic_variation,
                vid,
                hid,
                gene,
                gid,
                chemical,
                cid,
                pd_phenotype,
                pk_phenotype,
                evidence,
                association,
            ]
            R += [r]
    cols = [
        "aid",
        "genomic_variation",
        "vid",
        "hid",
        "gene",
        "gid",
        "chemical",
        "cid",
        "pd_phenotype",
        "pk_phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data

"""
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
        gene = c.inline_semicolon_splitter_space(r[4])
        gid = "nan"
        if gene is None:
            r = [
                aid,
                genomic_variation,
                vid,
                hid,
                gene,
                gid,
                chemical,
                cid,
                pd_phenotype,
                pk_phenotype,
                evidence,
                association,
            ]
            R += [r]
        for g in gene:
            if g in gene_name:
                i = gene_name.index(g)
                gid = gene_id[i]
            r = [
                aid,
                genomic_variation,
                vid,
                hid,
                g,
                gid,
                chemical,
                cid,
                pd_phenotype,
                pk_phenotype,
                evidence,
                association,
            ]
            R += [r]
    cols = [
        "aid",
        "genomic_variation",
        "vid",
        "hid",
        "gene",
        "gid",
        "chemical",
        "cid",
        "pd_phenotype",
        "pk_phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data
"""

def create_table():
    data = get_genes_from_vars()
    data.to_csv(
        os.path.join(processed_folder, "pgx_relation_int", "drug_labels_int.csv"),
        index=False,
    )

if __name__ == "__main__":
    create_table()
