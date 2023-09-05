import os
import sys
import pandas as pd
import numpy as np
import requests

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
haps_path = os.path.join(data_folder, "pharmgkb", "haplotypes")


def create_allele_definition_file(df):
    hap_dict = {}
    ch_position = df.iat[2, 0]
    if "NC_" in ch_position:
        ch = ch_position.split()[2]
    else:
        ch = None
    for i, r in enumerate(df.values):
        if i == 0:
            starts = r[1:]
        elif i == 1:
            proteins = r[1:]
        elif i == 2:
            ncs = r[1:]
        elif i == 3:
            ngs = r[1:]
        elif i == 4:
            rsids = r[1:]
    for i, r in enumerate(df.values):
        if i >= 6:
            hap = r[0]
            hap_dict[hap] = []
            for n, x in enumerate(r[1:]):
                if x is not np.nan:
                    rsid = rsids[n]
                    start = starts[n]
                    protein = proteins[n]
                    nc = ncs[n]
                    ng = ngs[n]
                    hap_dict[hap] += [[rsid, start, protein, nc, ng]]
    df_rows = []
    for key, value in hap_dict.items():
        if isinstance(value, list):
            for sublist in value:
                df_rows.append([key] + sublist)
        else:
            df_rows.append([key] + value)
    df1 = pd.DataFrame(df_rows)
    df1.columns = ["haplotype_number", "rsID", "start", "protein", "NC", "NG"]
    df1 = df1.replace(np.nan, None)
    df1 = df1.applymap(lambda x: x.rstrip() if isinstance(x, str) else x)
    if ch != None:
        df1["NC"] = df1["NC"].apply(lambda x: f"{ch}:{x}" if x else None)
    df1["gene"] = [g] * len(df1)
    df1["haplotype"] = df1.apply(
        lambda row: row["gene"] + str(row["haplotype_number"])
        if str(row["haplotype_number"]).startswith("*")
        else row["gene"] + " " + str(row["haplotype_number"]),
        axis=1,
    )
    return df1


def add_hid_from_url(df):
    haps = list(set(df["haplotype"].tolist()))
    haps_dict = {}
    haps_not = []
    for hap in haps:
        try:
            url = "https://api.pharmgkb.org/v1/data/haplotype/?symbol={}".format(hap)
            response = requests.get(url)
            data = response.json()
            first_item = data["data"][0]
            haps_dict[hap] = first_item["id"]
        except KeyError:
            print(hap)
            haps_not += [hap]
    df["hid"] = df["haplotype"].map(haps_dict)
    return df, haps_not


if __name__ == "__main__":
    filenames = os.listdir(haps_path)
    gene_list = []
    for filename in filenames:
        fn = str(filename)
        if filename != "nofile.csv":
            if fn[-3:] == "csv":
                gene = fn.split("_")[0]
                gene_list += [gene]
    gene_list = sorted(gene_list)
    haps_not_list = []
    for g in gene_list:
        print(g)
        data = pd.read_csv(
            os.path.join(haps_path, "{}_allele_definition_table.csv".format(g))
        )
        data = create_allele_definition_file(data)
        data, haps_not = add_hid_from_url(data)
        if gene == "GSTM1":  # Manually modify GSTM1 and GSTT1 files
            data = data.drop([1, 2])
            data = data.append(
                {
                    "haplotype_number": "null",
                    "rsID": np.nan,
                    "start": np.nan,
                    "protein": np.nan,
                    "NC": np.nan,
                    "NG": np.nan,
                    "gene": "GSTM1",
                    "haplotype": "GSTM1 null",
                    "hid": "PA166048675",
                },
                ignore_index=True,
            )
        elif gene == "GSTT1":
            data = data.drop([1, 2])
            data = data.append(
                {
                    "haplotype_number": "null",
                    "rsID": np.nan,
                    "start": np.nan,
                    "protein": np.nan,
                    "NC": np.nan,
                    "NG": np.nan,
                    "gene": "GSTM1",
                    "haplotype": "GSTT1 null",
                    "hid": "PA166048678",
                },
                ignore_index=True,
            )
        data.to_csv(
            os.path.join(processed_folder, "haplotypes", "{}_haplotypes.csv".format(g)),
            index=False,
        )
        haps_not_list += [haps_not]
    df = pd.DataFrame(haps_not_list, columns=["haplotype"])
    df.to_csv(
        os.path.join(processed_folder, "haplotypes", "manual_curation.csv"), index=False
    )  # manually check the haplotypes without url and add them
