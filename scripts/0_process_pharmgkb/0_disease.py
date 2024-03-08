import os
import sys
import pandas as pd


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    df = r.phenotypes
    return df


def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    R = []
    for r in df.values:
        did = c.stringify(r[0])  # PharmGKB Accession Id
        disease = c.stringify(r[1])  # Name
        r = [did, disease]
        R += [r]
    cols = ["did", "disease"]
    data = pd.DataFrame(R, columns=cols)
    data.to_csv(os.path.join(processed_folder, "0_disease.csv"), index=False)
    return data


if __name__ == "__main__":
    create_table()
