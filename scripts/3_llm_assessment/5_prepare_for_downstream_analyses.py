import pandas as pd
import os
root = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(root, "../../results/results_pairs/chemical_gene_pairs_prediction_output_focus_with_variant_aggregates_top50_filter_llm_top10.csv"))
df = df[df["llm_rank"] <= 10]
df_ = df[["inchikey", "cid", "chemical", "uniprot_ac", "gene", "gid"]].copy()
df_["llm_rank"] = [int(x) for x in df["llm_rank"].tolist()]
df_.to_csv(os.path.join(root, "../../results/results_pairs/llm_top10_only_minimal_info.csv"), index=False)