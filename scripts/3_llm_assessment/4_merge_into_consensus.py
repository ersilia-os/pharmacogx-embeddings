import os
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(root, "..", "..", "src"))
from llm_reranking import LLMCompoundGeneRerankerConsensus

# If lazy is True, do not use LLM for the explanation. Only for testing purposes
lazy = False

results_dir = os.path.join(root, "..", "..", "results", "results_pairs")

df = pd.read_csv(os.path.join(results_dir, "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_top50_filter.csv"))

chemicals = sorted(df["chemical"].unique().tolist())

data_pairs = {}
for i, chemical in enumerate(chemicals):
    print(i, chemical)
    ranker = LLMCompoundGeneRerankerConsensus(results_dir=results_dir, lazy=lazy)
    data = ranker.run(chemical)
    for d in data:
        data_pairs[(chemical, d["gene"])] = (d["rank"], d["explanation"])

ranks = []
explanations = []
for r in df[["chemical", "gene"]].values:
    k = (r[0], r[1])
    if k in data_pairs:
        ranks += [data_pairs[k][0]]
        explanations += [data_pairs[k][1]]
    else:
        ranks += [None]
        explanations += [None]

df["llm_rank"] = ranks
df["llm_expl"] = explanations

df.to_csv(os.path.join(results_dir, "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_top50_filter_llm_top10.csv"), index=False)