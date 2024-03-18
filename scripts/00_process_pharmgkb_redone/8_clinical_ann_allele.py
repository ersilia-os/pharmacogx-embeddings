import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import CsvCleaner
from pharmgkb import RawData
from variant_processing import VariantProcessor

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    df = r.clinical_ann_alleles
    return df

def get_normal_alleles(df):
    df = df[df["Allele Function"]== "Normal function"]
    haps = []
    for s in df["Annotation Text"].tolist():
        if "allele is assigned as a normal function allele by CPIC." in s:
            hap = s.split(" ")[1]
            haps += [hap]
    return haps

if __name__ == "__main__":    
    c = CsvCleaner()
    p = VariantProcessor()
    df = get_raw_files()
    haps = get_normal_alleles(df)
    haps = list(set(haps))
    df = pd.DataFrame({"haplotype": haps})
    df["gene"] = [x.split("*")[0] for x in df ["haplotype"].tolist()]
    df = p._add_hids(df)
    df = p._add_gids(df)
    df.to_csv(os.path.join(processed_folder, "6_clinical_annotation_allele.csv"), index=False)
