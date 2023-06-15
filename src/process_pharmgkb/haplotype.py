import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

def create_hap_table():
    dfs = []
    haps_path = os.path.join(processed_folder, "haplotypes")
    for fn in os.listdir(haps_path):
        if fn != "manual_curation.csv":
            if fn.endswith(".csv"):
                file_path = os.path.join(haps_path, fn)
                df = pd.read_csv(file_path)
                dfs.append(df)
    all_dfs = pd.concat(dfs, ignore_index=True)
    return all_dfs

def add_haps_from_rlx(df):
    c = CsvCleaner()
    rlx = pd.read_csv(os.path.join(processed_folder, "haplotype_rlx.csv"))
    rlx["haplotype"] = rlx["haplotype"].apply(lambda hap: ':'.join(hap.split(':')[:2]) if hap.startswith('HLA-') else hap) #change hla for only two positions 
    rlx = rlx.replace("CYP2A6*1X2A", "CYP2A6*1x2") #cyp2a6*1x2A is only 1x2 in pharmgkb
    rlx = rlx[["hid", "haplotype", "gene"]].drop_duplicates(keep = "first")
    new_rows = rlx[~rlx["hid"].isin(df["hid"])]
    R = []
    for r in new_rows.values:
        rsID = None
        start = None
        protein = None
        nc = None
        ng = None
        gene = c.stringify(r[2])
        haplotype = c.stringify(r[1])
        haplotype_number = haplotype.replace(gene, "")
        hid = c.stringify(r[0])
        r_ = [haplotype_number, rsID, start, protein, nc, ng, gene, haplotype, hid]
        R += [r_]
    df = df.append(pd.DataFrame(R, columns=df.columns), ignore_index=True)
    return df

def add_gid(df):
    gene_df = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    mapping_dict = gene_df.set_index("gene")["gid"].to_dict()
    df["gid"] = df["gene"].map(mapping_dict)
    df = df[["hid", "haplotype", "haplotype_number", "gid", "gene", "rsID", "start", "protein", "NC", "NG"]]
    return df

if __name__ == "__main__":
    data = create_hap_table()
    data = add_haps_from_rlx(data)
    data = add_gid(data)
    data.to_csv(os.path.join(processed_folder, "haplotype.csv"), index=False)