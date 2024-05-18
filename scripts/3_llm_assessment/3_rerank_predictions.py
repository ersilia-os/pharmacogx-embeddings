import os
import sys
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(root, "..", "..", "src"))
from llm_reranking import LLMCompoundGeneReranker

results_dir = os.path.join(root, "..", "..", "results", "results_pairs")
df = pd.read_csv(os.path.join(root, "..", "..", "results", "results_pairs", "chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_top50_filter.csv"))

chemical_names = df["chemical"].unique().tolist()

print("Working on chemicals", len(chemical_names))

for round in range(3):
    print(f"Round {round}")
    for i, chemical_name in enumerate(chemical_names):
        print(i, chemical_name)
        ranker = LLMCompoundGeneReranker(df, results_dir=results_dir, round=round)
        data = ranker.run(chemical_name)