import os
import sys
import pandas as pd
import requests

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


def get_gene_from_variant(variant):
    var_dict = {}
    try:
        url = "https://api.pharmgkb.org/v1/data/variant/?symbol={}&view=max".format(
            variant
        )
        response = requests.get(url)
        data = response.json()
        print(response)
        related_genes = [gene["symbol"] for gene in data["data"][0]["relatedGenes"]]
        print(related_genes)
        if len(related_genes) > 0:
            var_dict[variant] = related_genes
    except KeyError:
        print("No URL")
    return var_dict


def add_genes(df):  # check that no variant is missing genes that should be there
    c = CsvCleaner()
    R = []
    for r in df.values:
        vid = c.stringify(r[0])
        variant = c.stringify(r[1])
        gene = c.stringify(r[2])
        print(variant,gene)
        if gene is None:
            print("trying to get gene")
            var_dict = get_gene_from_variant(variant)
            print(var_dict)
            if len(var_dict.keys()) > 0:
                for i in var_dict.values():
                    r = [vid, variant, i]
                    R += [r]
        else:
            r = [vid, variant, gene]
            R += [r]
    cols = ["vid", "variant", "gene"]
    data = pd.DataFrame(R, columns=cols)
    return data


def deconv_genes(df):
    c = CsvCleaner()
    R = []
    for r in df.values:
        vid = c.stringify(r[0])
        variant = c.stringify(r[1])
        gene = c.inline_comma_splitter(r[3])
        if gene is not None:
            for g in gene:
                r = [vid, variant, g]
                R += [r]
        else:
            r = [vid, variant, None]
            R += [r]
    cols = ["vid", "variant", "gene"]
    data = pd.DataFrame(R, columns=cols)
    return data


def add_gid(df):
    gene_df = pd.read_csv(os.path.join(processed_folder, "gene.csv"))
    mapping_dict = gene_df.set_index("gene")["gid"].to_dict()
    df["gid"] = df["gene"].map(mapping_dict)
    return df


if __name__ == "__main__":
    data = get_raw_files()
    data = deconv_genes(data)
    #data = add_genes(data) #all genes that could be there are there
    data = add_gid(data)
    data.to_csv(os.path.join(processed_folder, "variant.csv"), index=False)
