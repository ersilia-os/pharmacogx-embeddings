import os
import sys
import pandas as pd


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData
from variant_processing import VariantProcessor

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    autom_ann = r.automated_annotations
    return autom_ann

def eliminate_no_genes(df):
    df = df[
        ~df["Gene Symbols"].isna()
    ]  # many automated annotations do not have an associated gene because they refer to viral or bacterial genes. These have been removed to avoid confusion
    return df

def deconv_genomic_var(df):
    c = CsvCleaner()
    p = VariantProcessor()
    R = []
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
            vid = None
            hap = c.stringify(r[4])
            hid = c.stringify(r[3])
        if hap is not None:
            hap = p.clean_haps(hap)
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
    data = data.drop_duplicates(keep="first")
    return data

# as variants will be associated to the wrong gene (for example, genes VKROC1 and PRSS53 associated with warfarin metabolism vairant rs7294)
# rs7294 is a VKROC1 variant, not a PRSS53. It is safer to start form variants/haplotypes and add the genes later

def deconv_gene(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        chemical = r[0]
        cid = r[1]
        gene = c.inline_comma_splitter(r[2])
        var = r[3]
        vid = r[4]
        for g in gene:
            r_ = [
                chemical,
                cid,
                g,
                var,
                vid,
            ]
            R += [r_]
    cols = ["chemical", "cid", "gene", "variant", "vid"]
    data = pd.DataFrame(R, columns=cols)
    data = data.drop_duplicates(keep="first")
    return data

def add_genes_to_vars(df):
    p = VariantProcessor()
    gene_vid_dict = p.gene_vid_pairs()
    R = []
    for i, row in df.iterrows():
        chemical = row['chemical']
        cid = row['cid']
        gene = row['gene']
        vid = row['vid']
        var = row['variant']
        if (gene, vid) not in gene_vid_dict:
            vid = None
            variant = None
        R += [[chemical, cid, gene, var, vid]]
    cols = ["chemical", "cid", "gene", "variant", "vid"]
    data = pd.DataFrame(R, columns=cols)
    return data

if __name__ == "__main__":
    #df = get_raw_files()
    filename = "autom_ann_test"
    df = pd.read_csv("{}.csv".format(filename))
    p = VariantProcessor()
    print(df.shape)
    df = eliminate_no_genes(df)
    print(df.shape)
    df = deconv_genomic_var(df)
    print(df.shape)
    df = p.hap_to_var(df)
    print(df.shape)
    df = p.eliminate_wt(df)
    print(df.shape)
    df = p.clean_dup_haps(df)
    print(df.shape)
    df = deconv_gene(df)
    print(df.shape)
    df = add_genes_to_vars(df)
    print(df.shape)
    df = p.add_cid_gid(df)
    print(df.shape)
    df.to_csv("{}_dec.csv".format(filename), index=False)
