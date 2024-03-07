import os
import sys
import joblib
import json

root = os.path.dirname(os.path.abspath(__file__))
embeddings_folder = os.path.join(root, "..", "..", "embeddings")
if not os.path.exists(embeddings_folder):
    os.mkdir(embeddings_folder)

sys.path.append(os.path.join(root, "..", "..", "src"))

from compound_structures import CompoundStructureEmbedding
from protein_sequences import ProteinSequenceEmbedding
from bioteque import BiotequeGeneEmbedding, BiotequeCompoundEmbedding

bge = BiotequeGeneEmbedding()
bce = BiotequeCompoundEmbedding()
pse = ProteinSequenceEmbedding()
cse = CompoundStructureEmbedding()

print(bge.available())
print(bce.available())
print(pse.available())
print(cse.available())

compound_embeddings_names = []
protein_embeddings_names = []

print("Reading embeddings and saving embeddings")

for x in pse.available():
    protein_embeddings_names += [x]
    file_name = "protein-sequence---{0}.joblib".format(x)
    print(file_name)
    data = ProteinSequenceEmbedding(x).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in bge.available().values:
    protein_embeddings_names += ["--".join(x)]
    file_name = "protein-bioteque---{0}.joblib".format("--".join(x))
    print(file_name)
    data = BiotequeGeneEmbedding(x[0], x[1]).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in cse.available():
    compound_embeddings_names += [x]
    file_name = "compound-structure---{0}.joblib".format(x)
    print(file_name)
    data = CompoundStructureEmbedding(x).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in bce.available().values:
    compound_embeddings_names += ["--".join(x)]
    file_name = "compound-bioteque---{0}.joblib".format("--".join(x))
    print(file_name)
    data = BiotequeCompoundEmbedding(x[0], x[1]).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

with open(os.path.join(embeddings_folder, "available_embeddings.json"), "w") as f:
    json.dump(
        {"compound": compound_embeddings_names, "protein": protein_embeddings_names},
        f,
        indent=4,
    )
