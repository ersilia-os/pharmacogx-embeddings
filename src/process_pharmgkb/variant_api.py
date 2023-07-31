import os
import sys
import requests
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

def get_json(df):
    vids = list(set(df["vid"].tolist()))
    vids_dict = {}
    for i,vid in enumerate(vids):
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
                chr = locations[0]["sequence"]["name"]
                vids_dict[vid] = [assembly, begin, end, intronic_offset, ref_allele, ref_hgvs, chr]
            except:
                assembly = locations[1]["assembly"]
                begin = locations[1]["begin"]
                end = locations[1]["end"]
                intronic_offset = locations[1]["intronicOffset"]
                ref_allele = locations[1]["referenceAllele"]
                ref_hgvs = locations[1]["referenceHgvs"]
                chr = locations[1]["sequence"]["name"]
                vids_dict[vid] = [assembly, begin, end, intronic_offset, ref_allele, ref_hgvs, chr]
        except:
            print(vid)
    return vids_dict


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(processed_folder, "variant_complete.csv"))
    vids_dict = get_json(df)
    print(vids_dict)
    df_ = pd.DataFrame.from_dict(vids_dict, orient='index', columns=['assembly', 'begin', 'end', 'intronic_offset', 'ref_allele', 'ref_hgvs', 'chr'])
    df_.reset_index(inplace=True)
    df_.rename(columns={'index': 'vid'}, inplace=True)
    merged_df = pd.merge(df, df_, on='vid', how='left')
    merged_df.to_csv(os.path.join(processed_folder, "variant_assembly.csv"), index=False)