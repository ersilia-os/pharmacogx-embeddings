import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

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

def add_gid(df):
    gene_df = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    mapping_dict = gene_df.set_index("gene")["gid"].to_dict()
    df["gid"] = df["gene"].map(mapping_dict)
    return df

if __name__ == "__main__":
    data = create_hap_table()
    data = add_gid(data)
    data.to_csv(os.path.join(processed_folder, "haplotype.csv"), index=False)