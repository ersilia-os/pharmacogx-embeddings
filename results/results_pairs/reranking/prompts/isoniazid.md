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
My drug of interest is isoniazid.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
SLCO1B1, SLCO1B3, TNF, ABCB1, NAT2, EPHX1, CYP3A4, CYP2C19, CYP2B6, CYP2C9, CYP2A6, XPO1, CYP2D6, CYP2E1, GCLC, GSTP1, GSTT1, FMO1, VDR, NR1I2, CYP2F1, SLCO1A2, CYP4A11, BACH1, CYP2J2, CYP4F2, CYP4B1, GSTM3, GSTA1, CYP2C8, HLA-C, ASTN2, CYP2A13, HLA-G, NR1I3, FMO5, NAT1, GSTM1, HLA-E, NOS2, MAFK, HLA-B, HLA-A, CYP2C18, FMO4, DUX1, GSTM4, CYP2A7, GSTM5, GSTA5, FMO6P, GSTA3, GSTO1, CYP4F12, GSTK1, CYP2D7, GSTA4, MGST1, GSS, CYP2S1, MGST2, GSTT2, GSTO2, GSTA2, GSTM2, CYP4F8, CYP4F3, MGST3


# Known pharmacogenetic associations
In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
SLCO1B1, NAT2, GSTT1, NR1I2, GSTM1
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:


## Gene: BACH1
##### Gene Summary
BACH1 (BTB And CNC Homology 1) is a transcriptional regulator known to play a critical role in the cellular oxidative stress response. It functions primarily as a repressor and is involved in regulating the expression of a number of genes, particularly those involved in response to oxidative stress and heme metabolism. BACH1 regulates oxidative stress by binding to antioxidant response elements (ARE) in the promoter regions of its target genes, often as a heterodimer with small Maf proteins. Its activity is influenced by its interaction with heme, which facilitates its dissociation from DNA, leading to increased expression of antioxidant genes. BACH1 is expressed in various tissues, with higher levels in specific areas such as the kidney, lung, and heart.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
BACH1 is linked to several cellular pathways associated with oxidative stress and inflammatory responses, which are integral to various physiological and pathological processes. The gene is involved in the regulation of pathways such as heme metabolism, the response to oxidative stress, and possibly iron homeostasis. Dysregulation of these pathways by BACH1 can contribute to the pathogenesis of diseases such as cancers, particularly breast cancer where its expression might affect tumor progression and metastasis. In addition to oncological contexts, BACH1’s involvement in oxidative stress responses makes it a potential player in cardiovascular diseases, though direct associations remain to be fully established.

##### Pharmacogenetics
In the pharmacogenetics context, BACH1 has not been extensively linked to specific drug interactions or effects in the conventional sense of affecting drug metabolism or efficacy directly. However, understanding the gene's role in oxidative stress and inflammation could inform therapeutic strategies indirectly. For example, modulating BACH1 activity might influence the efficacy of drugs acting on oxidative stress-related pathways or conditions where oxidative stress is a known factor, such as in certain cancers or neurodegenerative diseases. Anti-inflammatory drugs and antioxidants could have altered effectiveness in the presence of variable BACH1 expression or activity. Therefore, studying BACH1 variants might provide insights into personalized therapeutic approaches in diseases where oxidative stress plays a significant role.
