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
My drug of interest is artesunate.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, CYP3A4, CYP2C19, CYP2B6, CYP2C9, CYP2A6, CYP3A5, G6PD, IKBKG, CYP2C8, CYP3A43, CYP3A7, CYP2A7, CYP2D7
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Artesunate is an antimalarial drug belonging to the artemisinin class, specifically used as the first-line treatment for severe malaria in both adults and children. It was developed from artemisinin to improve hydrophilicity and approved by the FDA on May 26, 2020. Artesunate works through its metabolism to dihydroartemisinin (DHA), which engages in free-radical-mediated inhibition of the Plasmodium parasite's protein and nucleic acid synthesis across all erythrocytic stages. This drug showcases a short half-life and acts quickly with a moderate therapeutic index. Besides its antimalarial action, artesunate may produce side effects such as post-treatment hemolytic anemia and hypersensitivity reactions. Its pharmacokinetic profile reveals rapid absorption and conversion to DHA, which achieves peak plasma concentrations shortly after administration.

## Drug Targets, Enzymes, Transporters, and Carriers
The primary action of artesunate and its active metabolite DHA involves the malaria protein EXP-1 from Plasmodium falciparum, influencing calcium adenosine triphosphatase and other parasitic proteins. Metabolism of artesunate is predominantly facilitated by plasma esterases and further glucuronidation by the enzymes UGT1A9 and UGT2B7. Minor contributions from CYP2A6 have been reported. Regarding transport, artesunate and its metabolites interact with multiple transporters; P-glycoprotein (ABCB1), ABCG2, and solute carrier proteins such as SLCO1B1 and SLC22A8, which might affect drug distribution and excretion. Serum albumin (ALB) serves as a carrier for the drug, potentially influencing its pharmacokinetic profile.

## Pharmacogenetics
The pharmacogenetic profile of artesunate hinges on its metabolism and transport. Variability in genes such as UGT1A9, UGT2B7, and CYP2A6 could influence the drug's pharmacokinetic and pharmacodynamic properties, consequently affecting efficacy and safety. For instance, genetic variants in UGT enzymes might alter the rate of DHA glucuronidation, impacting drug levels and response. Similarly, polymorphisms in ABCB1 and other transporter genes may modify the drug’s absorption and elimination, potentially leading to variations in drug exposure among individuals. Despite this, specific pharmacogenetic guidelines for artesunate dosing based on these genetic factors are not currently established, but they underscore the importance of further research in this area to optimize malaria treatment efficacy.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
