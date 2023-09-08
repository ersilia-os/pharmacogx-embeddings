import os
import argparse
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "src"))
from samplers import PositiveNegativeSampler
from splitters import RandomPairSplitter
from bimodal_model import EnsembleBimodalStackedModel, get_embedding_names

parser = argparse.ArgumentParser()

parser.add_argument("--model_name", type=str, required=False, default=None)
parser.add_argument(
    "--only_adme_genes",
    action="store_true",
    help="Flag to indicate if only ADME genes should be used.",
)
parser.add_argument(
    "--only_pk", action="store_true", help="Flag to indicate if only PK should be used."
)
parser.add_argument("--negative_ratio", type=int, default=10)
parser.add_argument("--n_folds", type=int, default=5)

args = parser.parse_args()
model_name = args.model_name
only_pk = args.only_pk
only_adme_genes = args.only_adme_genes
negative_ratio = args.negative_ratio
n_folds = args.n_folds

if only_pk:
    sufix_0 = "only_pk"
else:
    sufix_0 = "all_outcomes"

if only_adme_genes:
    sufix_1 = "only_adme_genes"
else:
    sufix_1 = "all_genes"

input_csv = os.path.join(
    root, "..", "data", "ml_datasets", "df_{0}_{1}.csv".format(sufix_0, sufix_1)
)

if model_name is None:
    model_name = "model_{0}_{1}".format(sufix_0, sufix_1)

model_folder = os.path.join(root, "..", "models", model_name)

print("Training models")

embeddings_names = get_embedding_names()
cemb_names_list = embeddings_names["compound"][:2]
pemb_names_list = embeddings_names["protein"][:2]

for i in range(n_folds):
    k_model_folder = "{0}/fold_{1}".format(model_folder, i)

    df = pd.read_csv(input_csv)

    ds = PositiveNegativeSampler(df, negative_ratio).sample()

    ds_tr, ds_te = RandomPairSplitter().split(ds)

    model = EnsembleBimodalStackedModel(
        cemb_names_list, pemb_names_list, model_folder=k_model_folder
    )
    model.fit(ds_tr)
    model.evaluate(ds_te)