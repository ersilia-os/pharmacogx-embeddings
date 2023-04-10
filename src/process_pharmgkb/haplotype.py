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


# we want the gid - haplotype - hid relationships
def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    R = []
    for r in df.values:
        e1_type = c.stringify(r[2])
        if e1_type == "Gene":
            gid = c.stringify(r[0])
            e2_type = c.stringify(r[5])
            if e2_type == "Haplotype":
                hid = c.stringify(r[3])
                haplotype = c.stringify(r[4])
            else:
                continue
        elif e1_type == "Haplotype":
            hid = c.stringify(r[0])
            haplotype = str(r[1])
            e2_type = c.stringify(r[5])
            if e2_type == "Gene":
                gid = c.stringify(r[3])
            else:
                continue
        else:
            continue

        r = [hid, haplotype, gid]
        R += [r]
    cols = ["hid", "haplotype", "gid"]
    data = pd.DataFrame(R, columns=cols)
    print(data.shape)
    data.drop_duplicates(keep="first", inplace=True)
    print(data.shape)
    data.to_csv(os.path.join(processed_folder, "haplotype.csv"), index=False)
    return data


if __name__ == "__main__":
    create_table()
