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
My drug of interest is mefloquine.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, CYP3A4, CYP2C19, CYP2D6, G6PD, CYP2D7
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Mefloquine, sold under various brand names such as Lariam, Eloquine, and Mefliam, is an antimalarial medication used primarily for the prevention and treatment of malaria. The drug is indicated for use against Plasmodium vivax and Plasmodium falciparum, including strains resistant to chloroquine. Mefloquine was developed by the Walter Reed Army Institute of Research in the mid-20th century and was FDA-approved in 1989. It is a blood schizonticide, meaning it acts on the blood stages of the malaria parasite lifecycle. Mefloquine is known for its neuropsychiatric side effects, which have led to controversy regarding its use. The drug is absorbed well in the gastrointestinal tract with increased bioavailability when taken with food. It reaches peak concentration in the blood between 6 to 24 hours after intake. Mefloquine is extensively metabolized in the liver, predominantly by the enzyme CYP3A4, and its metabolites include an inactive carboxylic acid and a minor alcohol metabolite.

## Drug Targets, Enzymes, Transporters, and Carriers
Mefloquine's primary target in the Plasmodium parasite is suggested to be the 80S ribosome, inhibiting protein synthesis, which contributes to its schizonticidal effects. The drug's human pharmacokinetic profile involves several key enzymes and a transporter. It is metabolized primarily by cytochrome P450 3A4 (CYP3A4), with two known metabolites. Additionally, enzymes such as Cytochrome P450 19A1 (CYP19A1), Acetylcholinesterase (ACHE), and Cholinesterase (BCHE) are also involved in its metabolism to varying extents. Mefloquine is also a substrate for the transporter P-glycoprotein 1 (ABCB1), which plays a role in its cellular efflux and possibly affects its distribution and elimination.

## Pharmacogenetics
The pharmacogenetics of mefloquine are not extensively documented in the provided data, but inferences can be drawn from its metabolism and transporter interactions. Variants in the CYP3A4 gene, which is responsible for the metabolism of mefloquine, could potentially influence the drug's plasma levels and hence its efficacy and toxicity. For instance, individuals with certain genetic polymorphisms that result in decreased CYP3A4 activity might experience higher concentrations of mefloquine, increasing the risk of its side effects. Similarly, genetic variations in ABCB1 might affect the transport and distribution of mefloquine in the body, influencing both the drug’s effectiveness and toxicity profile. These pharmacogenetic factors are crucial for personalizing mefloquine dosages to enhance therapeutic outcomes and minimize adverse effects, although specific guidelines based on genetic testing are not yet standardized.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
