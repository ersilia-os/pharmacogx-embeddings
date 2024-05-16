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
My drug of interest is Capreomycin.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, ABCC2, MT-RNR1
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Capreomycin, known by various names including Capastat, Helpomycin, Kapocin, and Lykocin, is a cyclic peptide antibiotic categorized under the aminoglycoside family, although structurally distinct from typical aminoglycosides. It is produced by Streptomyces capreolus. Capreomycin is primarily used in the treatment of tuberculosis (TB) as part of multi-drug regimens especially in cases resistant to first-line treatments. The drug is not absorbed when taken orally and is thus administered parenterally. Its exact pharmacokinetic properties regarding metabolism are unclear, but its pharmacodynamics activity involves bactericidal action likely through protein synthesis inhibition by binding to the 70S ribosomal unit, resulting in fatal abnormal protein production for the bacteria.

## Drug Targets, Enzymes, Transporters, and Carriers
Capreomycin acts on Mycobacterium tuberculosis by targeting the 16S/23S rRNA (cytidine-2'-O)-methyltransferase TlyA enzyme, which is a specific RNA-modifying enzyme that plays a crucial role in the life cycle of the bacteria. By interfering with this target, Capreomycin disrupts the normal synthesis of proteins essential for bacterial survival and proliferation. There are no specific enzymes, transporters, or carriers indicated in the available data directly connected to Capreomycin's action or disposition, emphasizing its rather straightforward mechanism involving direct bacterial interference.

## Pharmacogenetics
There is limited detailed genomic or pharmacogenetic data provided directly related to Capreomycin from the source. Nevertheless, considering its inclusion in the aminoglycoside family, it could be inferred that pharmacogenetic variability in genes involved in drug metabolism and aminoglycoside disposition, such as those coding for ribosomal proteins or transport proteins, might influence the effectiveness or toxicity of the drug. However, more specific studies are needed to establish concrete pharmacogenetic associations. Toxicity profiles like hypokalemia, hypocalcemia, and hypomagnesemia associated with Capreomycin also suggest potential areas where genetic variability in ion transport or homeostasis could impact adverse effects prevalence or severity.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
