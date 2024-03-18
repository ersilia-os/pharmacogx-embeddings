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
    df = r.study_parameters
    return df


def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    df = df[["Study Parameters ID", "Variant Annotation ID", "Biogeographical Groups"]]
    df.rename(
        columns={
            "Study Parameters ID": "sid",
            "Variant Annotation ID": "vaid",
            "Biogeographical Groups": "biogroup",
        },
        inplace=True,
    )
    df.to_csv(os.path.join(processed_folder, "8_study_parameters.csv"), index=False)
    return df


if __name__ == "__main__":
    create_table()


def create_table_from_manual_curation():
    df = pd.read_csv(os.path.join(processed_folder, "study_parameters_bid.csv"))
    c = CsvCleaner()
    data_dict = {}
    R = []
    for r in df.values:
        sid = c.stringify(r[0])
        aid = c.stringify(r[1])
        bid = c.inline_comma_splitter(r[3])
        print(bid)
        for b in bid:
            r = [sid, aid, b]
            R += [r]
    cols = ["sid", "vaid", "bid"]
    data = pd.DataFrame(R, columns=cols)
    data.to_csv(os.path.join(processed_folder, "study_bio_group.csv"), index=False)
    return data
