# Imports
import pandas as pd
import argparse
import os
from rdkit import Chem
from rdkit import RDLogger
from standardiser import standardise
from rdkit.Chem import Descriptors

RDLogger.DisableLog("rdApp.*")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--only_adme_genes",
    action="store_true",
    help="Flag to indicate if only ADME genes should be used.",
)
parser.add_argument(
    "--only_pk", action="store_true", help="Flag to indicate if only PK should be used."
)

parser.add_argument("--exp", type=str, default=10)

args = parser.parse_args()
only_adme_genes = args.only_adme_genes
only_pk = args.only_pk
exp = args.exp

root = os.path.dirname(os.path.abspath(__file__))

output_folder = os.path.join(root, "..", "data", f"ml_datasets_pairs_{exp}")
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Read main processed PharmGKB table
df = pd.read_csv(
    os.path.join(
        root,
        "..",
        "..",
        "data",
        "pharmgkb_processed",
        "13_pgkb_merged.csv",
    ),
    low_memory=False,
)


def table_statistics(df):
    pairs = set([tuple(x) for x in df[["cid", "gid"]].values])
    triplets = set([tuple(x) for x in df[["cid", "vid", "gid"]].values])
    print("Compounds: ", len(set(df["cid"])))
    print("Genes:     ", len(set(df["gid"])))
    print("Variants:  ", len(set(df["vid"])))
    print("Pairs:     ", len(pairs))
    print("Triplets:  ", len(triplets))

print("> Initial table")
table_statistics(df)
print("")

# Focus genes are ADME genes provided by H3D
focus_genes = pd.read_csv(
    os.path.join(root, "..", "..", "data", "of_interest", "adme_gene_list.tsv"),
    sep="\t",
)

# Focus compounds are antimalarial and antituberculosis drugs provided by H3D
focus_compounds = pd.read_csv(
    os.path.join(
        root, "..", "..", "data", "of_interest", "curated_drugs_for_gradient.tsv"
    ),
    sep="\t",
)


def check_molecule(mol):
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    has_3_carbons = num_carbons >= 3
    molecular_weight = Descriptors.MolWt(mol)
    weight_between_100_and_1000 = 100 <= molecular_weight <= 1000
    return has_3_carbons and weight_between_100_and_1000


R = []
for r in focus_compounds[["SMILES", "Drug"]].values:
    smi = r[0]
    mol = Chem.MolFromSmiles(smi)
    if not check_molecule(mol):
        continue
    try:
        mol = standardise.run(mol)
    except:
        continue
    if mol is None:
        continue
    inchi = Chem.rdinchi.MolToInchi(mol)[0]
    inchikey = Chem.rdinchi.InchiToInchiKey(inchi)
    R += [(inchikey, r[1], Chem.MolToSmiles(mol))]
focus_compounds = pd.DataFrame(R, columns=["inchikey", "chemical", "smiles"])
focus_genes = focus_genes[focus_genes["PharmGKB ID"].notnull()]

if only_adme_genes:
    df = df[df["gid"].isin(focus_genes["PharmGKB ID"].tolist())]
    print("> ADME genes filter")
    table_statistics(df)
    print("")

# Map compounds to InChIKeys
cid2smi_ = {}
cid2chemical = {}
for r in df[["cid", "smiles", "chemical"]].values:
    cid = r[0]
    smi = r[1]
    if str(smi) == "nan":
        continue
    if str(r[2]) == "nan":
        continue
    cid2smi_[cid] = smi
    cid2chemical[cid] = r[2]

cid2smi = {}
cid2key = {}
for cid, smi in cid2smi_.items():
    mol = Chem.MolFromSmiles(smi)
    if not check_molecule(mol):
        continue
    try:
        mol = standardise.run(mol)
    except:
        continue
    if mol is None:
        continue
    inchi = Chem.rdinchi.MolToInchi(mol)[0]
    inchikey = Chem.rdinchi.InchiToInchiKey(inchi)
    smiles = Chem.MolToSmiles(mol)
    cid2smi[cid] = smiles
    cid2key[cid] = inchikey

# Map genes to UniProt ACs
hp = pd.read_csv(
    os.path.join(
        root, "..", "..", "data", "other", "human_proteome_with_genenames.tab"
    ),
    sep="\t",
)
cols = list(hp.columns)
hp = hp[(hp[cols[0]].notnull()) & (hp[cols[2]].notnull())]
g2p = {}
up = pd.read_csv(
    os.path.join(
        root, "..", "..", "data", "other", "human_proteome_with_genenames.tab"
    ),
    sep="\t",
)
for v in up[
    ["Entry", "Gene names", "Gene names  (primary )", "Gene names  (synonym )"]
].values:
    p = v[0]
    g = []
    for x in v[1:]:
        x = str(x)
        if x == "nan":
            continue
        for y in x.split(" "):
            g += [y]
    for x in g:
        g2p[x] = p

gid2key = {}
for r in df[["gid", "gene"]].values:
    if str(r[0]) == "nan" or str(r[1]) == "nan":
        continue
    if r[1] not in g2p:
        continue
    gid2key[r[0]] = g2p[r[1]]


pharmgkb2prot = {}
pharmgkb2gene = {}
for r in pd.read_csv(
    os.path.join(root, "..", "..", "data", "other", "pgkb_gene_uniprot_mapping.tsv"),
    sep="\t",
).values:
    pharmgkb2prot[r[0]] = r[2]
    pharmgkb2gene[r[0]] = r[1]


# Filter to only consider PK relationships
if only_pk:
    print("> PK filter")
    df = df[df["phenotype"].isin(["Metabolism/PK"])]  # , "Toxicity", "Dosage"])]
    table_statistics(df)
    print("")

#df = df[df["evidence"] != "4"] #this is the original
#df = df[df["evidence"].isin(["1A", "1B", "2", "3"])] #this is ev3
#df = df[df["evidence"].isin(["1A", "1B", "2"])] #this is ev2
#df = df[df["evidence"].isin(["1A", "1B", "2", "5", "6"])] #this is ev5
df = df[df["evidence"].isin(["1A", "1B", "2", "6"])] #this is ev6

print("> Evidence filter")
table_statistics(df)
print("")

# Build a unique set of triplets
triplets = set()
not_prot = []
not_chem = []
for r in df[["cid", "chemical", "gid", "gene", "vid", "variant"]].values:
    r = tuple(r)
    if r[0] not in cid2key:
        ckey = None
        not_chem += [r[0]]
    else:
        ckey = cid2key[r[0]]
    if r[2] not in pharmgkb2prot:
        gkey = None
        not_prot += [r[2]]
    else:
        gkey = pharmgkb2prot[r[2]]
    if gkey is None or ckey is None:
        continue
    triplets.update([(ckey, r[0], r[1], gkey, r[3], r[2], r[5], r[4])])

print(">> Removals")
triplets = list(triplets)
triplets = list(set(triplets))
print("Proteins lost: ", len(set(not_prot)))
print("Chemicals lost:", len(set(not_chem)))
print("")

dt = pd.DataFrame(
    triplets,
    columns=[
        "inchikey",
        "cid",
        "chemical",
        "uniprot_ac",
        "gene",
        "gid",
        "variant",
        "vid",
    ],
)
print("> Final table")
table_statistics(dt)

if only_pk:
    sufix_0 = "only_pk"
else:
    sufix_0 = "all_outcomes"

if only_adme_genes:
    sufix_1 = "only_adme_genes"
else:
    sufix_1 = "all_genes"

file_name = "df_{0}_{1}.csv".format(sufix_0, sufix_1)

dt.to_csv(os.path.join(output_folder, file_name), index=False)
