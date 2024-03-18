import os
import sys
import pandas as pd
import collections

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData
from variant_processing import VariantProcessor

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

def get_raw_files():
    r = RawData()
    df = r.drug_labels
    return df

# The Drug Label information contains information of whether a drug is recommended for testing
# It means, it will be associated with level 1A (if prescribing info) or 1B (if not prescribing info) according to PharmGKB
# The evidence level (1A or 1B) needs to be added as it is assumed, but not explicit in a column
# If more than one agency has information for a drug, we will take the one with prescribing info

label_mapping = {
    "Testing required": 1,
    "Testing recommended": 2,
    "Actionable PGx": 3,
    "Informative PGx": 4
}
prescribing_mapping = {"Prescribing Info": 1, "Other": -1}
dosing_mapping = {"Dosing Info": 1, "Other": -1}


def str_to_int(df):
    df['Testing Level'] = df['Testing Level'].map(label_mapping)
    df['Has Dosing Info'] = df['Has Dosing Info'].map(dosing_mapping)
    df['Has Prescribing Info'] = df['Has Prescribing Info'].map(prescribing_mapping)
    return df

def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        drug_label = c.stringify(r[4])
        prescribing = c.stringify(r[5])
        dosing = c.stringify(r[6])
        chemical = c.stringify(r[10])
        gene = c.inline_semicolon_splitter_space(r[11])
        var_hap = c.stringify(r[12])
        if gene is not None:  # if gene is none, do not keep record
            for g in gene:
                r_ = [
                    drug_label,
                    prescribing,
                    dosing,
                    chemical,
                    g,
                    var_hap,
                ]
                R += [r_]
    cols = [
        "drug_label",
        "prescribing_guideline",
        "dosing_guideline",
        "chemical",
        "gene",
        "hap_var",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data

def deconv_chemical(df): 
    c = CsvCleaner()
    R = []
    for r in df.values:
        drug_label = r[0]
        prescribing = r[1]
        dosing = r[2]
        chemical = c.inline_semicolon_splitter_space(r[3])
        gene = r[4]
        hap_var = r[5]
        if chemical is not None: #if chemical is None, do not keep record
            for ch in chemical:
                r_ = [drug_label, prescribing, dosing, ch, gene, hap_var]
                R += [r_]
    cols = [
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
    p = VariantProcessor()
    all_vars = p.all_vars
    all_haps = p.all_haps
    variants = all_vars["variant"].tolist()
    haplotypes = all_haps["haplotype"].tolist()
    R = []
    for r in df.values:
        drug_label = r[0]
        prescribing = r[1]
        dosing = r[2]
        chemical = r[3]
        gene = r[4]
        var_hap = c.inline_semicolon_splitter_space(r[5])
        common_r = [drug_label,prescribing,dosing,chemical,gene,None,None]
        if var_hap is not None:
            for vh in var_hap:
                vh = p.clean_haps(vh)
                r_ = common_r[:]
                if vh in variants:
                    idx = [i for i, x in enumerate(variants) if x == vh] #make sure we get all variants, even those associated to more than one gene
                    gene_ = [all_vars.loc[i, "gene"] for i in idx]
                    if gene in gene_:
                        r_[5] = vh
                elif vh in haplotypes:
                    i = haplotypes.index(vh)
                    gene_ = all_haps.loc[i, "gene"]
                    if gene == gene_:
                        r_[6] = vh
                R += [r_]
        else:
            R += [common_r]
    cols = [
        "drug_label",
        "prescribing_guideline",
        "dosing_guideline",
        "chemical",
        "gene",
        "variant",
        "haplotype",
    ]
    data = pd.DataFrame(R, columns=cols)
    data.drop_duplicates(keep = "first", inplace=True)
    #we will not keep the dosing or prescribing information, only add evidence level of 1A or 1B
    data = data[["chemical","gene","variant","haplotype"]]
    d = collections.defaultdict(list)
    for r in data.values:
        k = tuple(r[:-2])
        v = tuple(r[-2:])
        d[k] += [v]
    d_ = {}
    for k, v in d.items():
        if len(v) > 1:
            all_none = all(x[0] is None and x[1] is None for x in v)
            if all_none:
                v_ = [(None, None)]
            else:
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

def add_genes_to_vars(df):
    p = VariantProcessor()
    gene_vid_dict = p.gene_vid_pairs()
    R = []
    for i, row in df.iterrows():
        chemical = row['chemical']
        gene = row['gene']
        var = row['variant']
        vid = row['vid']
        if gene is not None:
            if (gene, vid) not in gene_vid_dict:
                vid = None
                var = None
        R += [[chemical, gene, var, vid]]
    cols = ["chemical","gene", "variant", "vid"]
    data = pd.DataFrame(R, columns=cols)
    return data


def add_evidence(df):
    evidence_values = []
    for variant in df["variant"]:
        if pd.isna(variant) or variant == "":
            evidence_values.append("1B")
        else:
            evidence_values.append("1A")
    df["evidence"] = evidence_values
    return df

if __name__ == "__main__":
    p = VariantProcessor()
    df = get_raw_files()
    print(df.shape)
    df = str_to_int(df)
    df = deconv_gene(df)
    print(df.shape)
    df = deconv_chemical(df)
    print(df.shape)
    df = deconv_hap_variant(df)
    print(df.shape)
    df = p.hap_to_var(df)
    print(df.shape)
    df = p.clean_dup_haps(df)
    print(df.shape)
    df = add_genes_to_vars(df)
    df = p.add_cid_gid(df)
    print(df.shape)
    df = add_evidence(df)
    print(df.shape)
    df.to_csv(os.path.join(processed_folder, "8_drug_labels.csv"), index=False)

