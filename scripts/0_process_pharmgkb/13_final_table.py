import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

df1 = pd.read_csv(os.path.join(processed_folder, "6_clinical_annotation.csv"))
df2 = pd.read_csv(os.path.join(processed_folder, "7_clinical_variant.csv"), low_memory=False)
df3 = pd.read_csv(os.path.join(processed_folder, "9_var_pheno_ann.csv"))
df4 = pd.read_csv(os.path.join(processed_folder, "10_var_drug_ann.csv"))
df5 = pd.read_csv(os.path.join(processed_folder, "11_drug_labels.csv"))
df6 = pd.read_csv(os.path.join(processed_folder, "12_autom_ann.csv"))

def add_empty_cols(data):
    # List of columns to ensure
    cols= [
        "cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "significance", "phenotype", 
        "did", "disease", "biogroup", "caid", "vaid"
    ]
    # Add missing columns with empty values
    for col in cols:
        if col not in data.columns:
            data[col] = pd.Series(dtype='object')
    # Reorder columns
    data = data.reindex(columns=cols)
    return data


df1 = add_empty_cols(df1)
df2 = add_empty_cols(df2)
df3 = add_empty_cols(df3)
df4 = add_empty_cols(df4)
df5 = add_empty_cols(df5)
df6 = add_empty_cols(df6)

data = pd.concat([df1, df2, df3, df4, df5, df6])
print(data.shape)
data = data.drop_duplicates(keep="first")
print(data.shape)
data.to_csv(os.path.join(processed_folder, "14_pgkb_merged.csv"), index=False)