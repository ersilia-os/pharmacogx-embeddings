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
    df = r.variants
    return df

def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    df = df[~df["Gene IDs"].isna()]
    R = []
    for r in df.values:
        vid = c.stringify(r[0])
        variant = c.stringify(r[1])
        gid = c.inline_comma_splitter(r[2])
        for g in gid:
            r = [vid,
                variant,
                g]
            R += [r]
    cols = ["vid", "variant", "gid"]
    data = pd.DataFrame(R, columns=cols)
    data.to_csv(os.path.join(processed_folder, "variant.csv"),index=False)
    return(data)

if __name__ == "__main__":
    data = create_table()

