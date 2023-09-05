import os
import argparse
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "src"))
from samplers import PositiveNegativeSampler
from splitters import RandomPairSplitter
from compound_structures import CompoundStructureEmbedding
from protein_sequences import ProteinSequenceEmbedding
from bioteque import BiotequeGeneEmbedding
from bimodal_model import (
    EnsembleBimodalStackedModel,
    load_ensemble_bimodal_stacked_model,
)

bge = BiotequeGeneEmbedding()
pse = ProteinSequenceEmbedding()
cse = CompoundStructureEmbedding()

parser = argparse.ArgumentParser()

parser.add_argument("--model_name", type=str, required=True)
parser.add_argument("--input_csv", type=str, required=True)
parser.add_argument("--negative_ratio", type=int, default=10)

args = parser.parse_args()
model_name = args.model_name
input_csv = args.input_csv
negative_ratio = args.negative_ratio

df = pd.DataFrame(input_csv, index=False)

ds = PositiveNegativeSampler(df, negative_ratio).sample()

ds_tr, ds_te = RandomPairSplitter().split(ds)

cemb_list = []
for x in cse.available():
    cemb_list += [(x, CompoundStructureEmbedding(x).get())]

pemb_list = []
for x in pse.available():
    pemb_list += [(x, ProteinSequenceEmbedding(x).get())]

for x in bge.available().values:
    pemb_list += [(x, BiotequeGeneEmbedding(x[0], x[1]).get())]

model = EnsembleBimodalStackedModel(cemb_list[:1], pemb_list[:1])
model.fit(ds_tr)
model.evaluate(ds_te)
model_folder = model.model_folder
model = load_ensemble_bimodal_stacked_model(model_folder)
df = model.predict(ds_te)
