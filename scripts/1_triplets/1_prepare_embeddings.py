import os
import sys
import joblib
import json

root = os.path.dirname(os.path.abspath(__file__))
embeddings_folder = os.path.join(root, "..", "..", "embeddings")

sys.path.append(os.path.join(root, "..", "..", "src"))

from compound_structures import CompoundStructureEmbedding
from protein_sequences import ProteinSequenceEmbedding
from bioteque import BiotequeGeneEmbedding
from variant import VariantEmbedding

bge = BiotequeGeneEmbedding()
pse = ProteinSequenceEmbedding()
cse = CompoundStructureEmbedding()
vne = VariantEmbedding()

print(bge.available())
print(pse.available())
print(cse.available())
print(vne.available())

compound_embedding_names = []
protein_embeddings_names = []
variant_embedding_names = []

print("Reading embeddings and saving embeddings")

for x in cse.available():
    compound_embedding_names += [x]
    file_name = "compound-structure---{0}.joblib".format(x)
    print(file_name)
    data = CompoundStructureEmbedding(x).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in pse.available():
    protein_embeddings_names += [x]
    file_name = "protein-sequence---{0}.joblib".format(x)
    print(file_name)
    data = ProteinSequenceEmbedding(x).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in bge.available().values:
    protein_embeddings_names += ["--".join(x)]
    file_name = "bioteque---{0}.joblib".format("--".join(x))
    print(file_name)
    data = BiotequeGeneEmbedding(x[0], x[1]).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

for x in vne.available().values:
    variant_embedding_names += [x]
    file_name = "variant---{0}.joblib".format(x)
    print(file_name)
    data = VariantEmbedding(x).get()
    joblib.dump(data, os.path.join(embeddings_folder, file_name))

with open(os.path.join(embeddings_folder, "available_embeddings.json"), "w") as f:
    json.dump(
        {
            "compound": compound_embedding_names,
            "protein": protein_embeddings_names,
            "variant": variant_embedding_names,
        },
        f,
        indent=4,
    )
