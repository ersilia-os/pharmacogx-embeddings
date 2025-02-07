import os
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
pharmgkb_folder = os.path.join(data_folder, "pharmgkb")
processed_folder = os.path.join(data_folder, "pharmgkb_processed")

# Manually create Tables to build upon for the PGX Relationships

# Pharmacokinetic Phenotype
pk = ["Dosage", "Metabolism/PK", "Other"]
df = pd.DataFrame(pk, columns=["pk_phenotype"])
df.to_csv(os.path.join(processed_folder, "pk_phenotype.csv"), index=False)

# Pharmacodynamic Phenotype
pdyn = ["Efficacy", "Toxicity", "PD", "Other"]
df = pd.DataFrame(pdyn, columns=["pd_phenotype"])
df.to_csv(os.path.join(processed_folder, "pd_phenotype.csv"), index=False)

# Evidence
# Level 0 is from druglabel
ev = {
    "1A": "Clincal",
    "1B": "ClinicalAnnotation",
    "2A": "ClinicalAnnotation",
    "2B": "ClinicalAnnotation",
    "3": "ClinicalAnnotation",
    "4": "ClinicalAnnotation",
    "5": "var_drug_ann",
    "6": "autom_ann",
}
df = pd.DataFrame.from_dict(ev, orient="index")
df.reset_index(inplace=True)
df.rename(columns={"index": "evidence", 0: "source"}, inplace=True)
df.to_csv(os.path.join(processed_folder, "evidence.csv"), index=False)

# Biogeographical groups
bio = {
    "African American/Afro-Caribbean": "AAC",
    "American": "AME",
    "Central/South Asian": "SAS",
    "East Asian": "EAS",
    "European": "EUR",
    "Latino": "LAT",
    "Near Eastern": "NEA",
    "Oceanian": "OCE",
    "Sub-Saharan African": "SSA",
    "Multiple Groups": "MG",
    "Unknown": "UNK",
    "Custom": "CST",
}
df = pd.DataFrame.from_dict(bio, orient="index")
df.reset_index(inplace=True)
df.rename(columns={"index": "biogeographical_group", 0: "bid"}, inplace=True)
df.to_csv(os.path.join(processed_folder, "biogeographical_group.csv"), index=False)
