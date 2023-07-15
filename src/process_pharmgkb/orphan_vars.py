import os
import sys
import requests
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def vaid_from_url(df):
    vars = df["variant"].tolist()
    var_dict = {}
    for var in vars:
        print(var)
        try:
            url = "https://api.pharmgkb.org/v1/data/variant/?name={}&view=max".format(
                var
            )
            response = requests.get(url)
            data = response.json()
            vid = data["data"][0]["id"]
            try:
                gene = data["data"][0]["relatedGenes"][0]["symbol"]
                gid = data["data"][0]["relatedGenes"][0]["id"]
            except:
                gene = None
                gid = None
            var_dict[var] = [vid, gene, gid]
        except:
            var_dict[var] = [None, None, None]
    for k, v in var_dict.items():
        if v[1] == None:
            if len(k.split(" ")) > 1:
                print(k)
                v[1] = k.split(" ")[0]
                url = "https://api.pharmgkb.org/v1/data/gene?symbol={}&view=min".format(
                    v[1]
                )
                response = requests.get(url)
                data = response.json()
                v[2] = data["data"][0]["id"]
    df = pd.DataFrame(var_dict).transpose().reset_index()
    df.columns = ["variant", "vid", "gene", "gid"]
    return df


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(processed_folder, "orphan_variant_list.csv"))
    df = vaid_from_url(df)
    df.to_csv(os.path.join(processed_folder, "orphan_variant.csv"), index=False)
