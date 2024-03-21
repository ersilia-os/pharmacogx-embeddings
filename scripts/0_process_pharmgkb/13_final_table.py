import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

df1 = pd.read_csv(os.path.join(processed_folder, "6_clinical_annotation.csv"))
df2 = pd.read_csv(os.path.join(processed_folder, "7_clinical_variant.csv"), low_memory=False)
df3 = pd.read_csv(os.path.join(processed_folder, "8_drug_labels.csv"))
df4 = pd.read_csv(os.path.join(processed_folder, "9_var_drug_ann.csv"))
df5 = pd.read_csv(os.path.join(processed_folder, "10_var_pheno_ann.csv"))
df6 = pd.read_csv(os.path.join(processed_folder, "11_autom_ann.csv"))

cols = ["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]

# the clinical files are the most complete ones, we keep all the columns except score and ID
df1 = df1[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]
df2 = df2[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]

# drug labels is not associated to a phenotype or a disease
df3["phenotype"] = None
df3["disease"] =  None
df3["did"] = None
df3 = df3[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]

# var - drug and var - pheno annotations have a significance instead of evidence field
# keep only significant associations and add evidence level 5 to distinguish
df4 = df4[df4["significance"]==1]
df4["evidence"] = "5"
df4["disease"] = None
df4["did"] = None
df4 = df4[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]

df5 = df5[df5["significance"]==1]
df5["evidence"] = "5"
df5["disease"] = None
df5["did"] = None
df5 = df5[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]

# automated annotations is the less complete
df6["evidence"] = "6"
df6["phenotype"] = None
df6["did"] = None
df6["disease"] = None
df6 = df6[["cid", "chemical", "smiles", "gid", "gene", "ensembl_id", 
        "vid", "variant", "evidence", "phenotype", "did", "disease"]]

data = pd.concat([df1, df2, df3, df4, df5, df6])
print(data.shape)
data = data.drop_duplicates(keep="first")
print(data.shape)
data = data[~data["cid"].isna()]
data.to_csv(os.path.join(processed_folder, "13_pgkb_merged.csv"), index=False)