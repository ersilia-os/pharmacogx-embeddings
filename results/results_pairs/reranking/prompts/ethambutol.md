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
My drug of interest is ethambutol.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
TNF, ABCB1, NAT2, CYP2C19, CYP2B6, CYP2C9, CYP2A6, CYP2D6, CYP2E1, G6PD, NR1I2, HLA-DRB1, CYP2F1, CYP2J2, GSTM3, GSTA1, CYP2C8, HLA-DQB1, HLA-DQA1, CYP2A13, HLA-DPB1, NAT1, GSTM1, HLA-DPA1, HLA-DRB3, CYP2C18, GSTM4, CYP2A7, HLA-DRB5, GSTM5, GSTA5, GSTA3, CYP2D7, MGST2, GSTM2


# Known pharmacogenetic associations
In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
NAT2
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Ethambutol, also known under brand names such as Etibi and Tibutol, is a bacteriostatic antimicrobial agent specifically indicated for the treatment of pulmonary tuberculosis. This drug is commonly used in a regimen with other anti-tuberculosis medications including isoniazid, rifampin, and pyrazinamide. Having gained FDA approval in 1967, ethambutol’s mechanism primarily revolves around its ability to inhibit arabinosyltransferase enzymes (embA, embB, and embC) in *Mycobacterium tuberculosis*, which leads to impaired cell wall synthesis. The drug shows good oral bioavailability at around 75-80%, with peak serum concentrations reached within two to four hours after administration. Its metabolism involves oxidation by aldehyde dehydrogenase.

## Drug Targets, Enzymes, Transporters, and Carriers
Ethambutol targets arabinosyltransferases in *Mycobacterium tuberculosis*—specifically, embA, embB, and embC. These enzymes are crucial for the polymerization of arabinogalactan, a vital component of the bacterial cell wall. Inhibition of these targets leads to a blockade in cell wall synthesis, impairing bacterial growth and multiplication. Regarding metabolism in humans, ethambutol is metabolized by several cytochrome P450 enzymes, including CYP1A2, CYP2E1, CYP2C19, CYP2D6, CYP2A6, CYP2C9, and CYP3A4. There are no specific transporters or carriers identified for ethambutol affecting its pharmacokinetics notably.

## Pharmacogenetics
Pharmacogenetic aspects of ethambutol primarily involve enzymes responsible for its metabolism, notably CYP1A2. Genetic polymorphisms in this enzyme can influence the pharmacokinetics of ethambutol, as evidenced by variability in the area under the concentration-time curve (AUC). Such genetic variations can affect drug exposure, which may impact both efficacy and toxicity, underscoring the importance of monitoring for side effects, particularly optic neuritis—a serious adverse effect. Although not specifically detailed in the genomic data provided, it is plausible that polymorphisms in other metabolizing enzymes like CYP2E1, CYP2C19, and others might similarly influence individual responses to ethambutol therapy. Given these possibilities, pharmacogenetic testing might inform personalized dosing strategies to optimize therapeutic outcomes and minimize adverse effects.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
