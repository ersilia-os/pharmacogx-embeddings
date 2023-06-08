import os
import sys
import pandas as pd
import requests


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))

from utils import CsvCleaner
from pharmgkb import RawData

data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")


def get_raw_files():
    r = RawData()
    df = r.chemicals
    return df


def create_table():
    c = CsvCleaner()
    df = get_raw_files()
    # obtain relevant fields from the chemicals.csv
    data_dict = {}
    for r in df.values:
        cid = c.stringify(r[0])
        chemical = c.stringify(r[1])
        chemical_type = c.stringify(r[5])
        smiles = c.stringify(r[7])
        if smiles is None:
            crossr = c.inline_comma_splitter(r[6])
            if crossr is not None:
                for i in crossr:
                    if len(crossr) == 1:
                        if "PubChem Compound" in i:
                            print(crossr)
                            cpd = (i.split(":")[-1])
                            data = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/CanonicalSMILES/TXT".format(cpd))
                            smiles = data.text.strip()
                            print(smiles)
                        else:
                            data = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/CanonicalSMILES/TXT".format(chemical))
                            try_smiles = data.text.strip()
                            if "Status" in try_smiles:
                                smiles = None
                            else:
                                smiles = try_smiles
                            print(smiles)
                    else:
                        if "PubChem Compound" in i:
                            print(crossr)
                            cpd = (i.split(":")[-1][:-1])
                            data = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/CanonicalSMILES/TXT".format(cpd))
                            smiles = data.text.strip()
                            print(smiles)
                        else:
                            data = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/CanonicalSMILES/TXT".format(chemical))
                            try_smiles = data.text.strip()
                            if "Status" in try_smiles:
                                smiles = None
                            else:
                                smiles = try_smiles
                            print(smiles)
        dosing_guideline = c.stringify(r[9])
        if dosing_guideline == "No":
            dosing_guideline = -1
        elif dosing_guideline == "Yes":
            dosing_guideline = 1
        else:
            dosing_guideline = 0
        drug_label = c.stringify(r[18])
        if drug_label == "Testing required":
            drug_label = 1
        elif drug_label == "Testing recommended":
            drug_label = 2
        elif drug_label == "Actionable PGx":
            drug_label = 3
        elif drug_label == "Informative PGx":
            drug_label = 4        
        else:
            drug_label = -1
        data_dict[cid] = [chemical, chemical_type, smiles, dosing_guideline, drug_label]
    data = pd.DataFrame.from_dict(data_dict, orient="index")
    data.reset_index(inplace=True)
    data.rename(
        columns={
            "index": "cid",
            0: "chemical",
            1: "chemical_type",
            2: "smiles",
            3: "dosing_guideline",
            4: "drug_label"
        },
        inplace=True,
    )
    data.to_csv(os.path.join(processed_folder, "chemical.csv"), index=False)


if __name__ == "__main__":
    create_table()
