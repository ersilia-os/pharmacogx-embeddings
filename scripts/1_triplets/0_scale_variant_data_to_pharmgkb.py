import os
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "src"))

from variants import SnpEffTableEncoder

pharmgkb_file = os.path.join(
    root, "..", "data", "variants", "pharmgkb", "pharmgkb_mutations.tsv"
)

print("Reading data")
data = pd.read_csv(pharmgkb_file, sep="\t", low_memory=False)
print(data.shape)
data = data.head()

print("Starting encoder")
encoder = SnpEffTableEncoder("other")

print("Calculating encoder")
emb = encoder.calculate(data)

print(emb)
