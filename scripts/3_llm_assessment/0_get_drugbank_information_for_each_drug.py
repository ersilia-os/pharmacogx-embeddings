import os
import os
from lxml import etree
from tqdm import tqdm
import csv
import json
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(root, "..", "..", "data", "drugbank")

# Path to your XSD schema file
xsd_file = os.path.join(data_dir, 'drugbank.xsd')

# Path to your XML file
xml_file = os.path.join(data_dir, 'full_database.xml')


def extract_drugbank_smiles(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug SMILES data
    drug_smiles = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        
        # Find the calculated properties section and extract SMILES
        properties = drug.findall('db:calculated-properties/db:property', namespaces=ns)
        smiles = None
        for property in properties:
            if property.find('db:kind', namespaces=ns).text == "SMILES":
                smiles = property.find('db:value', namespaces=ns).text
                break  # Exit after finding the SMILES to avoid unnecessary processing

        # Organize data into a dictionary
        smiles_info = {
            'DrugBankId': drug_id.text if drug_id is not None else None,
            'Smiles': smiles
        }
        drug_smiles.append(smiles_info)

    return drug_smiles


def extract_pharmgkb_identifiers(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a dictionary to store PharmGKB identifiers keyed by DrugBank ID
    pharmgkb_ids = {}

    # Iterate over each drug entry
    for drug in tqdm(tree.xpath('//db:drug', namespaces=ns)):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        if drug_id is not None:
            drug_id_text = drug_id.text
            # Find all external identifiers
            external_identifiers = drug.findall('.//db:external-identifier', namespaces=ns)
            for identifier in external_identifiers:
                resource = identifier.find('db:resource', namespaces=ns)
                if resource is not None and resource.text == 'PharmGKB':
                    id_text = identifier.find('db:identifier', namespaces=ns)
                    if id_text is not None:
                        pharmgkb_ids[drug_id_text] = id_text.text
                        break  # Stop looking through more identifiers once PharmGKB is found

    return pharmgkb_ids

# Specify the path to your XML file
xml_file_path = xml_file

print("Extracting PharmGKB identifiers...")
pharmgkb_ids = extract_pharmgkb_identifiers(xml_file_path)

# Output the results
pharmgkb_ids_file = os.path.join(data_dir, 'pharmgkb_ids.csv')
with open(pharmgkb_ids_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["DrugBankId", "PharmGKBId"])
    for db_id, pharm_id in pharmgkb_ids.items():
        writer.writerow([db_id, pharm_id])

print("Extracting SMILES...")
drugbank_smiles = extract_drugbank_smiles(xml_file)

drugbank_smiles_file = os.path.join(data_dir, 'drugbank_smiles.csv')
with open(drugbank_smiles_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["DrugBankId", "Smiles"])
    for d in drugbank_smiles:
        if d["DrugBankId"] is None or d["Smiles"] is None:
            continue
        writer.writerow([d["DrugBankId"], d["Smiles"]])


print("Mapping DrugBank to any of our identifiers...")
print("...Print getting the identifiers of the drugs explored in this study...")
df = pd.read_csv(os.path.join(root, "..", "..", "data", "ml_datasets_pairs", "chemical_gene_pairs_prediction_input.csv"))

unique_drugs = []
for v in df[["inchikey", "cid", "chemical"]].values:
    unique_drugs += [(v[0], v[1], v[2])]
unique_drugs = list(set(unique_drugs))

pgkb2drugbank = {}
with open(pharmgkb_ids_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        pgkb2drugbank[row['PharmGKBId']] = row['DrugBankId']


def extract_drug_names(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug names and brand information
    drug_names_brands = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        generic_name = drug.find('db:name', namespaces=ns).text if drug.find('db:name', namespaces=ns) is not None else "Unknown"
        
        # Extract brand names
        brands = []
        brand_entries = drug.findall('db:international-brands/db:international-brand', namespaces=ns)
        for brand in brand_entries:
            brand_name = brand.find('db:name', namespaces=ns)
            if brand_name is not None:
                brands.append(brand_name.text)

        # Organize data into a dictionary
        drug_info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Generic Name': generic_name,
            'Brand Names': brands
        }
        drug_names_brands.append(drug_info)

    return drug_names_brands

print("Extracting drug names...")
drug_names = extract_drug_names(xml_file)
name2drugbank = {}
for d in drug_names:
    name2drugbank[d["Generic Name"].lower()] = d["DrugBank ID"]
    for b in d["Brand Names"]:
        name2drugbank[b.lower()] = d["DrugBank ID"]


manual_cid2drugbank = {}
with open(os.path.join(data_dir, "manually_annotated.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        manual_cid2drugbank[row["cid"]] = row["drugbank_id"]

cid2drugbank = {}

missing = []
for r in unique_drugs:
    cid = r[1]
    name = r[2].lower()
    if cid in pgkb2drugbank:
        cid2drugbank[cid] = pgkb2drugbank[cid]
        continue
    if name in name2drugbank:
        cid2drugbank[cid] = name2drugbank[name]
    if cid in manual_cid2drugbank:
        cid2drugbank[cid] = manual_cid2drugbank[cid]

cid2drugbank = dict((k,v) for k,v in cid2drugbank.items() if v is not None and v != "None" and v != "." and v != "")
    

with open(data_dir + "/cid2drugbank.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["cid", "drugbank_id"])
    for k,v in cid2drugbank.items():
        writer.writerow([k,v])


def extract_drug_descriptions(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug descriptions
    drug_descriptions = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        description = drug.find('db:description', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Description': description.text if description is not None else None
        }
        drug_descriptions.append(info)

    return drug_descriptions


def extract_drug_indications(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug indications
    drug_indications = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        indication = drug.find('db:indication', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Indication': indication.text if indication is not None else None
        }
        drug_indications.append(info)

    return drug_indications


def extract_drug_toxicity(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug toxicity information
    drug_toxicity = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        toxicity = drug.find('db:toxicity', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Toxicity': toxicity.text if toxicity is not None else None
        }
        drug_toxicity.append(info)

    return drug_toxicity


def extract_drug_pharmacodynamics(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug toxicity information
    drug_pharmacodynamics = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        toxicity = drug.find('db:pharmacodynamics', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Pharmacodynamics': toxicity.text if toxicity is not None else None
        }
        drug_pharmacodynamics.append(info)

    return drug_pharmacodynamics


def extract_mechanism_of_action(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug mechanisms of action
    drug_mechanisms = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        mechanism = drug.find('db:mechanism-of-action', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Mechanism of Action': mechanism.text if mechanism is not None else None
        }
        drug_mechanisms.append(info)

    return drug_mechanisms


def extract_drug_absorption(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug absorption information
    drug_absorptions = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        absorption = drug.find('db:absorption', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Absorption': absorption.text if absorption is not None else None
        }
        drug_absorptions.append(info)

    return drug_absorptions


def extract_drug_metabolism(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug metabolism information
    drug_metabolisms = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        metabolism = drug.find('db:metabolism', namespaces=ns)
        
        # Organize data into a dictionary
        info = {
            'DrugBank ID': drug_id.text if drug_id is not None else None,
            'Metabolism': metabolism.text if metabolism is not None else None
        }
        drug_metabolisms.append(info)

    return drug_metabolisms


def extract_genomic_data(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store detailed genomic interaction information
    genomic_interactions = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        drug_name = drug.find('db:name', namespaces=ns).text if drug.find('db:name', namespaces=ns) is not None else "Unknown"
        
        # SNP Effects: Gene, Genotype, Description
        snp_effects = drug.findall('db:snp-effects/db:effect', namespaces=ns)
        for effect in snp_effects:
            gene_symbol = effect.find('db:gene-symbol', namespaces=ns)
            rs_id = effect.find('db:rs-id', namespaces=ns)  # RS ID can indicate genotype
            description = effect.find('db:description', namespaces=ns)

            # Organize SNP effect data
            effect_info = {
                'DrugBank ID': drug_id.text if drug_id is not None else None,
                'Drug Name': drug_name,
                'Gene Symbol': gene_symbol.text if gene_symbol is not None else None,
                'RS ID (Genotype)': rs_id.text if rs_id is not None else None,
                'Effect Description': description.text if description is not None else None
            }
            genomic_interactions.append(effect_info)
        
        # SNP Adverse Drug Reactions
        snp_adrs = drug.findall('db:snp-adverse-drug-reactions/db:reaction', namespaces=ns)
        for adr in snp_adrs:
            gene_symbol = adr.find('db:gene-symbol', namespaces=ns)
            rs_id = adr.find('db:rs-id', namespaces=ns)
            adverse_reaction = adr.find('db:description', namespaces=ns)  # Corrected to target 'description' directly

            # Organize SNP ADR data
            adr_info = {
                'DrugBank ID': drug_id.text if drug_id is not None else None,
                'Drug Name': drug_name,
                'Gene Symbol': gene_symbol.text if gene_symbol is not None else None,
                'RS ID (Genotype)': rs_id.text if rs_id is not None else None,
                'Adverse Reaction Description': adverse_reaction.text if adverse_reaction is not None else None
            }
            genomic_interactions.append(adr_info)

    return genomic_interactions


def extract_targets(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug target and gene information
    drug_target_genes = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):

        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        
        # Each drug can have multiple targets
        targets = drug.findall('db:targets/db:target', namespaces=ns)
        for target in targets:
            target_name = target.find('db:name', namespaces=ns)
            organism = target.find('db:organism', namespaces=ns)
            # Extract gene name from polypeptide, if available
            polypeptides = target.findall('db:polypeptide', namespaces=ns)
            for polypeptide in polypeptides:
                gene_name = polypeptide.find('db:gene-name', namespaces=ns)

                target_info = {
                    'DrugBank ID': drug_id.text if drug_id is not None else None,
                    'Target Name': target_name.text if target_name is not None else None,
                    "Organism": organism.text if organism is not None else None,
                    'Gene Name': gene_name.text if gene_name is not None else None
                }
                drug_target_genes.append(target_info)

    return drug_target_genes


def extract_drug_enzymes(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug enzyme information
    drug_enzymes = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):
        
        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)

        # Each drug can have multiple enzymes
        enzymes = drug.findall('db:enzymes/db:enzyme', namespaces=ns)
        for enzyme in enzymes:
            enzyme_name = enzyme.find('db:name', namespaces=ns)
            organism = enzyme.find('db:organism', namespaces=ns)
            # Extract gene name from polypeptide, if available
            polypeptides = enzyme.findall('db:polypeptide', namespaces=ns)
            for polypeptide in polypeptides:
                gene_name = polypeptide.find('db:gene-name', namespaces=ns)

                enzyme_info = {
                    'DrugBank ID': drug_id.text if drug_id is not None else None,
                    'Enzyme Name': enzyme_name.text if enzyme_name is not None else None,
                    'Organism': organism.text if organism is not None else None,
                    'Gene Name': gene_name.text if gene_name is not None else None
                }
                drug_enzymes.append(enzyme_info)

    return drug_enzymes

def extract_drug_transporters(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug transporter information
    drug_transporters = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):

        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        
        # Each drug can have multiple transporters
        transporters = drug.findall('db:transporters/db:transporter', namespaces=ns)
        for transporter in transporters:
            transporter_name = transporter.find('db:name', namespaces=ns)
            organism = transporter.find('db:organism', namespaces=ns)
            # Extract gene name from polypeptide, if available
            polypeptides = transporter.findall('db:polypeptide', namespaces=ns)
            for polypeptide in polypeptides:
                gene_name = polypeptide.find('db:gene-name', namespaces=ns)

                transporter_info = {
                    'DrugBank ID': drug_id.text if drug_id is not None else None,
                    'Transporter Name': transporter_name.text if transporter_name is not None else None,
                    'Organism': organism.text if organism is not None else None,
                    'Gene Name': gene_name.text if gene_name is not None else None
                }
                drug_transporters.append(transporter_info)

    return drug_transporters


def extract_drug_carriers(xml_file):
    # Define the namespace dictionary to handle namespaces in the XML file
    ns = {'db': 'http://www.drugbank.ca'}
    
    # Create an XML parser
    parser = etree.XMLParser(ns_clean=True, recover=True)

    # Parse the XML file
    tree = etree.parse(xml_file, parser)
    
    # Initialize a list to store drug carrier information
    drug_carriers = []

    # Iterate over each drug entry
    for drug in tree.xpath('//db:drug', namespaces=ns):

        drug_id = drug.find('.//db:drugbank-id[@primary="true"]', namespaces=ns)
        
        # Each drug can have multiple carriers
        carriers = drug.findall('db:carriers/db:carrier', namespaces=ns)
        for carrier in carriers:
            carrier_name = carrier.find('db:name', namespaces=ns)
            organism = carrier.find('db:organism', namespaces=ns)
            gene_name = None  # Default if no polypeptide or gene name is provided
            polypeptides = carrier.findall('db:polypeptide', namespaces=ns)
            for polypeptide in polypeptides:
                gene_name = polypeptide.find('db:gene-name', namespaces=ns)
                gene_name = gene_name.text if gene_name is not None else None

            carrier_info = {
                'DrugBank ID': drug_id.text if drug_id is not None else None,
                'Carrier Name': carrier_name.text if carrier_name is not None else None,
                'Organism': organism.text if organism is not None else None,
                'Gene Name': gene_name  # This will show the last gene name if multiple polypeptides are present
            }
            drug_carriers.append(carrier_info)

    return drug_carriers


accepted_drugbank_ids = set(cid2drugbank.values())
drugbank2cid = {v:k for k,v in cid2drugbank.items()}

print("Extracting names")
names = {}
for d in tqdm(extract_drug_names(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    names[k] = [d["Generic Name"]] + d["Brand Names"]


print("Extracting drug descriptions...")
descriptions = {}
for d in tqdm(extract_drug_descriptions(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    descriptions[k] = d['Description']


print("Extracting drug indications...")
indications = {}
for d in tqdm(extract_drug_indications(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    indications[k] = d['Indication']


print("Extracting drug pharmacodynamics...")
pharmacodynamics = {}
for d in tqdm(extract_drug_pharmacodynamics(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    pharmacodynamics[k] = d['Pharmacodynamics']


print("Extracting drug mechanisms of action...")
mechanisms = {}
for d in tqdm(extract_mechanism_of_action(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    mechanisms[k] = d['Mechanism of Action']


print("Extracting drug absorption...")
absorptions = {}
for d in tqdm(extract_drug_absorption(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    absorptions[k] = d['Absorption']


print("Extracting drug metabolism...")
metabolisms = {}
for d in tqdm(extract_drug_metabolism(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    metabolisms[k] = d['Metabolism']


print("Extracting drug toxicity...")
toxicities = {}
for d in tqdm(extract_drug_toxicity(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    toxicities[k] = d['Toxicity']


print("Extracting drug targets...")
targets = {}
for d in tqdm(extract_targets(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    if k not in targets:
        targets[k] = []
    x = [
        d["Gene Name"],
        d["Target Name"],
        d["Organism"],
    ]
    targets[k].append(x)


print("Extracting drug enzymes...")
enzymes = {}
for d in tqdm(extract_drug_enzymes(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    if k not in enzymes:
        enzymes[k] = []
    x = [
        d["Gene Name"],
        d["Enzyme Name"],
        d["Organism"],
    ]
    enzymes[k].append(x)


print("Extracting drug transporters...")
transporters = {}
for d in tqdm(extract_drug_transporters(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    if k not in transporters:
        transporters[k] = []
    x = [
        d["Gene Name"],
        d["Transporter Name"],
        d["Organism"],
    ]
    transporters[k].append(x)


print("Extracting drug carriers...")
carriers = {}
for d in tqdm(extract_drug_carriers(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    if k not in carriers:
        carriers[k] = []
    x = [
        d["Gene Name"],
        d["Carrier Name"],
        d["Organism"],
    ]
    carriers[k].append(x)


print("Extracting genomic data...")
genomic_data = {}
for d in tqdm(extract_genomic_data(xml_file)):
    if d["DrugBank ID"] not in accepted_drugbank_ids:
        continue
    k = drugbank2cid[d["DrugBank ID"]]
    if k not in genomic_data:
        genomic_data[k] = []
    genomic_data[k].append(d)


for k,v in tqdm(cid2drugbank.items()):
    data = {
        "pharmgkb_id": k,
        "drugbank_id": v,
        "names": names[k] if k in names else None,
        "description": descriptions[k] if k in descriptions else None,
        "indication": indications[k] if k in indications else None,
        "pharmacodynamics": pharmacodynamics[k] if k in pharmacodynamics else None,
        "mechanism-of-action": mechanisms[k] if k in mechanisms else None,
        "absorption": absorptions[k] if k in absorptions else None,
        "metabolism": metabolisms[k] if k in metabolisms else None,
        "toxicity": toxicities[k] if k in toxicities else None,
        "targets": targets[k] if k in targets else None,
        "enzymes": enzymes[k] if k in enzymes else None,
        "transporters": transporters[k] if k in transporters else None,
        "carriers": carriers[k] if k in carriers else None,
        "genomic-data": genomic_data[k] if k in genomic_data else None,
    }
    with open(os.path.join(data_dir, "json", "{0}.json".format(v)), "w") as f:
        json.dump(data, f, indent=4)
