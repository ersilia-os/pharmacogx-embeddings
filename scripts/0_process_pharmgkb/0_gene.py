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
    df = r.genes
    return df


def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    data_dict = {}
    for r in df.values:
        gid = c.stringify(r[0])
        hgnc = c.stringify(r[2])
        ensembl = c.stringify(r[3])
        gene = c.stringify(r[5])
        vip = c.stringify(r[8])
        if vip == "No":
            vip = -1
        elif vip == "Yes":
            vip = 1
        else:
            vip = 0
        variant_annotation = c.stringify(r[9])
        if variant_annotation == "No":
            variant_annotation = -1
        elif variant_annotation == "Yes":
            variant_annotation = 1
        else:
            variant_annotation = 0
        dosing_guideline = c.stringify(r[11])
        if dosing_guideline == "No":
            dosing_guideline = -1
        elif dosing_guideline == "Yes":
            dosing_guideline = 1
        else:
            dosing_guideline = 0
        data_dict[gid] = [
            gene,
            hgnc,
            ensembl,
            vip,
            variant_annotation,
            dosing_guideline,
        ]
    data = pd.DataFrame.from_dict(data_dict, orient="index")
    data.reset_index(inplace=True)
    data.rename(
        columns={
            "index": "gid",
            0: "gene",
            1: "hgnc_id",
            2: "ensembl_id",
            3: "vip",
            4: "variant_annotation",
            5: "dosing_guideline",
        },
        inplace=True,
    )
    data.to_csv(os.path.join(processed_folder, "0_gene.csv"), index=False)


if __name__ == "__main__":
    create_table()
