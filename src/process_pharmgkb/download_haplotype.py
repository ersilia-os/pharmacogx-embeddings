import os
import pandas as pd
import requests

import sys
root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

def download_table(gene_name):
    url = f"https://api.pharmgkb.org/v1/download/file/attachment/{gene_name}_allele_definition_table.xlsx"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{gene_name}_allele_definition_table.xlsx"
        with open(os.path.join(data_folder, "pharmgkb", "haplotypes", filename), "wb") as file:
            file.write(response.content)
        # Convert Excel file to CSV
        df = pd.read_excel(os.path.join(data_folder, "pharmgkb", "haplotypes", filename), sheet_name="Alleles")
        csv_filename = f"{gene_name}_allele_definition_table.csv"
        df.to_csv(os.path.join(data_folder,"pharmgkb", "haplotypes", csv_filename), index=False)
        print(f"Table downloaded for gene: {gene_name}")
        return None
    else:
        print(f"No table found for gene: {gene_name}")
        return gene_name

#genes = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
#gene_names = list(set(genes["gene"].tolist()))
#print(len(gene_names))


df1 = pd.read_csv(os.path.join(processed_folder, "clinical_annotation.csv"))
df2 = pd.read_csv(os.path.join(processed_folder, "clinical_variant.csv"))
df3 = pd.read_csv(os.path.join(processed_folder, "var_drug_ann.csv"))
df4 = pd.read_csv(os.path.join(processed_folder, "var_pheno_ann.csv"))
df5 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
gene_names =list(set(df1["gene"].tolist()+df2["gene"].tolist()+df3["gene"].tolist()+df4["gene"].tolist()+df5["gene"].tolist()))


no_file=[]
for gn in gene_names:
    gene_name = download_table(gn)
    if gene_name is not None:
        no_file += [gene_name]
df = pd.DataFrame(no_file, columns=['gene'])
df.to_csv(os.path.join(data_folder, "pharmgkb", "haplotypes", "no_file.csv"), index=False)