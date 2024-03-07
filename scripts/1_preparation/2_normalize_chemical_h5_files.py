import os
import sys
import json

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import H5Normalizer

available_descs = os.path.join(
    root, "..", "..", "data", "chemical_descriptors", "available_descs.json"
)

with open(available_descs, "r") as f:
    data = json.load(f)

descs = [
    eosid
    for eosid in data["chemical_descriptors"].keys()
    if data["chemical_descriptors"][eosid]["normalized"] == True
]

for eosid in descs:
    try:
        descs_path = os.path.join(
            root, "..", "..", "data", "chemical_descriptors", f"{eosid}.h5"
        )
        normalizer = H5Normalizer(descs_path)
        normalizer.run()
    except:
        print(f"Descriptor {eosid} not calculated")
