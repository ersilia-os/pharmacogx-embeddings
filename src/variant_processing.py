import os
import sys
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))

data_folder = os.path.abspath(os.path.join(root, "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

class VariantProcessor():
    def __init__(self):
        self.all_vars = pd.read_csv(os.path.join(processed_folder, "5_variant_complete.csv"))
        self.all_haps = pd.read_csv(os.path.join(processed_folder, "2_haplotype.csv"))
        self.hap2var = pd.read_csv(os.path.join(processed_folder, "3_hid_vid_complete.csv"))
        self.gene = pd.read_csv(os.path.join(processed_folder, "0_gene.csv"))
        self.chem = pd.read_csv(os.path.join(processed_folder, "0_chemical.csv"))
        self.disease = pd.read_csv(os.path.join(processed_folder, "0_disease.csv"))

    def clean_haps(self, var_hap):
        if var_hap is not None:
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
        else:
            var_hap = None
        return var_hap

    def _add_hids(self,df):
        hids = self.hap2var[["hid", "haplotype"]]
        data = pd.merge(df, hids, on = "haplotype", how="left")
        return data
    
    def _add_vids(self,df):
        vids = self.hap2var[["vid", "variant"]]
        data = pd.merge(df, vids, on = "variant", how="left")
        return data

    def _hap_to_var(self, df):
        if "hid" not in df.columns:
            df = self._add_hids(df)
        if "vid" not in df.columns:
            df = self._add_vids(df)
        h2v = self.hap2var[["hid", "haplotype", "vid", "variant"]]
        df_vid_only = df[df["hid"].isna()]
        df_hid_only = df[~df["hid"].isna()]
        df_hid_only = df_hid_only.drop(columns=["vid", "variant"])
        merged_df = pd.merge(df_hid_only, h2v, on=["haplotype", "hid"], how="left")
        data = pd.concat([df_vid_only, merged_df], axis=0)
        data = data.drop_duplicates(keep="first")
        return data

    def _add_gid_ensembl_id(self,df):
        gene = self.gene[["gene", "gid", "ensembl_id"]]
        data = pd.merge(df, gene, on="gene", how="left")
        return data

    def _add_cid_smiles(self, df):
        chem = self.chem[["chemical", "cid", "smiles"]]
        data = pd.merge(df, chem, on="chemical", how="left")
        return data

    def _add_did(self,df):
        data = pd.merge(df, self.disease, on="disease", how="left")
        return data

    def _clean_haps(self,df):
        df = df.drop(columns=["hid", "haplotype"])
        df = df.drop_duplicates(keep="first")
        return df
    
    def add_columns(self, df):
        df = self._hap_to_var(df)
        df = self._add_gid_ensembl_id(df)
        df = self._add_cid_smiles(df)
        df = self._add_did(df)
        df = self._clean_haps(df)
        return df

    def add_columns_no_did(self, df):
        df = self._hap_to_var(df)
        df = self._add_gid_ensembl_id(df)
        df = self._add_cid_smiles(df)
        df = self._clean_haps(df)
        return df