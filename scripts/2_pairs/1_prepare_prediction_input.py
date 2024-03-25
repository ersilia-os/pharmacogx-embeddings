import pandas as pd
import os
from rdkit import Chem
from rdkit.Chem import Descriptors
from tqdm import tqdm
from standardiser import standardise
import uuid

root = os.path.dirname(os.path.abspath(__file__))

ml_datasets_folder = os.path.join(root, "..", "..", "data", "ml_datasets_pairs")


# Focus compounds are antimalarial and antituberculosis drugs provided by H3D
focus_compounds = pd.read_csv(
    os.path.join(
        root, "..", "..", "data", "of_interest", "curated_drugs_for_gradient.tsv"
    ),
    sep="\t",
)
inchikeys = []


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

# Focus genes are ADME genes provided by H3D
focus_genes = pd.read_csv(
    os.path.join(root, "..", "..", "data", "of_interest", "adme_gene_list.tsv"),
    sep="\t",
)

print(focus_genes)

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

pharmgkb2prot = {}
pharmgkb2gene = {}
for r in pd.read_csv(
    os.path.join(root, "..", "..", "data", "other", "pgkb_gene_uniprot_mapping.tsv"),
    sep="\t",
).values:
    pharmgkb2prot[r[0]] = r[2]
    pharmgkb2gene[r[0]] = r[1]

# interest data
our_compounds = set(focus_compounds["inchikey"].tolist())
adme_genes = set(focus_genes["PharmGKB ID"])

# screening data (our genes + all genes in PharmGKB with *some* kind of annotation)
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

prot2row = {}
for r in df[["gid", "gene"]].values:
    gid = str(r[0])
    gene = str(r[1])
    if gid == "nan" or gene == "nan":
        continue
    if gid not in pharmgkb2prot:
        continue
    prot = pharmgkb2prot[gid]
    prot2row[prot] = (prot, gene, gid, 1)
my_gids = set(df["gid"])

# inchikey, cid, chemical, uniprot_ac, gene, gid

for gid in adme_genes:
    if gid in my_gids:
        continue
    if gid not in pharmgkb2prot:
        continue
    p = pharmgkb2prot[gid]
    g = pharmgkb2gene[gid]
    prot2row[p] = (p, g, gid, 0)

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
cid2inchikey = {}
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
    cid2inchikey[cid] = inchikey

ik2row = {}
for k, v in tqdm(cid2inchikey.items()):
    cid = k
    inchikey = v
    chemical = str(cid2chemical[cid])
    smiles = str(cid2chemical[cid])
    if cid == "nan" or chemical == "nan" or smiles == "nan":
        continue
    ik2row[inchikey] = (inchikey, cid, chemical, 1)

for r in focus_compounds[["inchikey", "chemical"]].values:
    if r[0] in ik2row:
        continue
    else:
        cid = "nan-{0}".format(str(uuid.uuid4()))
        ik2row[r[0]] = (r[0], cid, r[1], 0)

R = []
for kc, vc in ik2row.items():
    for kp, vp in prot2row.items():
        r = list(vc[:3]) + list(vp[:3]) + [vc[3]] + [vp[3]]
        R += [r]

columns = [
    "inchikey",
    "cid",
    "chemical",
    "uniprot_ac",
    "gene",
    "gid",
    "chemical_in_pgkb",
    "gene_in_pgkb",
]

print(len(ik2row))
print(len(prot2row))

di = pd.DataFrame(R, columns=columns)

coi = []
for ik in di["inchikey"].tolist():
    if ik in our_compounds:
        coi += [1]
    else:
        coi += [0]
di["chemical_of_interest"] = coi

goi = []
for p in di["gid"].tolist():
    if p in adme_genes:
        goi += [1]
    else:
        goi += [0]
di["adme_gene"] = goi

used = set()
for r in pd.read_csv(os.path.join(ml_datasets_folder, "df_all_outcomes_all_genes.csv"))[
    ["cid", "gid"]
].values:
    used.update([tuple(r)])

used_pk = set()
for r in pd.read_csv(os.path.join(ml_datasets_folder, "df_only_pk_all_genes.csv"))[
    ["cid", "gid"]
].values:
    used_pk.update([tuple(r)])

used_pk_adme = set()
for r in pd.read_csv(
    os.path.join(ml_datasets_folder, "df_only_pk_only_adme_genes.csv")
)[["cid", "gid"]].values:
    used_pk_adme.update([tuple(r)])

u0 = []
u1 = []
u2 = []
for r in di[["cid", "gid"]].values:
    r = tuple(r)
    if r in used:
        u0 += [1]
    else:
        u0 += [0]
    if r in used_pk:
        u1 += [1]
    else:
        u1 += [0]
    if r in used_pk_adme:
        u2 += [1]
    else:
        u2 += [0]
di["train_set"] = u0
di["train_set_pk"] = u1
di["train_set_pk_adme"] = u2

print(di)

di.to_csv(
    os.path.join(ml_datasets_folder, "chemical_gene_pairs_prediction_input.csv"),
    index=False,
)
