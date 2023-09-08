import pandas as pd
import os
from rdkit import Chem
from tqdm import tqdm
import uuid

root = os.path.dirname(os.path.abspath(__file__))

ml_datasets_folder = os.path.join(root, "..", "data", "ml_datasets")

# Focus compounds are antimalarial and antituberculosis drugs provided by H3D
focus_compounds = pd.read_csv(
    os.path.join(root, "../data/of_interest/curated_drugs_for_gradient.tsv"), sep="\t"
)
inchikeys = []
for smi in focus_compounds["SMILES"].tolist():
    mol = Chem.MolFromSmiles(smi)
    inchi = Chem.rdinchi.MolToInchi(mol)[0]
    inchikey = Chem.rdinchi.InchiToInchiKey(inchi)
    inchikeys += [inchikey]
focus_compounds["inchikey"] = inchikeys

# Focus genes are ADME genes provided by H3D
focus_genes = pd.read_csv(
    os.path.join(root, "../data/of_interest/adme_gene_list.tsv"), sep="\t"
)

# Map genes to UniProt ACs
hp = pd.read_csv(
    os.path.join(root, "../data/other/human_proteome_with_genenames.tab"), sep="\t"
)
cols = list(hp.columns)
hp = hp[(hp[cols[0]].notnull()) & (hp[cols[2]].notnull())]
g2p = {}
up = pd.read_csv(
    os.path.join("..", "data", "other", "human_proteome_with_genenames.tab"),
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

# interest data
our_compounds = set(focus_compounds["inchikey"].tolist())
adme_genes = []
for g in focus_genes["Gene Symbol"].tolist():
    if g in g2p:
        adme_genes += [(g2p[g], g)]
adme_genes = set(adme_genes)
adme_genes_set = set([x[0] for x in list(adme_genes)])

# screening data (our genes + all genes in PharmGKB with *some* kind of annotation)
df = pd.read_csv(
    os.path.join(
        root, "..", "data", "pharmgkb_processed", "final_tables", "pgkb_merged.csv"
    ),
    low_memory=False,
)

prot2row = {}
for r in df[["gid", "gene"]].values:
    gid = str(r[0])
    gene = str(r[1])
    if gid == "nan" or gene == "nan":
        continue
    if gene not in g2p:
        continue
    prot = g2p[gene]
    prot2row[prot] = (prot, gene, gid, 1)

# inchikey, cid, chemical, uniprot_ac, gene, gid

for p, g in adme_genes:
    if p in prot2row:
        continue
    gid = "nan-{0}".format(str(uuid.uuid4()))
    prot2row[p] = (p, g, gid, 0)

ik2row = {}
compounds = list(
    set([(r[0], r[1], r[2]) for r in df[["cid", "chemical", "smiles"]].values])
)
for r in tqdm(compounds):
    cid = str(r[0])
    chemical = str(r[1])
    smiles = str(r[2])
    if cid == "nan" or chemical == "nan" or smiles == "nan":
        continue
    mol = Chem.MolFromSmiles(smiles)
    inchi = Chem.rdinchi.MolToInchi(mol)[0]
    inchikey = Chem.rdinchi.InchiToInchiKey(inchi)
    ik2row[inchikey] = (inchikey, cid, chemical, 1)

for r in focus_compounds[["inchikey", "Drug"]].values:
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
for p in di["uniprot_ac"].tolist():
    if p in adme_genes_set:
        goi += [1]
    else:
        goi += [0]
di["adme_gene"] = goi

used = set()
for r in pd.read_csv(
    os.path.join(root, "..", "data", "ml_datasets", "df_all_outcomes_all_genes.csv")
)[["cid", "gid"]].values:
    used.update([tuple(r)])

used_pk = set()
for r in pd.read_csv(
    os.path.join(root, "..", "data", "ml_datasets", "df_only_pk_all_genes.csv")
)[["cid", "gid"]].values:
    used_pk.update([tuple(r)])

used_pk_adme = set()
for r in pd.read_csv(
    os.path.join(root, "..", "data", "ml_datasets", "df_only_pk_only_adme_genes.csv")
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
    os.path.join(
        root, "..", "data", "ml_datasets", "chemical_gene_pairs_prediction_input.csv"
    ),
    index=False,
)
