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
    df = r.chemicals
    return df


def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    # eliminate rows without smiles
    df = df[~df["SMILES"].isna()]
    # obtain relevant fields from the chemicals.csv
    data_dict = {}
    for r in df.values:
        cid = c.stringify(r[0])
        chemical = c.stringify(r[1])
        chemical_type = c.stringify(r[5])
        smiles = c.stringify(r[7])
        dosing_guideline = c.stringify(r[9])
        if dosing_guideline == "No":
            dosing_guideline = -1
        elif dosing_guideline == "Yes":
            dosing_guideline = 1
        else:
            dosing_guideline = 0
        data_dict[cid] = [chemical, chemical_type, smiles, dosing_guideline]
    data = pd.DataFrame.from_dict(data_dict, orient="index")
    data.reset_index(inplace=True)
    data.rename(
        columns={
            "index": "cid",
            0: "chemical",
            1: "chemical_type",
            2: "smiles",
            3: "dosing_guideline",
        },
        inplace=True,
    )
    data.to_csv(os.path.join(processed_folder, "chemical.csv"), index=False)


if __name__ == "__main__":
    create_table()
