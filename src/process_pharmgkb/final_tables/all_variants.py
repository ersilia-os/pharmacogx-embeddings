import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

data_folder = os.path.abspath(os.path.join(root, "..","..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
final_folder = os.path.join(data_folder, "pharmgkb_processed", "final_tables")

if __name__ == "__main__":
    df1 = pd.read_csv(os.path.join(processed_folder, "variant.csv"))
    df2 = pd.read_csv(os.path.join(processed_folder, "hid_vid_complete.csv"))
    df2 = df2[["variant", "vid", "gene", "gid"]]
    df = pd.concat([df1, df2], ignore_index=True)
    print(df.shape)
    df = df.drop_duplicates(keep="first")
    print(df.shape)
    df.to_csv(os.path.join(final_folder, "all_variants.csv"), index=False)


