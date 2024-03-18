import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

from utils import CsvCleaner
from pharmgkb import RawData
from variant_processing import VariantProcessor

def get_raw_files():
    r = RawData()
    df = r.relationships
    return df

def parse_rlx():
    df = get_raw_files()
    df = df[df["Entity1_type"]=="Variant"]
    df = df[["Entity1_id", "Entity1_name"]]
    df.drop_duplicates(inplace=True)
    df.rename(columns={"Entity1_id": "vid", "Entity1_name": "variant"}, inplace=True)
    return df

def add_genes(df):
    c = CsvCleaner()
    p = VariantProcessor()
    R = []
    for r in df.values:
        vid = c.stringify(r[0])
        variant = c.stringify(r[1])
        var_dict = p.get_gene_from_variant(variant)
        if len(var_dict.keys()) > 0:
            for i in var_dict.values():
                for i_ in i:
                    r = [vid, variant, i_]
                    R += [r]
        else:
            r = [vid, variant, None]
            R += [r]
    cols = ["vid", "variant", "gene"]
    data = pd.DataFrame(R, columns=cols)
    return data

def parse_h2v():
    df = pd.read_csv(os.path.join(processed_folder, "3_hid_vid_complete.csv"))
    df = df.drop_duplicates(subset=["vid"], keep="first")
    df = df[["variant","vid", "gene", "gid"]]
    return df

if __name__ == "__main__":
    p = VariantProcessor()
    df1 = pd.read_csv(os.path.join(processed_folder, "4_variant.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "4_orphan_variant.csv"))
    df3 = parse_h2v()
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df4 = parse_rlx()
    merged = df4.merge(df[['vid', 'variant']], on=['vid', 'variant'], how='left', indicator=True)
    df4_ = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    df4_ = add_genes(df4_)
    df4_ = p._add_gids(df4_)
    df = pd.concat([df, df4_], ignore_index=True)
    df = df.drop_duplicates(keep="first")
    print(len(set(df["vid"])))
    print(df.shape)
    df.to_csv(os.path.join(processed_folder, "5_variant_complete.csv"), index=False)