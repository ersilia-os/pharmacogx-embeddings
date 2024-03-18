import os
import sys
import pandas as pd
import requests

root = os.path.abspath(os.path.dirname(__file__))

data_folder = os.path.abspath(os.path.join(root, "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

class VariantProcessor():
    def __init__(self):
        self.gene = self._read_csv(os.path.join(processed_folder, "0_gene.csv"))
        self.chem = self._read_csv(os.path.join(processed_folder, "0_chemical.csv"))
        self.disease = self._read_csv(os.path.join(processed_folder, "0_disease.csv"))
        self.all_haps = self._read_csv(os.path.join(processed_folder, "2_haplotype.csv"))
        self.hap2var = self._read_csv(os.path.join(processed_folder, "3_hid_vid_complete.csv"))
        self.all_vars = self._read_csv(os.path.join(processed_folder, "5_variant_complete.csv"))
        self.alleles = self._read_csv(os.path.join(processed_folder, "6_clinical_annotation_allele.csv"))

    def _read_csv(self, file_path):
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return None

    def clean_haps(self, var_hap):
        if var_hap.startswith("HLA-"):
            var_hap = ":".join(var_hap.split(":")[:2])
        if var_hap == "G6PD B (wildtype)":
            var_hap = "G6PD B (reference)"
        g6pd_list1 = [
            "G6PD Mediterranean",
            "Dallas",
            "Panama",
            "Sassari",
            "Cagliari",
            "Birmingham",
        ]
        if var_hap in g6pd_list1:
            var_hap = (
                "G6PD Mediterranean, Dallas, Panama, Sassari, Cagliari, Birmingham"
            )
        g6pd_list2 = ["G6PD Canton", "Taiwan-Hakka", "Gifu-like", "Agrigento-like"]
        if var_hap in g6pd_list2:
            var_hap = "G6PD Canton, Taiwan-Hakka, Gifu-like, Agrigento-like"
        return var_hap

    def gene_vid_pairs(self):
        gene_vid_dict = {}
        for index, row in self.all_vars.iterrows():
            gene = row['gene']
            vid = row['vid']
            if (gene, vid) not in gene_vid_dict:
                gene_vid_dict[(gene, vid)] = None
        return gene_vid_dict
    
    def get_gene_from_variant(self, var):
        var_dict = {}
        try:
            url = "https://api.pharmgkb.org/v1/data/variant/?symbol={}&view=max".format(
                var
            )
            response = requests.get(url)
            data = response.json()
            related_genes = [gene["symbol"] for gene in data["data"][0]["relatedGenes"]]
            if len(related_genes) > 0:
                var_dict[var] = related_genes
        except KeyError:
            print("No URL")
        return var_dict

    def _add_hids(self,df):
        hids = self.hap2var[["hid", "haplotype"]].drop_duplicates()
        data = pd.merge(df, hids, on = "haplotype", how="left")
        return data
    
    def _add_vids(self,df):
        vids = self.hap2var[["vid", "variant"]].drop_duplicates()
        data = pd.merge(df, vids, on = "variant", how="left")
        return data
    
    def _add_gids(self,df):
        gene = self.gene[["gene", "gid"]].drop_duplicates()
        data = pd.merge(df, gene, on="gene", how="left")
        return data

    def hap_to_var(self, df):
        if "hid" not in df.columns:
            df = self._add_hids(df)
        if "vid" not in df.columns:
            df = self._add_vids(df)
        h2v = self.hap2var[["hid", "haplotype", "vid", "variant"]].drop_duplicates()
        df_vid_only = df[df["hid"].isna()]
        df_hid_only = df[~df["hid"].isna()]
        df_hid_only = df_hid_only.drop(columns=["vid", "variant"])
        merged_df = pd.merge(df_hid_only, h2v, on=["haplotype", "hid"], how="left")
        data = pd.concat([df_vid_only, merged_df], axis=0)
        data = data.drop_duplicates(keep="first")
        return data

    def clean_dup_haps(self,df):
        df = df.drop(columns=["hid", "haplotype"])
        df = df.drop_duplicates(keep="first")
        return df

    def _add_gid_ensembl_id(self,df):
        gene = self.gene[["gene", "gid", "ensembl_id"]].drop_duplicates()
        data = pd.merge(df, gene, on="gene", how="left")
        return data

    def _add_cid_smiles(self, df):
        chem = self.chem[["chemical", "cid", "smiles"]].drop_duplicates()
        data = pd.merge(df, chem, on="chemical", how="left")
        return data

    def _add_smiles(self, df):
        chem = self.chem[["chemical", "smiles"]].drop_duplicates()
        data = pd.merge(df, chem, on="chemical", how="left")
        return data
    
    def _add_did(self,df):
        data = pd.merge(df, self.disease, on="disease", how="left")
        return data
    
    def add_gid_cid_did(self, df):
        df = self._add_gid_ensembl_id(df)
        df = self._add_cid_smiles(df)
        df = self._add_did(df)
        return df
    
    def add_cid_gid(self, df):
        df = self._add_gid_ensembl_id(df)
        df = self._add_cid_smiles(df)
        return df

    def eliminate_wt(self, df):
    #eliminates the WT allele as it is NOT a PGX association
        df_filtered = df[~df["haplotype"].str.contains("reference", case=False, na=False)]
        return df_filtered
    
    def eliminate_normal_function_allele(self, df):
        #eliminates the normal function alleles defined by CPIC
        alleles = self.alleles["haplotype"].tolist()
        print(alleles)
        df_filtered = df[~df["haplotype"].isin(alleles)]
        return df_filtered
    

