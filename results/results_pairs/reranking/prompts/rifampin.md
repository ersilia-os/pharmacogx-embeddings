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
My drug of interest is rifampin.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
SLCO1B1, SLCO1B3, TNF, ABCB1, NAT2, CYP3A4, CYP2C19, CYP2B6, CYP2C9, CYP2A6, ABCC2, CYP3A5, XPO1, CYP2D6, CYP2E1, GSTP1, GSTT1, FMO1, VDR, NR1I2, SLCO1C1, CYP2F1, SLCO1A2, CYP4A11, BACH1, CYP2J2, CYP4F2, ADORA2A-AS1, GSTM3, GSTA1, CYP2C8, CYP27B1, CYP2A13, CYP24A1, NR1I3, FMO5, NAT1, CYP2R1, GSTM1, CUX2, RIPOR2, AGBL4, NOS2, MAFK, CYP3A7, BCL11A, CYP2C18, FMO4, CYP4X1, DUX1, GSTM4, CYP2A7, MROH2A, GSTM5, GSTA5, HOXC13, FMO6P, GSTA3, GSTK1, CYP2D7, GSTA4, MGST1, CYP2S1, GSTT2, GSTA2, GSTM2, SLCO6A1, CYP4F8


# Known pharmacogenetic associations
In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
SLCO1B1, NAT2, GSTT1, VDR, NR1I2, CYP27B1, GSTM1
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Rifampicin, also known as Rifadine, Rifaldin, Rifoldin, Rimactan, Rimactane, Rofact, and Tubocin, is a semisynthetic antibiotic derived from Streptomyces mediterranei. It is primarily used for treating various forms of tuberculosis, including those resistant to other treatments. As a potent bactericidal agent, rifampicin inhibits DNA-dependent RNA polymerase in bacterial cells, leading to suppression of RNA synthesis and cell death. This antibiotic has a broad antibacterial spectrum, but its use is primarily focused on mycobacterial infections because it quickly leads to resistance if used alone. Rifampicin is well absorbed from the gastrointestinal tract, highly distributed across the body, including the CSF, metabolized mainly in the liver by deacetylation, and excreted through bile.

## Drug Targets, Enzymes, Transporters, and Carriers
Rifampicin targets the bacterial DNA-dependent RNA polymerase subunit beta (rpoB), crucial for RNA synthesis. It also interacts with the nuclear receptor subfamily 1, group I, member 2 (NR1I2) in humans, which plays a role in regulating genes involved in drug metabolism and transport. The metabolism of rifampicin involves several cytochrome P450 enzymes, including CYP1A2, CYP2A6, CYP2C8, CYP2C9, CYP2C19, CYP2B6, CYP2E1, CYP3A4, CYP3A5, CYP3A43, CYP3A7, and also UDP-glucuronosyltransferases UGT1A1 and UGT1A9. It influences various transporters such as ABCB1, ABCC1-3, ABCC5, ABCB11, SLCO1B1, SLCO1B3, SLCO1A2, SLCO2B1, SLC22A6, SLC22A7, and SLC22A8, which may affect its disposition and the disposal of other concurrently administered drugs. Carriers like ALB (serum albumin) and ORM2 (alpha1-acid glycoprotein) are involved in its systemic circulation.

## Pharmacogenetics
Rifampicin pharmacogenetics reveals significant interactions, particularly involving enzymes responsible for drug metabolism. The induction of CYP3A4 by rifampicin is well-documented, leading to reduced plasma concentrations of co-administered drugs metabolized by this enzyme, such as protease inhibitors and non-nucleoside reverse transcriptase inhibitors. Moreover, the genetic variances in CYP2B6, CYP2C8, CYP2C9, CYP2C19, and CYP2E1 can alter rifampicin's efficacy and safety, impacting individual responses significantly. Polymorphisms in ABCB1 and other drug transporters also potentially modify the pharmacokinetics and pharmacodynamics of rifampicin, affecting drug absorption and resistance profiles. Genetic testing and personalized medicine approaches may optimize rifampicin therapy by tailoring dosages to achieve maximal efficacy with minimal adverse effects, particularly in multi-drug resistant tuberculosis treatments.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:


