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
My drug of interest is pyrazinamide.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
TNF, ABCB1, NAT2, CYP3A4, CYP2C19, CYP2B6, CYP2C9, CYP2A6, CYP1A2, CYP2E1, GSTP1, GSTT1, CYP2F1, CYP2J2, GSTM3, GSTA1, CYP2C8, CYP2A13, NAT1, GSTM1, HLA-B, CYP2C18, GSTM4, CYP2A7, GSTM5, GSTA5, GSTA3, CYP2D7, GSTA4, CYP2S1, MGST2, GSTT2, GSTA2, GSTM2, MGST3


# Known pharmacogenetic associations
In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
NAT2
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Pyrazinamide is a pyrazine derivative that serves as an antitubercular agent. It is indicated for the initial treatment of active tuberculosis, typically used in combination with other antituberculous medications for both adults and children. Pyrazinamide possesses a unique mode of action, targeting the bacteria that cause tuberculosis (TB) and is specifically active against *Mycobacterium tuberculosis*. The drug is well-absorbed from the gastrointestinal tract, undergoes metabolism primarily in the liver, and exerts its bactericidal effects only under slightly acidic conditions. The drug has known side effects such as liver injury, arthralgias, and hypersensitivity reactions.

## Drug Targets, Enzymes, Transporters, and Carriers
Pyrazinamide is prodrug that is converted by the bacterial pyrazinamidase enzyme into its active form, pyrazinoic acid, which targets fatty acid synthetase (FAS) in *M. tuberculosis*. This inhibition interferes with the bacterium's fatty acid synthesis, crucial for its growth and replication. Additionally, pyrazinoic acid disrupts membrane potential and energy production within the bacterial cells, contributing to its antitubercular activity. In humans, pyrazinamide is metabolized by aldehyde oxidase (AOX1) and xanthine dehydrogenase/oxidase (XDH), which are responsible for its hepatic metabolism. There are no specific transporters or carriers noted in the provided data for its transport or distribution.

## Pharmacogenetics
Currently, specific pharmacogenetic data related to pyrazinamide is not extensively detailed. However, considering its metabolism involves enzymes like AOX1 and XDH, genetic variations in these enzymes could potentially influence the drug's pharmacokinetics and side effect profile. For instance, polymorphisms in XDH have been associated with altered activity levels, which might affect drug metabolism and toxicity. Although not directly specified in the drug profile, it implies that individual genetic differences could potentially impact the efficacy and safety of pyrazinamide. Further studies would be necessary to establish more definitive pharmacogenetic associations.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
