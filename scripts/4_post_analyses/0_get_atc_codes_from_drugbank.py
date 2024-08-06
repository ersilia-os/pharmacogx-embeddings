import os
import pandas as pd
import xml.etree.ElementTree as ET

def extract_atc_codes(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define namespaces based on the XML schema
    namespaces = {
        'db': 'http://www.drugbank.ca'
    }

    # Initialize dictionary to store DrugBank IDs and ATC codes
    drug_atc_dict = {}

    # Iterate through each drug entry
    for drug in root.findall('db:drug', namespaces):
        # Extract the primary DrugBank ID
        drugbank_id_elem = drug.find('db:drugbank-id[@primary="true"]', namespaces)
        if drugbank_id_elem is not None:
            drugbank_id = drugbank_id_elem.text

            # Extract ATC codes
            atc_codes = []
            for atc_code in drug.findall('db:atc-codes/db:atc-code', namespaces):
                # Retrieve the 'code' attribute from each atc-code element
                atc_code_value = atc_code.attrib.get('code', '')
                atc_codes.append(atc_code_value)

            # Store in dictionary
            drug_atc_dict[drugbank_id] = atc_codes

    return drug_atc_dict

root = os.path.dirname(os.path.abspath(__file__))
xml_file_path = os.path.join(root, "..", "..", "data", "drugbank", "full_database.xml")
drug_atc_dict = extract_atc_codes(xml_file_path)

drug2atc = {}
for drug_id, atc_codes in drug_atc_dict.items():
    if len(atc_codes) > 0:
        drug2atc[drug_id] = atc_codes

df = pd.read_csv(os.path.join(root, "..", "..", "data", "drugbank", "pharmgkb_ids.csv"))

R = []
for r in df.values:
    dbid = r[0]
    pgkbid = r[1]
    if dbid in drug2atc:
        atcs = sorted(drug2atc[dbid])
        is_infectious = 0
        is_noncommunicable = 0
        for atc in atcs:
            if atc[0] == "J" or atc[0] == "P":
                is_infectious = 1
            else:
                is_noncommunicable = 1
        atcs = ";".join(sorted(drug2atc[dbid]))
        R.append([dbid, pgkbid, atcs, is_infectious, is_noncommunicable])
df = pd.DataFrame(R, columns=["drugbank_id", "pharmgkb_id", "atc_codes", "is_infectious", "is_noncommunicable"])

df.to_csv(os.path.join(root, "..", "..", "data", "drugbank", "drugbank_atc_codes.csv"), index=False)