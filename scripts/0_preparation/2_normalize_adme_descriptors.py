import pandas as pd
import os
import h5py
import numpy as np

results_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "chemical_descriptors"
)

# Load the data from eos7d58.csv file
df = pd.read_csv(os.path.join(results_dir, "eos7d58.csv"))

# Filter only for the columns that contain the keyword drugank, since this means they have been normalized
value_columns = [c for c in list(df.columns) if "drugbank" in c]
R = np.array(df[value_columns], dtype=np.float32)
smiles_list = df["input"].tolist()
inchikey_list = df["key"].tolist()

# Save the data to a new h5 file
h5_file = os.path.join(results_dir, "eos7d58_norm.h5")
if os.path.exists(h5_file):
    os.remove(h5_file)
with h5py.File(h5_file, "w") as f:
    f.create_dataset(
        "Inputs", data=np.array(smiles_list, dtype=h5py.string_dtype())
    )
    f.create_dataset(
        "Keys", data=np.array(inchikey_list, dtype=h5py.string_dtype())
    )
    f.create_dataset("Values", data=R)