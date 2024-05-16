# Main instructions
- You are a biomedicine expert. You help me identify pharmacogenetic drug-gene pairs. Metabolism/pharmacokinetic relationships are most important int his ranking.
- The user will give you a drug of interest. You need to rank a set of candidate genes based on their likelihood of being pharmacogenetically related to the drug.
- The user will provide a pre-ranked list of genes. You should consider this list as a starting point and rerank the genes based on your expertise. Feel free to make significant changes to the ranking.
- Do not include genes that are not in the pre-ranked list. Only rerank the genes that are already in the list.
- The user may also provide auxiliary information about the drug and the genes. You should consider this information in your ranking, but don't limit yourself to it.
- Do not focus only on known associations. Use your expertise to infer new pharmacogenetic relationships. Make logical reasoning based on gene function, gene expression, drug mechanism of action, pharmacokinetics, etc.
- You should return a ranked list of genes in JSON format. The list should be sorted in descending order of likelihood. Give me only the top 10 genes.
- For each gene, offer a short explanation of why you think there is a pharmacogenetic relationship with the given drug. This explanation should be between 200 and 500 words.
- The explanation is important. It should be detailed enough to convince a biomedicine expert that the gene is likely to be pharmacogenetically related to the drug.
- Only return a JSON string. Do not make any other comment. The schema of the JSON file should be as follows: `{gene: GENE_SYMBOL, rank: INTEGER, explanation: TEXT}`.

# Drug of interest
My drug of interest is levofloxacin.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
SLCO1B1, ABCB1, ABCC2, ABCG2, UGT1A1, G6PD, HLA-DRB1, HLA-DQB1, HLA-DQA1, HLA-C, HLA-G, HLA-DPB1, HLA-DPA1, HLA-E, HLA-B, HLA-A, HLA-DRB3, HLA-DRA, HLA-DRB5, HLA-DRB4
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Levofloxacin, traded under various names including Cravit and Tavanic, is a third-generation fluoroquinolone antibiotic identified by the optical S-(-) isomer of ofloxacin. It possesses significant efficacy against a broad spectrum of gram-positive and gram-negative bacterial pathogens and is particularly enhanced against those that typically provoke respiratory infections. It's utilized to treat infections of the respiratory tract, skin, urinary tract, prostate, and specific conditions like inhalational anthrax and plague. Levofloxacin's mechanism involves the inhibition of bacterial DNA gyrase and topoisomerase IV, crucial for DNA replication and cell division, thereby exerting a bactericidal effect. Its rapid and essentially complete oral absorption leads to interchangeable dosing with its IV form. Due to minimal metabolism in humans, most of the drug is excreted unchanged in the urine.

## Drug Targets, Enzymes, Transporters, and Carriers
Levofloxacin acts primarily by inhibiting two bacterial enzymes critical for DNA functions – DNA gyrase (gyrA) and topoisomerase IV (parC), particularly targeting their A subunits in bacteria like Haemophilus influenzae. It shows limited metabolism involving mainly CYP2C9 for the minor production of metabolites. Moreover, it interacts with various transporters including P-glycoprotein 1 (ABCB1), multiple members of the SLC22 family like SLC22A1, SLC22A2, and SLC22A4 which are responsible for its renal secretion, and organic anion transporters such as SLCO1A2 and SLCO4C1. Levofloxacin is also bound by serum albumin (ALB), impacting its distribution.

## Pharmacogenetics
Pharmacogenetic interactions of levofloxacin are not extensively documented in major databases or literature. However, the involvement of CYP2C9 and transport proteins such as ABCB1 suggests potential genetic variability in pharmacokinetics and dynamics could impact efficacy and safety. Variants in these genes might affect the drug’s metabolism and transport, altering exposure levels, effectiveness, and risk of adverse effects. Specifically, polymorphisms in ABCB1 could influence drug efflux from cells, potentially affecting drug concentrations in target tissues. While concrete pharmacogenetic guidelines for levofloxacin are not established, considering genetic testing may be prudent in cases of unusual responses or adverse effects.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
