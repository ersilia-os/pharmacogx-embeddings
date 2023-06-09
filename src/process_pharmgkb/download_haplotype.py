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
    else:
        print(f"No table found for gene: {gene_name}")

genes = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
gene_names = list(set(genes["gene"].tolist()))
print(len(gene_names))

for gn in gene_names:
    download_table(gn)