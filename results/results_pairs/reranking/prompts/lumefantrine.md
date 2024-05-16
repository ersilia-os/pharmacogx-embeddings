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
My drug of interest is lumefantrine.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, CYP3A4, CYP2C9, ABCC2, CYP3A5, ZSCAN25, CYP2D6, CYP3A43, ZNF211, ZNF565, ZNF165, ZNF568, CYP3A7, ZNF789, CYP2D7


# Known pharmacogenetic associations
In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
CYP3A4, ABCC2, CYP3A5, ZSCAN25
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Lumefantrine is an antimalarial drug primarily used in combination with artemether for treating acute uncomplicated malaria. It is part of the artemisinin combination therapy (ACT), a recommended treatment for *Plasmodium falciparum* malaria, especially in regions where resistance to chloroquine is a concern. Lumefantrine inhibits the formation of β-hematin, thereby disrupting nucleic acid and protein synthesis in the malaria parasite, although its exact mechanism of action remains not fully understood. Lumefantrine has a long half-life, which supports its role in clearing residual parasites after the rapid action of artemether. Its absorption is significantly enhanced by food, and it is extensively metabolized in the liver by CYP3A4, with desbutyl-lumefantrine being the major metabolite.

## Drug Targets, Enzymes, Transporters, and Carriers
Lumefantrine lacks specific protein targets according to the provided data, focusing instead on disrupting the metabolic pathways of the malaria parasite indirectly. Its metabolism is largely handled by liver enzymes where Cytochrome P450 3A4 (CYP3A4) plays a primary role, substantiating its significant influence on the drug’s pharmacokinetic profile. Cytochrome P450 2D6 (CYP2D6) is also listed as involved in its metabolic process, which may imply a secondary pathway or minor role. No specific transporters or carriers are documented in relation to lumefantrine transport within the human body based on the provided data.

## Pharmacogenetics
Focusing on pharmacogenetics, the primary enzymes involved in the metabolism of lumefantrine indicate potential variability in drug response based on genetic differences. Variants within the CYP3A4 gene can lead to differences in metabolism speed, affecting both the efficacy and toxicity of lumefantrine. For instance, some individuals with specific CYP3A4 alleles may metabolize lumefantrine more slowly, leading to increased exposure and potential toxicity, or more rapidly, possibly reducing drug efficacy. Similarly, although CYP2D6 is less central, genetic variations in this enzyme could potentially alter drug levels and effects. No direct genomic data link was provided in the summary, and thus specific genotype-related dosage recommendations are not available. However, these enzymatic pathways suggest that genetic testing could be beneficial in tailoring treatments for optimal efficacy and safety.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
