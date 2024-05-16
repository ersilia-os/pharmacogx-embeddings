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
My drug of interest is P-aminosalicylic acid.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, NAT2, CYP2C19, CYP2C9, G6PD, HLA-DRB1, CYP2C8, NAT1, HLA-B
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Aminosalicylic acid, also known as Pamisyl, Rexipas, and Rezipas (DrugBank ID: DB00233), is an antitubercular agent primarily used in the treatment of tuberculosis. This agent is often administered in conjunction with isoniazid and functions as a bacteriostatic drug against *Mycobacterium tuberculosis*. Aminosalicylic acid inhibits the bacterium's ability to multiply by disrupting folic acid synthesis and the formation of mycobactin, which is essential for bacterial iron uptake. This drug has a relatively short serum half-life of approximately one hour and is metabolized in the liver. The sodium salt form is generally better tolerated than the free acid form.

## Drug Targets, Enzymes, Transporters, and Carriers
Aminosalicylic acid works through the inhibition of folic acid synthesis by binding more effectively to pteridine synthetase than para-aminobenzoic acid, a precursor in folic acid synthesis pathway. Among its molecular targets are PTGS2 (Prostaglandin G/H synthase 2), CHUK (Inhibitor of nuclear factor kappa-B kinase subunit alpha), ALOX5 (Arachidonate 5-lipoxygenase), and PLA2G2E (Group IIE secretory phospholipase A2). These interactions suggest a mechanism involving the interruption of inflammatory processes, although their direct relevance to the drug's antitubercular action could be limited. Additionally, aminosalicylic acid is metabolized by the enzyme myeloperoxidase (MPO). There is no specific information provided about transporters or carriers.

## Pharmacogenetics
Currently, there is no detailed pharmacogenetic data provided for aminosalicylic acid in the DrugBank entry. However, variations in the MPO gene, which metabolizes the drug, may influence the drug's efficacy and safety profile, though detailed studies or clinical correlates need to be examined to substantiate this hypothesis. Generally, for drugs undergoing hepatic metabolism such as aminosalicylic acid, genetic polymorphisms in liver enzymes might significantly affect drug levels and treatment outcomes. Monitoring and further research into the genetic factors affecting the metabolism and action of aminosalicylic acid could be beneficial in optimizing treatment regimens for tuberculosis, especially in reducing toxicity and preventing resistance.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
