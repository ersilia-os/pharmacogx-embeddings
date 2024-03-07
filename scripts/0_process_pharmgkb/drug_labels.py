import os
import sys
import pandas as pd
import collections

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


def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        dlid = c.stringify(r[0])
        source = c.stringify(r[2])
        drug_label = c.stringify(r[4])
        if drug_label == "Testing required":
            drug_label = 1
        elif drug_label == "Testing recommended":
            drug_label = 2
        elif drug_label == "Actionable PGx":
            drug_label = 3
        elif drug_label == "Informative PGx":
            drug_label = 4
        else:
            drug_label = -1
        prescribing = c.stringify(r[5])
        if prescribing == "Prescribing Info":
            prescribing = 1
        else:
            prescribing = -1
        dosing = c.stringify(r[6])
        if dosing == "Dosing Info":
            dosing = 1
        else:
            dosing = -1
        chemical = c.stringify(r[10])
        gene = c.inline_semicolon_splitter_space(r[11])
        var_hap = c.stringify(r[12])
        if gene is not None:  # if gene is none, do not keep record
            for g in gene:
                r_ = [
                    dlid,
                    source,
                    drug_label,
                    prescribing,
                    dosing,
                    chemical,
                    g,
                    var_hap,
                ]
                R += [r_]
    cols = [
        "dlid",
        "source",
        "drug_label",
        "prescribing_guideline",
        "dosing_guideline",
        "chemical",
        "gene",
        "hap_var",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_hap_variant(df):
    c = CsvCleaner()
    vars = pd.read_csv(os.path.join(processed_folder, "variant_complete.csv"))
    haps = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    variants = vars["variant"].tolist()
    haplotypes = haps["haplotype"].tolist()
    R = []
    for r in df.values:
        dlid = r[0]
        source = r[1]
        drug_label = r[2]
        prescribing = r[3]
        dosing = r[4]
        chemical = r[5]
        gene = r[6]
        var_hap = c.inline_semicolon_splitter_space(r[7])
        if var_hap is not None:
            for vh in var_hap:
                if vh in variants:
                    i = variants.index(vh)
                    hap = None
                    gene_ = vars.loc[i, "gene"]
                    if gene_ == gene:
                        var = vh
                        r_ = [
                            dlid,
                            source,
                            drug_label,
                            prescribing,
                            dosing,
                            chemical,
                            gene_,
                            var,
                            hap,
                        ]
                    else:
                        var = None
                        r_ = [
                            dlid,
                            source,
                            drug_label,
                            prescribing,
                            dosing,
                            chemical,
                            gene,
                            var,
                            hap,
                        ]
                elif vh in haplotypes:
                    var = None
                    i = haplotypes.index(vh)
                    gene_ = haps.loc[i, "gene"]
                    if gene == gene_:
                        hap = vh
                        r_ = [
                            dlid,
                            source,
                            drug_label,
                            prescribing,
                            dosing,
                            chemical,
                            gene_,
                            var,
                            hap,
                        ]
                    else:
                        hap = None
                        r_ = [
                            dlid,
                            source,
                            drug_label,
                            prescribing,
                            dosing,
                            chemical,
                            gene,
                            var,
                            hap,
                        ]
                else:
                    var = None
                    hap = None
                    r_ = [
                        dlid,
                        source,
                        drug_label,
                        prescribing,
                        dosing,
                        chemical,
                        gene,
                        var,
                        hap,
                    ]
                R += [r_]
        else:
            var = None
            hap = None
            r_ = [
                dlid,
                source,
                drug_label,
                prescribing,
                dosing,
                chemical,
                gene,
                var,
                hap,
            ]
            R += [r_]
    cols = [
        "dlid",
        "source",
        "drug_label",
        "prescribing_guideline",
        "dosing_guideline",
        "chemical",
        "gene",
        "variant",
        "haplotype",
    ]
    data = pd.DataFrame(R, columns=cols)
    data = data.drop_duplicates(keep="first")
    d = collections.defaultdict(list)
    for r in data.values:
        k = tuple(r[:-2])
        v = tuple(r[-2:])
        d[k] += [v]
    d_ = {}
    for k, v in d.items():
        if len(v) > 1:
            v_ = [x for x in v if x[0] is not None or x[1] is not None]
        else:
            v_ = v
        d_[k] = v_
    R = []
    for k, v in d_.items():
        for x in v:
            R += [list(k) + list(x)]
    data = pd.DataFrame(R, columns=list(data.columns))
    return data


def deconv_chemical(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        dlid = r[0]
        source = r[1]
        drug_label = r[2]
        prescribing = r[3]
        dosing = r[4]
        chemical = c.inline_semicolon_splitter_space(r[5])
        gene = r[6]
        var = r[7]
        hap = r[8]
        if chemical is not None:
            for ch in chemical:
                r_ = [dlid, source, drug_label, prescribing, dosing, ch, gene, var, hap]
                R += [r_]
        else:
            r_ = [
                dlid,
                source,
                drug_label,
                prescribing,
                dosing,
                chemical,
                gene,
                var,
                hap,
            ]
            R += [r_]
    cols = [
        "dlid",
        "source",
        "drug_label",
        "prescribing_guideline",
        "dosing_guideline",
        "chemical",
        "gene",
        "variant",
        "haplotype",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


if __name__ == "__main__":
    df = get_raw_files()
    df = deconv_gene(df)
    df = deconv_hap_variant(df)
    df = deconv_chemical(df)
    df.to_csv(os.path.join(processed_folder, "drug_labels.csv"), index=False)
