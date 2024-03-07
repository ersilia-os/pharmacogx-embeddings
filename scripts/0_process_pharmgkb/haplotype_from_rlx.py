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
    df = r.relationships
    return df


# simply create a list of haplotypes with its hid and gid to which they belong
def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    df1 = df[df["Entity1_type"] == "Haplotype"]
    df1.drop_duplicates(subset=["Entity1_name"], keep="first", inplace=True)
    df1 = df1[["Entity1_id", "Entity1_name"]]
    df1.rename(columns={"Entity1_id": "hid", "Entity1_name": "haplotype"}, inplace=True)
    gene = []
    for h in df1["haplotype"]:
        if " " in h:
            g = h.split(" ")[0]
        elif "*" in h:
            g = h.split("*")[0]
        else:
            g = h
        gene += [g]
    df1["gene"] = gene
    gid_list = []
    genes = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    gene_names = genes["gene"].tolist()
    for r in df1.values:
        for i, gn in enumerate(gene_names):
            if r[2] == gn:
                gid = genes["gid"].loc[i]
                gid_list += [gid]
    df1["gid"] = gid_list
    df1.to_csv(os.path.join(processed_folder, "haplotype_rlx.csv"), index=False)
    return df1


if __name__ == "__main__":
    create_table()