## Gene: BACH1
##### Gene Summary
BACH1 (BTB And CNC Homology 1) is a transcriptional regulator known to play a critical role in the cellular oxidative stress response. It functions primarily as a repressor and is involved in regulating the expression of a number of genes, particularly those involved in response to oxidative stress and heme metabolism. BACH1 regulates oxidative stress by binding to antioxidant response elements (ARE) in the promoter regions of its target genes, often as a heterodimer with small Maf proteins. Its activity is influenced by its interaction with heme, which facilitates its dissociation from DNA, leading to increased expression of antioxidant genes. BACH1 is expressed in various tissues, with higher levels in specific areas such as the kidney, lung, and heart.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
BACH1 is linked to several cellular pathways associated with oxidative stress and inflammatory responses, which are integral to various physiological and pathological processes. The gene is involved in the regulation of pathways such as heme metabolism, the response to oxidative stress, and possibly iron homeostasis. Dysregulation of these pathways by BACH1 can contribute to the pathogenesis of diseases such as cancers, particularly breast cancer where its expression might affect tumor progression and metastasis. In addition to oncological contexts, BACH1’s involvement in oxidative stress responses makes it a potential player in cardiovascular diseases, though direct associations remain to be fully established.

##### Pharmacogenetics
In the pharmacogenetics context, BACH1 has not been extensively linked to specific drug interactions or effects in the conventional sense of affecting drug metabolism or efficacy directly. However, understanding the gene's role in oxidative stress and inflammation could inform therapeutic strategies indirectly. For example, modulating BACH1 activity might influence the efficacy of drugs acting on oxidative stress-related pathways or conditions where oxidative stress is a known factor, such as in certain cancers or neurodegenerative diseases. Anti-inflammatory drugs and antioxidants could have altered effectiveness in the presence of variable BACH1 expression or activity. Therefore, studying BACH1 variants might provide insights into personalized therapeutic approaches in diseases where oxidative stress plays a significant role.


## Gene: CYP2R1
##### Gene Summary
CYP2R1 (Cytochrome P450 Family 2 Subfamily R Member 1) is primarily known for its role in the hydroxylation of vitamin D to form 25-hydroxyvitamin D, the major circulating form of vitamin D, which is critical for subsequent activation to the hormonally active form, calcitriol. Expressed predominantly in the liver, CYP2R1 is a part of the cytochrome P450 superfamily, enzymes that are often involved in the metabolism of drugs and synthesis of cholesterol, steroids, and other lipids.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
CYP2R1 is intimately linked to vitamin D metabolism, with potential implications in diseases associated with vitamin D deficiency, such as rickets, osteoporosis, and certain immune diseases. Mutations in this gene can lead to vitamin D-dependent rickets type 1B, a rare autosomal recessive disorder characterized by the early onset of rickets, muscle weakness, and growth retardation. Despite its primary role in vitamin D metabolism, CYP2R1 does not have extensive associations with a wide range of drugs akin to other CYP enzymes. Its influence remains largely confined to its pivotal enzymatic role within the vitamin D pathway, including the conversion of vitamin D to its more active form in the liver.

##### Pharmacogenetics
Pharmacogenetic associations of CYP2R1 primarily concern its impact on vitamin D levels in the body, which in turn can influence the efficacy and safety of vitamin D supplementation and metabolism. Genetic variants can affect individual responses to vitamin D intake and thus susceptibility to diseases related to vitamin D deficiency. Differential activity of CYP2R1, determined by specific gene variants, could potentially modify vitamin D processing and thereby influence conditions like bone health and immune function. Given its role in this pathway, pharmacogenetic testing might guide personalized vitamin D supplementation strategies. However, direct associations with traditional pharmacological agents are relatively limited compared to other cytochrome P450 enzymes.
