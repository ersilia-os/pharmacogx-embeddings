import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", ".."))

data_folder = os.path.abspath(os.path.join(root, "..","..","..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
final_folder = os.path.join(data_folder, "pharmgkb_processed", "final_tables")

df1 = pd.read_csv(os.path.join(final_folder, "clinical_annotation.csv"))
df2 = pd.read_csv(os.path.join(final_folder, "clinical_variant.csv"), low_memory=False)
df3 = pd.read_csv(os.path.join(final_folder, "var_drug_ann.csv"))
df4 = pd.read_csv(os.path.join(final_folder, "var_pheno_ann.csv"))
df5 = pd.read_csv(os.path.join(final_folder, "autom_ann.csv"))

data = pd.concat([df1, df2, df3, df4, df5])

print(data.shape)
data = data.drop_duplicates(keep="first")
print(data.shape)
data.to_csv(os.path.join(final_folder, "pgkb_merged.csv"), index=False)