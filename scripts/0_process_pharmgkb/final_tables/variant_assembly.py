import os
import sys
import requests
import pandas as pd
from ast import literal_eval

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..","..", "src"))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "..", "data"))
data_folder = os.path.abspath(os.path.join(root, "..", "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
final_folder = os.path.join(data_folder, "pharmgkb_processed", "final_tables")


def get_json(df):
    vids = list(set(df["vid"].tolist()))
    vids_dict = {}
    for i, vid in enumerate(vids):
        print(i)
        try:
            url = "https://api.pharmgkb.org/v1/data/variant/{}?view=max".format(vid)
            response = requests.get(url)
            data = response.json()
            locations = data["data"]["locations"]
            try:
                assembly = locations[0]["assembly"]
                begin = locations[0]["begin"]
                end = locations[0]["end"]
                intronic_offset = locations[0]["intronicOffset"]
                ref_allele = locations[0]["referenceAllele"]
                ref_hgvs = locations[0]["referenceHgvs"]
                try:
                    var_allele = locations[0]["variantAlleles"]
                    var_hgvs = locations[0]["variantHgvs"]
                except:
                    var_allele = None
                    var_hgvs = None
                chr = locations[0]["sequence"]["name"]
                vids_dict[vid] = [
                    assembly,
                    begin,
                    end,
                    intronic_offset,
                    ref_allele,
                    ref_hgvs,
                    var_allele,
                    var_hgvs,
                    chr,
                ]
            except:
                print("option 2")
                assembly = locations[1]["assembly"]
                begin = locations[1]["begin"]
                end = locations[1]["end"]
                intronic_offset = locations[1]["intronicOffset"]
                ref_allele = locations[1]["referenceAllele"]
                try:
                    ref_hgvs = locations[1]["referenceHgvs"]
                except:
                    ref_hgvs = None
                try:
                    var_allele = locations[1]["variantAlleles"]
                    var_hgvs = locations[1]["variantHgvs"]
                except:
                    var_allele = None
                    var_hgvs = None
                chr = locations[1]["sequence"]["name"]
                vids_dict[vid] = [
                    assembly,
                    begin,
                    end,
                    intronic_offset,
                    ref_allele,
                    ref_hgvs,
                    var_allele,
                    var_hgvs,
                    chr,
                ]
        except:
            print(vid)
    return vids_dict


rename_dict = {
    "vid": "vid_",
    "variant": "variant_",
    "gene": "gene_",
    "gid": "gid_",
    "assembly": "assembly_",
    "begin": "begin_",
    "end": "end_",
    "intronic_offset": "intronic_offset_",
    "ref_allele": "ref_allele_",
    "ref_hgvs": "ref_hgvs_",
    "var_allele": "var_allele_",
    "chr": "chr_",
}

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(final_folder, "all_variants.csv"))
    vids_dict = get_json(df)
    df_ = pd.DataFrame.from_dict(
        vids_dict,
        orient="index",
        columns=[
            "assembly",
            "begin",
            "end",
            "intronic_offset",
            "ref_allele",
            "ref_hgvs",
            "var_allele",
            "var_hgvs",
            "chr",
        ],
    )
    df_.reset_index(inplace=True)
    df_.rename(columns={"index": "vid"}, inplace=True)
    merged_df = pd.merge(df, df_, on="vid", how="left")
    # convert the var allele and var hgvs to real lists
    merged_df["var_allele"] = merged_df["var_allele"].apply(
        lambda x: literal_eval(x) if isinstance(x, str) else x
    )
    merged_df["var_hgvs"] = merged_df["var_hgvs"].apply(
        lambda x: literal_eval(x) if isinstance(x, str) else x
    )

    exploded_df_A = (
        merged_df.explode("var_allele")
        .rename(columns=rename_dict)
        .reset_index(drop=True)
    )
    exploded_df_B = (
        merged_df.explode("var_hgvs")
        .rename(columns={"var_hgvs": "var_hgvs_"})
        .reset_index(drop=True)
    )
    result_df = pd.concat([exploded_df_A, exploded_df_B], axis=1)
    result_df = result_df[
        [
            "vid_",
            "variant_",
            "gene_",
            "gid_",
            "assembly_",
            "begin_",
            "end_",
            "intronic_offset_",
            "ref_allele_",
            "ref_hgvs_",
            "var_allele_",
            "var_hgvs_",
            "chr_",
        ]
    ]
    result_df.columns = [col.rstrip("_") for col in result_df.columns]
    result_df.to_csv(os.path.join(final_folder, "variant_assembly.csv"), index=False)
