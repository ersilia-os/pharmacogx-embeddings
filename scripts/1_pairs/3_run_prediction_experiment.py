import pandas as pd
import os
import sys
from tqdm import tqdm

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))
from bimodal_model import EnsembleBimodalStackedModel, get_embedding_names

df = pd.read_csv(
    os.path.join(
        root,
        "..",
        "..",
        "data",
        "ml_datasets_pairs",
        "chemical_gene_pairs_prediction_input.csv",
    )
)
df = df[df["chemical_of_interest"] == 1]

embeddings_names = get_embedding_names()
cemb_names_list = embeddings_names["compound"]
pemb_names_list = embeddings_names["protein"]

sufixes = [
    ("all_outcomes", "all_genes"),
    ("only_pk", "all_genes"),
    ("only_pk", "only_adme_genes"),
]

fold_groups = []

results_folder = os.path.join(root, "..", "..", "results_pairs")
if not os.path.exists(results_folder):
    os.mkdir(results_folder)

for sufix_0, sufix_1 in sufixes:
    model_name = "model_{0}_{1}".format(sufix_0, sufix_1)
    print(model_name)
    model_folder = os.path.join(root, "..", "..", "models", "models_pairs", model_name)
    n_folds = 0
    for l in os.listdir(model_folder):
        if l.startswith("fold_"):
            n_folds += 1
    fg0 = []
    fg1 = []
    for i in tqdm(range(n_folds)):
        k_model_folder = "{0}/fold_{1}".format(model_folder, i)
        model = EnsembleBimodalStackedModel(
            cemb_names_list, pemb_names_list, model_folder=k_model_folder
        )
        df = model.predict(df)
        columns = list(df.columns)
        c0 = columns[-2]
        c1 = columns[-1]
        c0 = "{0}_{1}_{2}_{3}".format(c0, sufix_0, sufix_1, i)
        c1 = "{0}_{1}_{2}_{3}".format(c1, sufix_0, sufix_1, i)
        fg0 += [c0]
        fg1 += [c1]
        columns[-2:] = [c0, c1]
        df.columns = columns
    fold_groups += [
        (
            "{0}_{1}_{2}".format("y_hat", sufix_0, sufix_1),
            "{0}_{1}_{2}".format("support", sufix_0, sufix_1),
            fg0,
            fg1,
        )
    ]

for fg in fold_groups:
    cn0 = fg[0]
    cn1 = fg[1]
    cols0 = fg[2]
    cols1 = fg[3]
    df[cn0] = df[cols0].mean(axis=1)
    df[cn1] = df[cols1].mean(axis=1)
    df = df.drop(cols0 + cols1, axis=1)

df.to_csv(
    os.path.join(
        results_folder, "results", "chemical_gene_pairs_prediction_output_focus.csv"
    ),
    index=False,
)
