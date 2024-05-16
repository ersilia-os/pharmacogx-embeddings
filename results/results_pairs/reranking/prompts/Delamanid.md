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
My drug of interest is Delamanid.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, CYP3A4, CYP2C19, CYP2C9, CYP3A5, CYP2D6, CYP2D7
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Delamanid is an anti-tuberculosis medication belonging to the nitro-dihydro-imidazooxazole class, specifically designed to inhibit the synthesis of mycolic acids essential for the bacterial cell wall structure. It is primarily indicated for the treatment of pulmonary multidrug-resistant tuberculosis (MDR-TB) and extensively drug-resistant tuberculosis (XDR-TB) in adults. As a prodrug, delamanid requires metabolic activation via the mycobacterial enzyme systems to exert its antimicrobial effects. It demonstrates a relatively focused spectrum of activity, being potent against certain mycobacterial species but not against common Gram-positive or Gram-negative bacteria. Delamanid is absorbed orally with adjusted bioavailability when taken with food, and it undergoes extensive metabolism predominantly via serum albumin and to some extent by cytochrome P450 enzymes, notably CYP3A4.

## Drug Targets, Enzymes, Transporters, and Carriers
Delamanid acts through a complex mechanism involving its transformation by mycobacterial enzymes, specifically the deazaflavin-dependent nitroreductase, to interrupt the synthesis of key mycolic acids, ultimately weakening the bacterial cell wall. Human enzymes also play a role in its metabolism; CYP3A4 contributes to the metabolic activities leading to its detoxification and clearance. It should be noted that delamanid interacts with human proteins such as albumin (ALB) and alpha-1-acid glycoprotein 1 (ORM1), which could implicate these carriers in the drug’s pharmacokinetics, possibly affecting its distribution and half-life.

## Pharmacogenetics
In the pharmacogenetic context, delamanid’s efficacy and safety could be influenced by variations in the genes encoding its metabolic enzymes and target proteins. Given that CYP3A4 is involved in its metabolism, genetic variants of the CYP3A4 gene that alter enzyme activity could potentially affect the pharmacokinetics and dynamics of delamanid, though specific studies or clinical guidelines correlating these genetic variants with delamanid response are not extensively documented. Furthermore, mutations in the mycobacterial genes responsible for the activation of delamanid, such as those affecting the F420 coenzyme system, contribute to resistance mechanisms. This interaction underlines the importance of considering both host and pathogen genetics in the treatment planning for tuberculosis, particularly with regard to resistance development and therapeutic outcomes.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
