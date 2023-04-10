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
    var_fa_ann = r.var_fa_ann
    return var_fa_ann


def deconv_genomic_var():
    c = CsvCleaner()
    var_fa_ann = get_raw_files()
    variant = pd.read_csv(os.path.join(processed_folder, "variant.csv"))
    var_name = variant["variant"].tolist()
    var_id = variant["vid"].tolist()
    haplotype = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    hap_name = haplotype["haplotype"].tolist()
    hap_id = haplotype["hid"].tolist()
    R = []
    for r in var_fa_ann.values:
        aid = c.stringify(r[0])
        gene = c.stringify(r[2])
        chemical = c.stringify(r[3])
        phenotype = c.stringify(r[5])
        evidence = "5C"
        association = c.stringify(r[6])
        if association == "yes":
            association = 1
        elif association == "no":
            association = -1
        elif association == "not stated":
            association = 0
        genomic_variation = c.inline_comma_splitter_space(r[1])
        vid = None
        hid = None
        for g in genomic_variation:
            if g in var_name:
                i = var_name.index(g)
                vid = var_id[i]
            elif g in hap_name:
                i = hap_name.index(g)
                hid = hap_id[i]
            else:
                print(g)
            r = [aid, g, vid, hid, gene, chemical, phenotype, evidence, association]
        R += [r]
    cols = [
        "aid",
        "genomic_variation",
        "vid",
        "hid",
        "gene",
        "chemical",
        "phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_gene():
    c = CsvCleaner()
    data = deconv_genomic_var()
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
        phenotype = c.stringify(r[6])
        evidence = c.stringify(r[7])
        association = c.stringify(r[8])

        gene = c.inline_quote_splitter(r[4])
        gid = None
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
                phenotype,
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
        "phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_chemical():
    c = CsvCleaner()
    data = deconv_gene()
    ch = pd.read_csv(os.path.join(processed_folder, "chemical.csv"))
    ch_name = ch["chemical"].tolist()
    ch_id = ch["cid"].tolist()
    R = []
    for r in data.values:
        aid = c.stringify(r[0])
        genomic_variation = c.stringify(r[1])
        vid = c.stringify(r[2])
        hid = c.stringify(r[3])
        gene = c.stringify(r[4])
        gid = c.stringify(r[5])
        phenotype = c.stringify(r[7])
        evidence = c.stringify(r[8])
        association = c.stringify(r[9])

        chemical = c.inline_quote_splitter(r[6])
        cid = None
        for chem in chemical:
            if chem in ch_name:
                i = ch_name.index(chem)
                cid = ch_id[i]

            r = [
                aid,
                genomic_variation,
                vid,
                hid,
                gene,
                gid,
                chem,
                cid,
                phenotype,
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
        "phenotype",
        "evidence",
        "association",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_pheno():
    c = CsvCleaner()
    data = deconv_chemical()
    pd_pheno = pd.read_csv(os.path.join(processed_folder, "pd_phenotype.csv"))
    pd_pheno_name = pd_pheno["pd_phenotype"].tolist()
    pk_pheno = pd.read_csv(os.path.join(processed_folder, "pk_phenotype.csv"))
    pk_pheno_name = pk_pheno["pk_phenotype"].tolist()
    R = []
    for r in data.values:
        aid = c.stringify(r[0])
        genomic_variation = c.stringify(r[1])
        vid = c.stringify(r[2])
        hid = c.stringify(r[3])
        gene = c.stringify(r[4])
        gid = c.stringify(r[5])
        chemical = c.stringify(r[6])
        cid = c.stringify(r[7])
        evidence = c.stringify(r[9])
        association = c.stringify(r[10])

        phenotype = c.inline_quote_splitter_noslash(r[8])
        pd_phenotype = None
        pk_phenotype = None
        for p in phenotype:
            if p in pd_pheno_name:
                pd_phenotype = p
            elif p in pk_pheno_name:
                pk_phenotype = p
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


def create_table():
    data = deconv_pheno()
    data.to_csv(
        os.path.join(processed_folder, "pgx_relation_int", "var_fa_ann_int.csv"),
        index=False,
    )


if __name__ == "__main__":
    create_table()
