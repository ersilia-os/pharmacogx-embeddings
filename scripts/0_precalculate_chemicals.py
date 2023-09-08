import pandas as pd
import os
from rdkit import Chem
from rdkit.Chem import InchiToInchiKey, MolToInchi
from rdkit.Chem import Descriptors
from standardiser import standardise
import h5py
import numpy as np
from eosce.models import ErsiliaCompoundEmbeddings
from rdkit import RDLogger
import warnings

# Suppress RDKit warnings
lg = RDLogger.logger()
lg.setLevel(RDLogger.CRITICAL)

# Suppress Python warnings
warnings.filterwarnings("ignore")

root = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(root, "..", "data", "chemical_descriptors")

if not os.path.exists(os.path.join(results_dir, "drug_molecules.csv")):
    df = pd.read_csv(
        os.path.join(root, "..", "data", "pharmgkb_processed", "chemical.csv")
    )
    smiles_list = [
        y for x in df[df["smiles"].notnull()]["smiles"].tolist() for y in x.split(" ")
    ]
    print(len(smiles_list))

    df = pd.read_csv(
        os.path.join(
            root, "..", "data", "of_interest", "curated_drugs_for_gradient.tsv"
        ),
        delimiter="\t",
    )
    smiles_list += [
        y for x in df[df["SMILES"].notnull()]["SMILES"].tolist() for y in x.split(" ")
    ]
    print(len(smiles_list))

    """
    sdf_file = os.path.join(
        root, "..", "data", "chemical_descriptors", "open_structures.sdf"
    )
    suppl = Chem.SDMolSupplier(sdf_file)
    for mol in suppl:
        if mol is not None:
            smiles = Chem.MolToSmiles(mol)
            smiles_list.append(smiles)
    """

    def check_molecule(mol):
        num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
        has_3_carbons = num_carbons >= 3
        molecular_weight = Descriptors.MolWt(mol)
        weight_between_100_and_1000 = 100 <= molecular_weight <= 1000
        return has_3_carbons and weight_between_100_and_1000

    ik2smi = {}
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if not check_molecule(mol):
            continue
        try:
            mol = standardise.run(mol)
        except:
            continue
        if mol is None:
            continue
        inchi = MolToInchi(mol)
        inchi_key = InchiToInchiKey(inchi)
        ik2smi[inchi_key] = Chem.MolToSmiles(mol)

    R = []
    for k, v in ik2smi.items():
        R += [[k, v]]
    df = pd.DataFrame(R, columns=["inchikey", "smiles"])
    df.to_csv(os.path.join(results_dir, "drug_molecules.csv"), index=False)

else:
    df = pd.read_csv(os.path.join(results_dir, "drug_molecules.csv"))
    smiles_list = df["smiles"].tolist()
    model = ErsiliaCompoundEmbeddings()
    embeddings = model.transform(smiles_list)
    print(embeddings.shape)
    h5_file = os.path.join(results_dir, "ersilia_compound_embedding.h5")
    if os.path.exists(h5_file):
        os.remove(h5_file)
    with h5py.File(h5_file, "w") as f:
        f.create_dataset(
            "Inputs", data=np.array(smiles_list, dtype=h5py.string_dtype())
        )
        f.create_dataset(
            "Keys", data=np.array(df["inchikey"].tolist(), dtype=h5py.string_dtype())
        )
        f.create_dataset("Values", data=np.array(embeddings, dtype=np.float32))

    # the rest are generated, more simply, with ersilia CLI (eos4u6p, eos7w6n, etc)
