import os
import sys
import pandas as pd
import numpy as np


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
haps_path = os.path.join(data_folder, "pharmgkb", "haplotypes")

# Get a list of filenames in the directory
filenames = os.listdir(haps_path)
gene_list = []
for filename in filenames:
    fn = str(filename)
    if fn[-3:]=="csv":
        gene = fn.split("_")[0]
        gene_list += [gene]

for g in gene_list:
    df = pd.read_csv(os.path.join(haps_path, "{}_allele_definition_table.csv".format(g)))
    hap_dict = {}
    for i,r in enumerate(df.values):
        if i == 0:
            starts = r[1:]
        elif i == 1: 
            proteins = r[1:]
        elif i == 2 :
            ncs = r[1:]
        elif i == 3:
            ngs = r[1:]
        elif i == 4:
            rsids = r[1:]


    for i,r in enumerate(df.values):
        if i >= 6:
            hap = r[0]
            hap_dict[hap] = []
            for n,x in enumerate(r[1:]):
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

    df_ = pd.DataFrame(df_rows)
    df_.columns = ["haplotype_number", "rsID", "start", "protein", "NC", "NG"]
    df_["gene"] = [g]*len(df_)
    df_["haplotype"] = df_["gene"]+df_["haplotype_number"]
    df_.to_csv(os.path.join(processed_folder, "haplotypes_gene", "{}_haplotypes.csv".format(g)), index=False)