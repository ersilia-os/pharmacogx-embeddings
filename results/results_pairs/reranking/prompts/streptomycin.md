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
My drug of interest is streptomycin.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCC2, HLA-C, MT-RNR1, MT-ND1, HLA-G, HLA-E, HLA-B, HLA-A, BRINP3, NELL1
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Streptomycin, a seminal aminoglycoside antibiotic discovered in the 1940s from _Streptomyces griseus_, played a crucial role in the treatment of tuberculosis before the rise of antibiotic resistance and toxicity concerns. It is now primarily used as a second-line agent or in combination therapies for multi-drug resistant tuberculosis and certain other infections caused by susceptible strains of aerobic bacteria. Examples include infections caused by _Yersinia pestis_, _Francisella tularensis_, _Brucella_, and _Calymmatobacterium granulomatis_. Due to its poor oral absorption, streptomycin is administered parenterally, achieving peak serum concentration within one hour of intramuscular injection. The drug's notable toxicities include nephrotoxicity and ototoxicity, necessitating monitoring for early signs of hearing loss and kidney dysfunction.

## Drug Targets, Enzymes, Transporters, and Carriers
Streptomycin exerts its antibacterial effect primarily by binding to the 30S ribosomal subunit of bacteria, specifically targeting the rpsL gene product, the 30S ribosomal protein S12 in _Escherichia coli_. This interaction disrupts bacterial protein synthesis by causing misreading of mRNA, thus inhibiting bacterial growth and leading to cell death. The drug's mechanism encompasses initial electrostatic binding to bacterial cell membranes, followed by penetration and interference with the ribosome's normal function. Notably, streptomycin also interacts with human proteins, such as binding to the PADI4 (Protein-arginine deiminase type-4) in humans. The drug does not interact with any known metabolic enzymes, transporters, or carriers, which simplifies its pharmacokinetic profile but also limits modulation of its effects via these routes.

## Pharmacogenetics
While specific pharmacogenetic data for streptomycin is limited, the general interactions of aminoglycosides with genetic elements suggest considerations for streptomycin as well. Variability in drug response and toxicity, particularly ototoxicity, might be influenced by genetic variants in mitochondrial DNA or genes involved in the sensory function of the ear. Aminoglycosides are known to induce ototoxicity by generating free radicals within the inner ear's sensory cells, and variations in genes responsible for antioxidant defense could influence individual susceptibility to this adverse effect. Additionally, no significant associations with specific human gene polymorphisms have been conclusively linked to variations in streptomycin metabolism or efficacy, but research in this area could potentially improve the understanding of differential drug responses and help tailor antibiotic therapy more effectively in the future.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
