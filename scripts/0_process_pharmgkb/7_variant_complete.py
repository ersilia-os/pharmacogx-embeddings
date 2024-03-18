import os
import sys
import requests
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed_revision1")

from utils import CsvCleaner
from pharmgkb import RawData

def get_raw_files():
    r = RawData()
    df = r.relationships
    return df


def parse_h2v():
    df = pd.read_csv(os.path.join(processed_folder, "3_hid_vid_complete.csv"))
    df = df.drop_duplicates(subset=["vid"], keep="first")
    df = df[["variant","vid", "gene", "gid"]]
    return df


if __name__ == "__main__":
    df1 = pd.read_csv(os.path.join(processed_folder, "4_variant.csv"))
    print("Variants")
    print(df1.shape)
    print(len(set(df1["vid"])))
    df2 = pd.read_csv(os.path.join(processed_folder, "4_orphan_variant.csv"))
    print("Orphan")
    print(df2.shape)
    print(len(set(df2["vid"])))
    df3 = parse_h2v()
    print("HAP TO VAR")
    print(df3.shape)
    print(len(set(df3["vid"])))
    df = pd.concat([df1, df2, df3], ignore_index=True)
    print(df.shape)
    print(len(set(df["vid"])))
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    print(len(set(df["vid"])))
    df.to_csv(os.path.join(processed_folder, "5_variant_complete.csv"), index=False)