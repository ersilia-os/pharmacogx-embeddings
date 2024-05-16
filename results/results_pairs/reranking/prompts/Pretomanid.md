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
My drug of interest is Pretomanid.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCB1, CYP3A4, CYP2C19, CYP2B6, CYP2C9, CYP3A5, CYP2D6, CYP2E1, CYP2J2, CYP2C8, CYP2C18
# Auxiliary information about the drug
Below is some auxiliary information about the drug of interest:
## Drug Summary
Pretomanid is an antimycobacterial drug used in combination with bedaquiline and linezolid to treat adults with drug-resistant pulmonary tuberculosis (TB), specifically resistance to agents like isoniazid and rifampin, as well as in cases where patients are intolerant or unresponsive to standard therapies. This drug regimen shortens the duration and enhances the success rate of treatment regimes that traditionally may take longer and prove ineffective. Pretomanid is absorbed in the gastrointestinal tract with increased bioavailability when taken with a high-fat meal. The metabolism of pretomanid involves both reductive and oxidative pathways, with CYP3A4 being responsible for a significant portion of its oxidative metabolism. It acts as a prodrug, activated primarily by a nitroreductase enzyme.

## Drug Targets, Enzymes, Transporters, and Carriers
Pretomanid targets primarily bacterial proteins related to the pathophysiology of Mycobacterium tuberculosis. Important targets include the Fatty acid synthetase (fas), which is crucial for bacterial lipid synthesis, and nucleoid-associated protein Lsr2. It also affects the cyd operon, which is involved in the bacteria’s respiratory process. The nitroreductase enzyme Ddn metabolically activates pretomanid, which becomes bactericidal under anaerobic conditions by inducing nitric oxide production. Human transporter proteins affected include SLC22A8, which may play a role in the drug’s cellular uptake and distribution. No specific carriers are documented for pretomanid.

## Pharmacogenetics
Pretomanid’s effectiveness and safety could be influenced by genetic variations in the enzymes and transporters it interacts with. As CYP3A4 contributes to its metabolism, genetic polymorphisms in this enzyme that alter enzyme activity could influence pretomanid’s pharmacokinetics and potential drug-drug interactions, especially with other medications metabolized through the same pathway. Such variations might affect drug levels, efficacy, and safety profiles, including risks for hepatotoxicity and QT prolongation noted with its use. However, specific pharmacogenetic markers directly linked to pretomanid have not been well-established in published literature, indicating an area where additional research could be beneficial for optimizing treatment with pretomanid and reducing adverse effects.
# Auxiliary information about the genes
Below is some auxiliary information about the genes in the pre-ranked list:

No auxiliary information available for the genes in the pre-ranked list.
