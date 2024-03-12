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
    df = r.clinical_ann_alleles
    return df

def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    df2 = pd.read_csv(os.path.join(processed_folder, "6_clinical_annotation.csv"))
    R = []
    for r in df2.values:
        caid = r[0]
        vid = r[1]
        variant = r[2]
        hid = r[3]
        haplotype = r[4]
        gene = r[5]
        evidence = r[6]
        score = r[7]
        phenotype = r[8]
        chemical = r[9]
        disease = r[10]
        for r_ in df.values:
            caid_ = r_[0]
            allele = c.stringify(r_[1])
            anntext = r_[2]
            function = r_[3]
            if caid == caid_:
                if allele is not None:
                    nr = [
                        caid,
                        vid,
                        variant,
                        hid,
                        haplotype,
                        gene,
                        evidence,
                        score,
                        phenotype,
                        chemical,
                        disease,
                        allele,
                        anntext,
                        function,
                    ]
                    R += [nr]
            else:
                continue

    cols = [
        "caid",
        "vid",
        "variant",
        "hid",
        "haplotype",
        "gene",
        "evidence",
        "score",
        "phenotype",
        "chemical",
        "disease",
        "allele",
        "anntext",
        "function",
    ]
    data = pd.DataFrame(R, columns=cols)
    return data


if __name__ == "__main__":
    df = create_table()
    df = df.drop_duplicates(keep="first")
    df.to_csv(
        os.path.join(processed_folder, "clinical_annotation_allele.csv"), index=False
    )
