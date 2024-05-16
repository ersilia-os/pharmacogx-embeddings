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
My drug of interest is quinine.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
CYP3A4, CYP2C9, CYP3A5, CYP2D6, G6PD, KCNH2, CYP2A13, CYP3A43, KCNE1, CYP3A7, CYP2D7
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Quinine is an alkaloid derived from the bark of the cinchona tree, historically significant as an antimalarial agent. Apart from its primary use in treating malaria, especially chloroquine-resistant Plasmodium falciparum infections, it is also employed to relieve nocturnal leg cramps and myotonia congenita due to its muscle membrane stabilizing activity. This drug has notable antipyretic and analgesic properties and has found its way into common cold preparations as well. Quinine is administered parenterally and exhibits an absorption rate between 76% and 88%. It undergoes extensive hepatic metabolism, predominantly mediated by several cytochrome P450 enzymes, with over 80% being metabolized in the liver.

## Drug Targets, Enzymes, Transporters, and Carriers
Quinine targets include glycoprotein IX (GP9) and the intermediate conductance calcium-activated potassium channel protein 4 (KCNN4), impacting platelet function and potassium ion transport, respectively. The drug is metabolized primarily by hepatic cytochrome P450 enzymes including CYP3A4, CYP3A5, CYP1A1, CYP2D6, CYP1A2, CYP2C8, CYP2C9, CYP2C19, CYP2E1, and CYP3A7. Transport mechanisms involve several solute carriers such as SLC22A2, SLC22A1, SLC22A5, SLCO1A2, SLC22A4, and SLCO1B1, as well as the efflux transporter ABCB1 (P-glycoprotein 1). There is no indication of specific carrier proteins involved in its pharmacokinetics.

## Pharmacogenetics
The pharmacogenetics of quinine is largely influenced by polymorphisms in the CYP enzymes that metabolize it. Variants in CYP3A4 and CYP3A5, for instance, can alter the metabolism of quinine, potentially affecting both efficacy and toxicity. Additionally, the drug-induced thrombocytopenia associated with quinine is mediated through the immune generation of antibodies against platelet glycoproteins, namely GPIb-IX and GPIIb-IIIa. Genetic predispositions affecting the immune response to quinine or the baseline levels of these glycoproteins might influence susceptibility to adverse effects. The pharmacokinetics may also vary across individuals with different polymorphic forms of the involved solute carriers and P-glycoprotein, impacting drug absorption and elimination.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
