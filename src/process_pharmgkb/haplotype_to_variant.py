import os
import sys
import pandas as pd
import numpy as np
import requests

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def print_hids(df):
    df = df[~df["gene"].str.contains("HLA")]
    hids = df["hid"].tolist()
    hids = list(set(hids))
    for i, hid in enumerate(hids):
        if pd.notna(hid):
            continue
        else:
            print(type(hid))
            print("None")


def get_variants(df):
    df = df[~df["gene"].str.contains("HLA")]
    hids = df["hid"].tolist()
    hids = list(set(hids))
    R = []
    for i, hid in enumerate(hids):
        if pd.notna(hid):
            print(i, hid)
            try:
                url = "https://api.pharmgkb.org/v1/data/haplotype/{}".format(hid)
                response = requests.get(url)
                data = response.json()
                alleles = data["data"]["alleles"]
                for allele in alleles:
                    variant = allele["location"]["variant"]
                    vid = variant["id"]
                    var = variant["name"]
                    r_ = [hid, vid, var]
                    R += [r_]
                    print(r_)
            except KeyError:
                print("NOT " + str(hid))
    cols = ["hid", "vid", "variant"]
    data = pd.DataFrame(R, columns=cols)
    return data


def check_hids():
    df1 = pd.read_csv(os.path.join(processed_folder, "hid_to_vid.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    # Count the occurrences of hid in df1
    hid_counts_df1 = df1["hid"].value_counts()
    # Count the occurrences of hid in df2
    hid_counts_df2 = df2["hid"].value_counts()
    for hid in hid_counts_df1:
        print(hid)


def hap_to_var(df):
    df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    df2["variant"] = df2.apply(
        lambda row: row["rsID"]
        if pd.notnull(row["rsID"])
        else str(row["gene"] + " " + row["start"])
        if pd.notnull(row["start"])
        else None,
        axis=1,
    )
    R = []
    for r in df2.values:
        hid = r[0]
        haplotype = r[1]
        haplotype_number = r[2]
        gid = r[3]
        gene = r[4]
        rsID = r[5]
        start = r[6]
        protein = r[7]
        nc = r[8]
        ng = r[9]
        var = r[10]
        for r_ in df.values:
            hid_ = r_[0]
            vid = r_[1]
            var_ = r_[2]
            if var == var_:
                r = [
                    hid,
                    haplotype,
                    haplotype_number,
                    gid,
                    gene,
                    rsID,
                    start,
                    protein,
                    nc,
                    ng,
                    var,
                    vid,
                ]
                R += [r]
    cols = [
        "hid",
        "haplotype",
        "haplotype_number",
        "gid",
        "gene",
        "rsID",
        "start",
        "protein",
        "nc",
        "ng",
        "variant",
        "vid",
    ]
    data = pd.DataFrame(R, columns=cols)
    data.drop_duplicates(keep="first", inplace=True)
    return data


def add_vars(df):
    df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    df2["variant"] = df2.apply(
        lambda row: row["rsID"].strip()
        if pd.notnull(row["rsID"])
        else row["NC"].strip()
        if pd.notnull(row["NC"])
        else str(row["gene"] + " " + row["start"]).strip()
        if pd.notnull(row["gene"]) and pd.notnull(row["start"])
        else None,
        axis=1,
    )
    df2["variant"] = df2["variant"].apply(
        lambda var: var.rstrip("*") if pd.notnull(var) else var
    )
    df2.loc[df2["variant"] == "NAT2 Δ859", "variant"] = "NAT2 859Del"
    vid_mapping = (
        df.groupby("variant")["vid"].first().reset_index()
    )  # get unique vid-variant
    df2 = df2.merge(vid_mapping, on="variant", how="left")
    df2["vid"] = df2["vid"].fillna("")
    df2 = df2.replace("", None)
    return df2


def deconv_doubles(df):
    R = []
    for r in df.values:
        hid = r[0]
        hap = r[1]
        hap_num = r[2]
        gid = r[3]
        gene = r[4]
        rsid = r[5]
        start = r[6]
        protein = r[7]
        nc = r[8]
        ng = r[9]
        var = r[10]
        vid = r[11]
        if (vid == None) & ("HLA" not in gene):
            if ";" in str(start):
                st_split = [s.strip() for s in start.split(";")]
                nc_split = [s.strip() for s in nc.split(";")]
                if pd.notnull(protein):
                    protein_split = [s.strip() for s in protein.split(";")]
                    ng_split = [s.strip() for s in ng.split(";")]
                    for i, s in enumerate(st_split):
                        start = st_split[i]
                        nc = nc_split[i]
                        protein = protein_split[i]
                        ng = ng_split[i]
                        r_ = [
                            hid,
                            hap,
                            hap_num,
                            gid,
                            gene,
                            rsid,
                            start,
                            protein,
                            nc,
                            ng,
                            var,
                            vid,
                        ]
                        R += [r_]
                else:
                    for i, s in enumerate(st_split):
                        start = st_split[i]
                        nc = nc_split[i]
                        r_ = [
                            hid,
                            hap,
                            hap_num,
                            gid,
                            gene,
                            rsid,
                            start,
                            protein,
                            nc,
                            ng,
                            var,
                            vid,
                        ]
                        R += [r_]
            else:
                r_ = [
                    hid,
                    hap,
                    hap_num,
                    gid,
                    gene,
                    rsid,
                    start,
                    protein,
                    nc,
                    ng,
                    var,
                    vid,
                ]
                R += [r_]
        else:
            r_ = [hid, hap, hap_num, gid, gene, rsid, start, protein, nc, ng, var, vid]
            R += [r_]
    cols = []
    cols = [
        "hid",
        "haplotype",
        "haplotype_number",
        "gid",
        "gene",
        "rsID",
        "start",
        "protein",
        "nc",
        "ng",
        "variant",
        "vid",
    ]
    data = pd.DataFrame(R, columns=cols)
    data.drop(columns=["vid"], inplace=True)
    df2 = pd.read_csv(os.path.join(processed_folder, "hid_to_vid.csv"))
    vid_mapping = (
        df2.groupby("variant")["vid"].first().reset_index()
    )  # get unique vid-variant
    data = data.merge(vid_mapping, on="variant", how="left")
    data["vid"] = data["vid"].fillna("")
    data = data.replace("", None)
    return data


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
    print_hids(df)
    data = get_variants(df)
    data.to_csv(os.path.join(processed_folder, "hid_to_vid.csv"), index=False)
    check_hids()
    data = pd.read_csv(os.path.join(processed_folder, "hid_to_vid.csv"))
    data = add_vars(data)
    data = deconv_doubles(data)
    data.to_csv(os.path.join(processed_folder, "hid_vid_complete.csv"), index=False)
