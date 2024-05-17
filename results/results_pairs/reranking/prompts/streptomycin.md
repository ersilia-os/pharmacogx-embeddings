# Main instructions
- You are a biomedicine expert. You help me identify pharmacogenetic drug-gene pairs. Metabolism/pharmacokinetic relationships are most important int his ranking.
- The user will give you a drug of interest. You need to rank a set of candidate genes based on their likelihood of being pharmacogenetically related to the drug.
- The user will provide a pre-ranked list of genes. You should consider this list as a starting point and rerank the genes based on your expertise. Feel free to make significant changes to the ranking.
- Do not include genes that are not in the pre-ranked list. Only rerank the genes that are already in the list.
- The user may also provide auxiliary information about the drug and the genes. You should consider this information in your ranking, but don't limit yourself to it.
- Do not focus only on known associations. Use your expertise to infer new pharmacogenetic relationships. Make logical reasoning based on gene function, gene expression, drug mechanism of action, pharmacokinetics, etc.
- For example, consider known pharmacogenetic relationships of similar drugs and similar genes in your reasoning.
- You should return a ranked list of genes in JSON format. The list should be sorted in descending order of likelihood. Give me only the top 10 genes.
- For each gene, offer an explanation of why you think there is a pharmacogenetic relationship with the given drug. This explanation should be between 200 and 500 words. Be as detailed as possible.
- The explanation is important. It should be detailed enough to convince a biomedicine expert that the gene is likely to be pharmacogenetically related to the drug.
- Only return a JSON string. Do not make any other comment. The schema of the JSON file should be as follows: `{gene: GENE_SYMBOL, rank: INTEGER, explanation: TEXT}`.

# Drug of interest
My drug of interest is streptomycin.


# Pre-ranked list of genes
These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
ABCC2, MT-RNR1, HLA-A, ABCB1, ABCG2, ABCC4, ABCC3, CDA, BRINP3, HLA-B, NELL1, MT-ND1, PADI4, SLC28A3, HLA-E, HLA-C, VEGFC, HLA-G, SLCO1B1, TPMT, ABCB4, HLA-DRB1, SLC28A1, CTPS1, HFE, HCP5, RRM1, ADORA2A-AS1, C18orf56, C5orf56, HLA-DQB1, DCK, SLCO1A2, HLA-DRA, RUNDC3B, G6PD, MLN, DCTD, ABCC5, IGF2-AS, SLC22A11, TAPBP, GBP6, HLA-DPB1, ADA, SLC29A2, LILRB5, HLA-DRB5, ABCC11, SLC28A2
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


## Gene: ABCC2
##### Gene Summary
ABCC2, also known as ATP Binding Cassette Subfamily C Member 2, encodes the multidrug resistance-associated protein 2 (MRP2). This protein is part of the ATP-binding cassette (ABC) transporter superfamily that plays a critical role in the transport of a variety of exogenous and endogenous substrates including bile acids, glucuronides, and other conjugates across cellular membranes. Located predominantly in the liver, kidneys, and intestine, MRP2 influences the excretion of these substances into bile and urine. Its activity is essential for detoxification processes and the protection of the organism from potentially harmful substances.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
MRP2 is associated with several key health conditions predominantly due to its role in substance transport and detoxification. Dysfunction or reduced expression of this transporter can lead to Dubin-Johnson syndrome, a rare inherited disorder characterized by conjugated hyperbilirubinemia. With respect to cancer pharmacology, MRP2 is studied for its role in contributing to chemotherapy resistance by actively effluxing anticancer drugs out of cells. In metabolic pathways, MRP2 is involved in the transport of bilirubin glucuronides and bile acids, which are critical in lipid digestion and vitamin absorption. The transporter's function influences the pharmacokinetics and toxicity profiles of many drugs by affecting their absorption and excretion.

##### Pharmacogenetics
In pharmacogenetics, variations in the ABCC2 gene significantly affect the disposition and efficacy of various drugs. Polymorphisms in this gene have been associated with altered drug pharmacokinetics for antiepileptics, HIV protease inhibitors, and methotrexate among others. Specific alleles like c.1249G>A (rs2273697) and c.3972C>T (rs3740066) have been linked to differences in MRP2 function, impacting the transporter's ability to efflux methotrexate, leading to variability in toxicity and therapeutic response in cancer treatment. Additionally, genetic variants in ABCC2 may modify the response to antiviral drugs, influencing treatment outcomes in infections such as HIV. Such pharmacogenomic insights are crucial for tailoring medical treatments and optimizing therapeutic strategies based on patients' genetic profiles.


## Gene: MT-RNR1
##### Gene Summary
MT-RNR1, also known as mitochondrial ribosomal RNA 12S, encodes the mitochondrial 12S ribosomal RNA which is a component of the small ribosomal subunit. The MT-RNR1 gene is situated within mitochondrial DNA and plays a crucial role in the translation of mitochondrial-encoded proteins, which are essential for oxidative phosphorylation and energy production in cells. Beyond its fundamental role in protein synthesis, variants in this gene have been linked to a variety of mitochondrial dysfunctions given its critical involvement in cellular energetics and metabolism.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
MT-RNR1 is associated with several phenotypic outcomes and diseases, primarily linked to sensorineural hearing loss and mitochondrial dysfunction. Notably, alterations in this gene can lead to Non-Syndromic Hearing Loss and Deafness, Mitochondrial (NSHLDM), pointing to its vital role in cochlear function and inner ear cell metabolism. There is also evidence linking MT-RNR1 to certain cases of aminoglycoside-induced ototoxicity, underlining a gene-drug interaction that can exacerbate the risk of hearing loss. The primary biological pathway involving MT-RNR1 is the mitochondrial translational pathway, crucial for the synthesis of proteins that constitute the mitochondrial respiratory chain complexes.

##### Pharmacogenetics
In the realm of pharmacogenetics, MT-RNR1 holds significant importance due to its connection with aminoglycoside antibiotics, such as gentamicin and tobramycin. Specifically, certain variants in the MT-RNR1 gene can predispose individuals to aminoglycoside-induced ototoxicity, a severe side effect resulting in permanent hearing loss. This association particularly concerns the m.1555A>G mutation which greatly increases susceptibility to this side effect when patients with the mutation are treated with these antibiotics. As such, genetic screening for MT-RNR1 mutations is highly recommended before administering aminoglycosides to mitigate the risk of irreversible ototoxic effects, illustrating a critical pharmacogenetic consideration in clinical settings to enhance personalized medicine approaches.


## Gene: HLA-A
##### Gene Summary
HLA-A (Human Leukocyte Antigen A) is part of the Major Histocompatibility Complex (MHC) class I molecules, which are critical for the immune system to recognize foreign molecules. Located on chromosome 6, HLA-A plays a crucial role in the presentation of peptide antigens to immune cells, particularly T cells. The gene is highly polymorphic, which enables a broad range of antigen presentations, supporting the immune system's ability to recognize diverse pathogens. HLA-A is expressed ubiquitously on almost all nucleated cells and is fundamental in initiating immune responses and in disease susceptibility.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-A is implicated in a variety of drugs' efficacy and adverse reactions, along with susceptibility to numerous diseases. Specifically, it is involved in the pathogenesis of autoimmune diseases, infectious diseases, and cancer. The phenotypic effects of variations in HLA-A are diverse, impacting both disease progression and the outcome of drug treatments. In terms of pathways, HLA-A is a critical component of the antigen processing and presentation pathway, which is pivotal for the immune system's response to pathogens and tumor cells.

##### Pharmacogenetics
The pharmacogenetics of HLA-A is particularly relevant in the context of drug hypersensitivity reactions. For instance, the HLA-A*31:01 allele has been strongly associated with the development of carbamazepine-induced cutaneous adverse drug reactions. Similarly, HLA-A*02:01 is linked to an increased risk of severe cutaneous adverse reactions when using allopurinol. Additionally, some alleles of HLA-A are implicated in the response to treatments in infectious diseases like HIV, influencing the effectiveness of antiretroviral therapy. Given the critical role HLA-A plays in the immune system, its alleles are continuously studied to improve the safety and efficacy of medications through tailored therapeutic strategies based on genetic profiles.


## Gene: ABCB1
##### Gene Summary
ABCB1, also known as P-glycoprotein or MDR1 (multidrug resistance protein 1), is a crucial member of the ATP-binding cassette (ABC) transporter family. This protein functions as an ATP-dependent efflux pump, which plays a significant role in the transport of a wide array of substances across extra- and intra-cellular membranes. ABCB1 is widely expressed in tissue barriers with excretory or protective functions, including the intestinal epithelium, the blood-brain barrier, and the plasma membranes of hepatocytes and kidney tubules. Its primary biological role is to protect cells by pumping out toxic substances and xenobiotics, contributing to the pharmacokinetics of many drugs.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCB1 is implicated in multiple pharmacological and pathological contexts due to its broad substrate specificity. It influences the absorption, distribution, metabolism, and excretion (ADME) of many drugs including chemotherapeutics, antiepileptics, HIV protease inhibitors, and immunosuppressants. Pathologically, the overexpression of ABCB1 is linked to the development of multidrug resistance in cancer cells, a major hurdle in effective cancer chemotherapy. This gene has also been associated with various phenotypes affecting drug pharmacokinetics and patient responses to medication, thus impacting therapeutic outcomes.

##### Pharmacogenetics
The pharmacogenetics of ABCB1 has been extensively studied, and variations in this gene can significantly affect an individual’s response to a variety of drugs. Notable drugs influenced by ABCB1 polymorphisms include the immunosuppressant tacrolimus, chemotherapeutic agents such as vinblastine and doxorubicin, and cardiovascular drugs like digoxin. For example, certain variants in ABCB1 may alter drug disposition, affect blood and brain concentrations, and modulate adverse effects or therapeutic efficacy. This has notable clinical implications, especially in determining dosing regimes for drugs with narrow therapeutic indices to minimize toxicity while maximizing therapeutic effects, particularly in cancer and transplant medicine. Understanding ABCB1 genotypes is increasingly factored into personalized medicine approaches to optimize individual patient care.


## Gene: ABCG2
##### Gene Summary
ABCG2, known as ATP Binding Cassette Subfamily G Member 2, is a transporter protein that plays a crucial role in multidrug resistance in cancer treatment. It is part of the ATP-binding cassette (ABC) superfamily, which transport various molecules across extra- and intracellular membranes. ABCG2 is expressed in various tissues, prominently in the placenta, intestine, and brain, and it functions primarily as an efflux pump, transferring substrates out of cells. This activity helps in the regulation of xenobiotic transport in gut, as well as the blood-brain and blood-testis barriers.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCG2 is implicated in influencing the pharmacokinetics of a wide array of drugs due to its role in effluxing drugs out of cells. Diseases associated with ABCG2 include gout, as mutations in this gene affect urate excretion, leading to hyperuricemia. In cancer, ABCG2 contributes to chemotherapy resistance by pumping anticancer drugs out of cells, making them less effective. The gene is involved in various signaling pathways, including those related to drug transport and metabolism, highlighting its importance in modulating drug bioavailability and disposition.

##### Pharmacogenetics
In pharmacogenetics, ABCG2 has been studied for its significant impact on the absorption, distribution, and elimination of many drugs. Notably, variants of ABCG2, particularly the Q141K variant, have been associated with altered drug response and adverse drug reactions. Drugs affected include certain chemotherapy agents like irinotecan and topotecan, tyrosine kinase inhibitors such as vandetanib, and antiretroviral drugs. For example, the Q141K variant has been linked to increased plasma levels of rosuvastatin, necessitating dose adjustments. Understanding ABCG2 variants helps in personalizing treatment regimens to enhance efficacy and reduce toxicity, especially in cancer chemotherapy.


## Gene: ABCC4
##### Gene Summary
ABCC4, also known as Multidrug Resistance-Associated Protein 4 (MRP4), is a member of the ATP-binding cassette (ABC) transporter family. These transporters play a vital role in the movement of substrates across cellular membranes, using ATP hydrolysis for energy. ABCC4 primarily functions in the efflux of a variety of physiological substrates out of cells, including cyclic nucleotides, uric acid, and several other organic anions. It is expressed in a range of tissues, prominently in the kidneys, liver, and placenta, but also found in the brain, heart, and lungs, where it influences toxin secretion, drug excretion, and tissue protection.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCC4 is implicated in numerous physiological roles and pathological conditions, primarily due to its function in drug transport and resistance. Its overexpression in cancer cells can contribute to chemotherapy resistance by actively effluxing anticancer drugs out of cells. This gene has also been studied for its role in pulmonary conditions, and its altered expression or function has potential involvement in disorders related to abnormal transporter activities such as gout and cardiovascular diseases. Pathway involvement typically includes those associated with xenobiotic metabolism and pharmacokinetics, affecting drug absorption and disposition.

##### Pharmacogenetics
Pharmacogenetic research on ABCC4 has primarily focused on its role in cancer pharmacology and the efficacy and toxicity of antineoplastic agents. Variants in ABCC4 have been associated with altered responses to several drugs, including thiopurines (mercaptopurine), nucleoside-based antiretroviral drugs used in HIV treatment (such as azidothymidine), and anti-platelet therapy drugs (like clopidogrel). Such variants can influence drug efflux from cells, thereby modifying drug efficacy and side effects. In cancer therapy, ABCC4's influence on drug resistance substantially affects treatment outcomes, emphasizing the need for genotyping and personalized treatment approaches in oncology.


## Gene: ABCC3
##### Gene Summary
ABCC3, also known as ATP-binding cassette sub-family C member 3, is a gene that encodes for a protein of the same name, which is part of the ABC transporter family. The function of ABCC3 predominantly involves the transport of various molecules across extra- and intra-cellular membranes. This transmembrane protein is particularly involved in the transport of bile acids, conjugated steroids, and other substrates such as glucuronidated xenobiotics, playing an important role in multidrug resistance and the detoxification pathways of various drugs and environmental toxins. The gene is primarily expressed in the liver, with significant expression levels also observed in the intestine, kidneys, and other tissues.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCC3 is implicated in several biological pathways regarding the transportation of substances across membranes. The gene plays critical roles in bile acid and bile salt transport, potentially impacting diseases related to liver function, such as cholestasis and other liver disorders. Aberrant expression or function of ABCC3 has been associated with several types of cancer, notably hepatocellular carcinoma. Phenotypically, alterations in ABCC3 can influence drug pharmacokinetics and disposition, affecting drug efficacy and toxicity. It is involved in the cellular efflux of many xenobiotics and is a part of the Phase III metabolism of various compounds, working alongside conjugation enzymes from Phase II metabolism.

##### Pharmacogenetics
In pharmacogenetics, ABCC3 is of significant interest due to its role in modulating the transport and, hence, the effects of various drugs. Variants within the ABCC3 gene can affect the expression and functionality of the transporter, leading to differences in drug disposition and response among individuals. This has implications for numerous drugs, including irinotecan, a chemotherapeutic agent where altered ABCC3 function may impact drug excretion and toxicity. Additionally, the transporter-influenced pharmacokinetics of mercaptopurine, a drug used in the treatment of leukemia, and methotrexate, used in the treatment of autoimmune diseases and cancer, highlight its pharmacogenetic importance. Understanding genetic variations within ABCC3 can aid in optimizing dose regimens and minimizing side effects for these and other drugs, contributing to personalized medicine approaches.


## Gene: CDA
##### Gene Summary
CDA, or cytidine deaminase, is an enzyme predominantly involved in the metabolism of pyrimidine nucleosides in nucleotide salvage pathways, which are critical for DNA and RNA synthesis. This enzyme catalyzes the deamination of cytidine and deoxycytidine to uridine and deoxyuridine, respectively. CDA is expressed in various tissues with notable levels in the liver and blood cells. Its activity influences the effectiveness and toxicity of chemotherapeutic drugs, particularly nucleoside analogs.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
CDA is directly associated with the metabolism of several chemotherapeutic agents used in the treatment of cancers such as leukemia, lymphoma, and breast cancer. Disorders related to CDA include CDA deficiency, which can lead to increased drug toxicity and haematopoietic disorders. In terms of pathways, CDA is a key player in the pyrimidine metabolism pathway, specifically affecting nucleoside recycling. Genetic variations in CDA can affect drug efficacy and patient susceptibility to side effects of cytotoxic drugs.

##### Pharmacogenetics
The pharmacogenetics of CDA plays a significant role in determining the clinical outcomes in patients undergoing treatment with nucleoside analogs like gemcitabine and cytarabine. Variants in the CDA gene can lead to differences in enzyme activity, thereby influencing drug concentration and toxicity. For instance, reduced activity alleles can result in higher plasma levels of active drug metabolites, increasing the risk of severe toxicities in patients treated with these drugs. Specific attention is given to allelic variants like CDA*2, which have been associated with an increased risk of severe toxic reactions to chemotherapeutic treatments. Overall, understanding individual genetic variability in CDA is crucial for optimizing dosages and minimizing adverse effects of nucleoside analogs in cancer therapy.


## Gene: BRINP3
##### Gene Summary
BRINP3, also known as BMP/retinoic acid-inducible neural-specific protein 3, is a gene implicated in the regulation of neural development and cell cycle. Located on chromosome 10q25.2, BRINP3 is part of a family of BMP/retinoic acid-inducible neural-specific proteins, which also includes BRINP1 and BRINP2. The protein encoded by BRINP3 is primarily expressed in the brain and plays a role in dendritic growth and synaptic functions. This gene functions by modulating cell proliferation and differentiation in neural tissues.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
BRINP3 has been studied for its role in neurological conditions and psychiatric disorders. Research indicates a potential link between BRINP3 and disorders such as schizophrenia and bipolar disorder, although these associations need further validation. The gene is involved in neural pathways that could be significant for understanding the molecular foundations of these mental health conditions. BRINP3's interaction with growth factors and signaling pathways like those mediated by bone morphogenic proteins (BMPs) and retinoic acid indicates its importance in neurodevelopmental processes.

##### Pharmacogenetics
As of current knowledge, there is limited specific pharmacogenetic data associated with BRINP3 concerning direct interactions with drugs. The pharmacogenetic implications of BRINP3 are primarily associated with its potential role in influencing the susceptibility to and the progression of neurological and psychiatric conditions. Thus, understanding the gene's function and expression patterns could be crucial in the development of therapeutic strategies targeting these diseases. However, direct associations with drugs and personalized medicine applications based on BRINP3 expression or mutations are yet to be extensively explored and established.


## Gene: HLA-B
##### Gene Summary
HLA-B, the human leukocyte antigen B, is a gene located on chromosome 6 that plays a critical role in the immune system as part of the major histocompatibility complex (MHC) class I system. It encodes a cell surface protein that is ubiquitous among nucleated cells in the body. HLA-B proteins are primarily involved in presenting peptides derived from intracellular proteins to the immune system, specifically to cytotoxic T cells. This enables the immune system to detect cells that are infected with viruses or transformed by cancer. The extreme polymorphism in the HLA-B gene is a key feature that allows for a diverse immune response, capable of responding to a wide array of pathogens.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-B is associated with various diseases, prominently including autoimmune disorders and drug hypersensitivity reactions. The gene's diversity is linked to differential susceptibilities to diseases such as ankylosing spondylitis, Behcet's disease, and certain types of drug-induced hypersensitivity, like those triggered by abacavir, a drug used in the treatment of HIV. In immunopharmacology, particular HLA-B alleles play crucial roles in immune-mediated adverse drug reactions. For instance, the HLA-B*57:01 allele has been famously connected to severe reactions to abacavir. Additionally, the gene is involved in pathways pertaining to antigen processing and presentation, playing a pivotal role in the immune response modulation.

##### Pharmacogenetics
From a pharmacogenetic perspective, HLA-B is highly significant in influencing individual responses to medications, particularly through its impact on immune-mediated drug reactions. Specific alleles of HLA-B, such as HLA-B*57:01, have been associated with hypersensitivity to abacavir. Patients carrying this allele are at high risk of developing a severe hypersensitivity reaction if treated with abacavir, making genetic screening a critical component of patient management before initiating abacavir therapy. Other notable associations include HLA-B*15:02 with carbamazepine-induced Stevens-Johnson syndrome and toxic epidermal necrolysis, particularly in Asian populations. Such pharmacogenetic associations underscore the importance of considering HLA-B genotype in the personalized medicine context to optimize drug therapy and mitigate adverse effects.


## Gene: NELL1
##### Gene Summary
NELL1, short for Neural EGFL Like 1, is a protein-coding gene primarily involved in the regulation of bone and tissue development. The protein encoded by NELL1 is a secreted, extracellular matrix protein that rich in epidermal growth factor-like repeat domains, and it is believed to be critical in skeletal remodeling and integrity. It primarily functions in promoting osteoblast differentiation and enhances bone regeneration and repair. Expression of NELL1 is notably high in cranial and skeletal tissues during embryonic development, suggesting its significant role in bone formation and developmental processes.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
NELL1 is intricately linked with several skeletal disorders and craniofacial developmental anomalies. Deficiencies or mutations in the NELL1 gene have been associated with bone density abnormalities and certain forms of craniosynostosis, a condition marked by the premature fusion of cranial sutures. The gene's product influences a variety of signaling pathways including those related to bone morphogenetic proteins (BMP), Wnt, and possibly calcium signaling pathways, which are crucial for bone and cartilage development. Beyond its primary roles, NELL1 has potential implications in osteoporosis and osteoarthritis due to its involvement in bone metabolic processes.

##### Pharmacogenetics
Current pharmacogenetic insights into NELL1 are somewhat limited as it is not typically a direct target of pharmacological interventions in the conventional sense of drug targeting. However, its role in bone and skeletal tissue has propelled research into using NELL1 as a therapeutic target or biomarker in regenerative medicine and orthopedics. Advances have been made in exploiting NELL1 for therapeutic applications in bone grafts and in promoting bone growth where deficiencies exist. Drugs or biological agents that modulate the activity of pathways involving NELL1, or that use NELL1-related compounds, might eventually play a role in the treatment of bone-related diseases. These applications are still largely in the experimental or clinical trial stages.


## Gene: MT-ND1
##### Gene Summary
MT-ND1 (Mitochondrially Encoded NADH Dehydrogenase 1) is a gene located within the mtDNA (mitochondrial DNA) and encodes one of the subunits of the enzyme Complex I (NADH: ubiquinone oxidoreductase), which is the first enzyme complex in the mitochondrial respiratory chain. This complex is responsible for the transfer of electrons from NADH to ubiquinone, which is an essential step in the process of oxidative phosphorylation. The proper functioning of MT-ND1 is critical for the generation of ATP via the gradient-driven synthesis performed by ATP synthase. MT-ND1 expression and activity are most pivotal in tissues with high energy demands such as the heart, brain, and muscles.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
Mutations in MT-ND1 have been associated with several mitochondrial disorders, which affect cellular energy metabolism. Phenotypically, these mutations can manifest in a variety of ways, most commonly including Leber's Hereditary Optic Neuropathy (LHON), which is characterized by the death of retinal ganglion cells leading to blindness. Other conditions associated with mutations in this gene include mitochondrial encephalomyopathy, lactic acidosis, and stroke-like episodes (MELAS syndrome). Pathologically, alterations in MT-ND1 can disrupt the electron transport chain, resulting in decreased ATP production and increased ROS (reactive oxygen species) production, which in turn can contribute to cellular damage and inflammation.

##### Pharmacogenetics
Pharmacogenetic relevance of MT-ND1 mainly lies in its role influencing mitochondrial toxicity in response to various drugs, given its critical role in energy production. While specific drugs directly targeting MT-ND1's function are currently limited, understanding individual variations in MT-ND1 can help predict susceptibilities to drugs that impact mitochondrial function. Notably, antiretroviral drugs used in HIV treatment, such as Zidovudine, can cause mitochondrial toxicity whose severity might be influenced by MT-ND1 mutations. Therefore, genetic variations in this gene can potentially inform on the likely individual risks of mitochondrial disorders and drug-induced mitochondrial dysfunction, making it a candidate for consideration in personalized medicine strategies, especially in managing complex diseases with a mitochondrial component.


## Gene: PADI4
##### Gene Summary
PADI4, or Peptidyl Arginine Deiminase 4, is an enzyme that catalyzes the conversion of arginine residues in proteins to citrulline, known as citrullination or deimination. The activity of PADI4 is calcium-dependent, which alters protein properties by affecting ionic interactions, thus playing crucial roles in gene regulation and cellular differentiation. PADI4 expression is notable in immune cells like neutrophils and macrophages, and is also seen in the skin and other tissues involved in the immune response. Its regulation and activity affect processes such as inflammation and apoptosis.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
PADI4 is profoundly associated with autoimmune diseases, notably rheumatoid arthritis (RA), where it contributes to the formation of anti-citrullinated protein antibodies (ACPAs) - a hallmark of RA. Studies suggest its involvement in other inflammatory conditions and possibly in cancer, through mechanisms influencing apoptosis, gene regulation, and cell differentiation. The gene plays a significant role in the inflammatory response pathway by modifying histones, leading to changes in gene expression which can contribute to disease pathology. Understanding the pathways involving PADI4 could potentially identify new therapeutic targets for diseases characterized by inappropriate immune responses.

##### Pharmacogenetics
In pharmacogenetics, PADI4 is of particular interest due to its implications in the effectiveness and response rates of drugs used in the treatment of RA and potentially other autoimmune disorders. Variants in the PADI4 gene, especially those affecting enzyme function or expression, could influence patient responses to specific treatments. For instance, RA treatments like methotrexate and biologic agents may have varying efficacy dependent on PADI4 activity and expression levels, although direct correlations are still under investigation. Recognition of these associations is crucial in the context of personalized medicine, aiming to tailor therapeutic approaches based on individual genetic profiles.


## Gene: SLC28A3
##### Gene Summary
SLC28A3, or Solute Carrier Family 28 Member 3, is part of the solute carrier family, specifically involved in the sodium-coupled nucleoside transport. This gene encodes a protein known as a concentrative nucleoside transporter, which predominantly facilitates the cellular uptake of nucleosides and nucleoside analogs, along with sodium ions, primarily in the liver and kidney. The expressed transporter exhibits specificity mainly towards purine nucleosides, pyrimidine nucleosides, and their analogs, playing a crucial role in the salvaging and metabolism of nucleosides.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
The function of SLC28A3 is significant in contexts where nucleoside analogs are used, such as antiviral and anticancer therapies. Its activity affects the pharmacokinetics and efficacy of drugs like ribavirin, which is used against hepatitis C and certain viral hemorrhagic fevers. Additionally, alterations in the expression or function of this transporter can influence drug toxicity and resistance. The gene is also relevant in understanding conditions associated with disrupted nucleoside metabolism and transport, such as certain types of renal diseases.

##### Pharmacogenetics
The pharmacogenetic profile of SLC28A3 is critical particularly in the administration of ribavirin and other nucleoside analogs. Variations in the SLC28A3 gene can lead to differences in drug absorption and clearance, impacting drug efficacy and the risk of adverse effects. For instance, certain polymorphisms in SLC28A3 have been investigated for their role in modulating ribavirin treatment outcomes in hepatitis C patients, affecting therapy responses and the manifestation of anemia as a side effect. This highlights the importance of considering SLC28A3 genotypes in personalized medicine, particularly in treatments involving nucleoside analogs.


## Gene: HLA-E
##### Gene Summary
HLA-E, or Human Leukocyte Antigen E, is a gene encoding an MHC class I molecule, which plays a crucial role in the immune system by presenting antigens to T cells. It is located within the MHC class I region on chromosome 6. HLA-E is notable for its relatively limited polymorphism compared to other class I HLAs and presents a restricted set of peptides derived primarily from the signal sequences of other HLA class I molecules. This gene is ubiquitously expressed across various tissues but is more prominent in immune cells. HLA-E is involved in immune recognition by interacting with NK cell receptors, thus influencing the immune system’s response to infected or malignant cells.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-E is involved in various immune-mediated diseases and conditions due to its role in antigen presentation and immune regulation. It is associated with disease susceptibilities such as viral infections, autoimmune diseases, and cancer. The interaction of HLA-E with receptors such as NKG2A/C expressed on natural killer (NK) cells and some T cells modulates immune responses, potentially affecting disease outcome and severity. It is also implicated in transplantation biology, where its expression can impact graft acceptance and rejection. Furthermore, HLA-E participates in immune regulation pathways, including the presentation of viral and self-peptides to immune cells, playing a role in immune evasion and tolerance.

##### Pharmacogenetics
In the context of pharmacogenetics, the HLA-E gene has crucial implications, particularly in the field of transplantation and immune-modulating therapies. Although direct associations with specific drugs are not extensively characterized like other HLA genes (e.g., HLA-B or HLA-A), variations in HLA-E could potentially influence the efficacy and safety of drugs that modulate immune responses, including certain biologics used in autoimmune diseases and cancers. For example, understanding the role of HLA-E in immune checkpoint pathways could guide the use of checkpoint inhibitors in cancer therapy. Moreover, the influence of HLA-E on NK cell activity suggests that it could impact the outcomes of treatments involving NK cell modulation. As with other HLA genes, HLA-E could also be relevant in hypersensitivity reactions to certain drugs, although specific drug associations are less documented compared to other members of the HLA gene family.


## Gene: HLA-C
##### Gene Summary
HLA-C, or Human Leukocyte Antigen C, is part of the major histocompatibility complex (MHC) class I molecules encoded on chromosome 6. HLA-C plays a critical role in the immune system by presenting peptides derived from intracellular proteins to cytotoxic T cells. This presentation mechanism is fundamental for immune detection and response to infected or transformed cells. HLA-C is highly polymorphic, which influences its peptide binding preference and consequently impacts immune recognition. The expression of HLA-C is ubiquitous but relatively lower and more variable on different tissues compared to other MHC class I molecules.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-C is implicated in the pathogenesis of various autoimmune diseases and immune-related conditions, such as psoriasis, HIV infection control, and transplant rejection. Its variations influence the susceptibility to and prognosis of these conditions due to differences in immune response efficacy. For example, certain alleles like HLA-C*06 are strongly associated with psoriasis. HLA-C interactions are also critical in cancer immunosurveillance. Pathway involvement includes antigen processing and presentation, a key pathway in adaptive immunity, where HLA-C participates in presenting endogenously synthesized antigens to CD8+ T cells.

##### Pharmacogenetics
In pharmacogenetics, HLA-C has notable associations with drug hypersensitivity reactions. The allele HLA-C*06:02, for instance, is linked to adverse drug reactions with the antiviral agent abacavir used in HIV treatment. Patients carrying this allele have a significantly increased risk of developing abacavir hypersensitivity syndrome, which can be life-threatening. Therefore, genetic testing for HLA-C*06:02 is recommended before initiating abacavir treatment. Other drugs may also interact with different HLA-C variants affecting drug efficacy and toxicity, thus highlighting the importance of considering HLA-C alleles in precision medicine and individualized drug therapy planning.


## Gene: VEGFC
##### Gene Summary
VEGFC (Vascular Endothelial Growth Factor C) is crucial for the development and maintenance of lymphatic vessels, enhancing lymphangiogenesis. It primarily binds to the receptor tyrosine kinases FLT4/VEGFR-3 and, to a lesser extent, KDR/VEGFR-2. VEGFC plays a significant role in embryonic vascular development, promoting endothelial cell growth, migration, and survival. The expression of VEGFC is noted in various tissues, but prominently in tissues related to cardiovascular and lymphatic health.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
VEGFC is implicated in several pathological conditions, most notably in cancer where it can enhance tumor growth and metastasis by promoting angiogenesis and lymphangiogenesis. Disorders such as lymphedema and other lymphatic-related abnormalities have also been associated with dysregulation of VEGFC. The gene participates in critical pathways like PI3K-Akt signaling pathway, which influences cellular processes such as proliferation and survival. Its role in developing the lymphatic system links it to studies in developmental biology and diseases involving vascular abnormalities.

##### Pharmacogenetics
Despite the significant role of VEGFC in angiogenesis and potential implications in treatment efficacy, specific pharmacogenetic associations involving drug interactions or modifications based on VEGFC genetic variants are not extensively documented. The therapeutic strategies targeting VEGFC typically involve the use of biological agents aimed at inhibiting its activity to counteract tumor growth and metastasis. However, as the research field expands, understanding how variations in VEGFC could affect drug efficacy or patient response may emerge, particularly in cancer therapeutics where angiogenesis is a vital target.


## Gene: HLA-G
##### Gene Summary
HLA-G, or Human Leukocyte Antigen G, is a non-classical major histocompatibility complex (MHC) class I gene. Unlike its classical counterparts that are widely expressed, HLA-G displays a highly restricted expression pattern, predominantly expressed in immune-privileged tissues such as the placenta, specifically by trophoblast cells, where it plays a critical role in maternal-fetal tolerance. HLA-G interacts with inhibitory receptors such as ILT2 and ILT4 on immune cells, leading to the suppression of immune responses and contributing to the acceptance of the fetus during pregnancy, as well as playing roles in autoimmune disease, transplantation tolerance, and tumor evasion.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-G is implicated in a range of clinical conditions and interactions. It has been studied extensively in the context of pregnancy, particularly regarding preeclampsia and recurrent spontaneous abortion, where its altered expression may contribute to pathogenesis. Additionally, its expression in tumors—such as melanoma, breast, and lung cancer—can enable these cells to evade immune detection and destruction. HLA-G also plays a role in transplantation immunology, influencing graft acceptance and rates of rejection. The gene is involved in multiple immune regulation pathways, highlighting its general importance in modulating immune responses under various physiological and pathological conditions.

##### Pharmacogenetics
The study of pharmacogenetics in relation to HLA-G mainly focuses on its impact on transplantation outcomes and its potential in cancer immunotherapies. Variations and expression levels of HLA-G can influence the efficacy of immunosuppressive drugs used post-transplantation, potentially affecting the risk of graft rejection or acceptance. In cancer therapy, understanding the role of HLA-G can help refine approaches to increase the immunogenicity of cancer cells, potentially improving the effectiveness of checkpoint inhibitors and other immunomodulators. However, as of now, specific drug associations and standardized pharmacogenetic guidelines involving HLA-G remain under investigation and are not as well-defined as for some other pharmacogenetic targets.


## Gene: SLCO1B1
##### Gene Summary
SLCO1B1, officially known as Solute Carrier Organic Anion Transporter Family Member 1B1, is crucial in hepatic uptake of various endogenous and xenobiotic compounds, including bile acids, hormones, and drugs. The protein encoded by SLCO1B1 is an organic anion-transporting polypeptide, part of the larger solute carrier family. This transporter is predominantly expressed in the liver and plays a significant role in the hepatic clearance of drugs from the blood. Variations within this gene have been linked to alterations in drug pharmacokinetics and treatment outcomes.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
SLCO1B1 is implicated in multiple clinical scenarios due to its role in drug transport. Its function affects the disposition and efficacy of a wide range of drugs including statins, antivirals, and cancer chemotherapeutics. Polymorphisms in this gene are associated with several disease phenotypes, notably statin-induced myopathy and differences in drug metabolism leading to adverse drug reactions or altered therapeutic effects. The transporter is involved in numerous physiological and pharmacological pathways, with a key role in drug detoxification processes, impacting both pharmacodynamics and pharmacokinetics.

##### Pharmacogenetics
The pharmacogenetic relevance of SLCO1B1 is significant, particularly concerning the metabolism of statins such as simvastatin. Variants like the c.521T>C (also known as p.Val174Ala) polymorphism have been extensively studied for their impact on the pharmacokinetics of simvastatin, where this particular genetic alteration leads to a reduced transport function, increasing plasma concentration of the drug and risk of myopathy. Additionally, this gene affects the effectiveness and toxicity of other important drugs like atorvastatin, repaglinide, and rifampin. Patients carrying specific SLCO1B1 genotypes may require dose adjustments or alternative therapies to mitigate risks of adverse effects or therapeutic failures.


## Gene: TPMT
##### Gene Summary
TPMT, or Thiopurine S-methyltransferase, is an enzyme encoded by the TPMT gene in humans. This gene is critical for the metabolism of thiopurine drugs, which are used primarily in the treatment of cancer and autoimmune diseases. TPMT catalyzes the S-methylation of thiopurines, which is a crucial step in their biotransformation and inactivation. The activity of TPMT in the body varies significantly between individuals due to genetic polymorphisms, which can greatly influence drug efficacy and toxicity. Expression of TPMT is seen in various tissues including liver and red blood cells.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
TPMT is intimately associated with drugs like azathioprine, mercaptopurine, and thioguanine, which are commonly employed in the treatment of conditions such as acute lymphoblastic leukemia (ALL), inflammatory bowel disease (IBD), and autoimmune disorders. Genetic variants in TPMT can lead to varying levels of enzyme activity and thus influence the risk of adverse effects and treatment outcomes. Individuals with reduced or absent TPMT activity are at increased risk for severe myelosuppression when treated with standard doses of thiopurines. The enzyme plays a role in the purine metabolism pathway, impacting drug metabolism and chemical carcinogenesis.

##### Pharmacogenetics
The pharmacogenetics of TPMT is highly significant due to its impact on the treatment with thiopurine drugs. Variants in the TPMT gene can lead to low, intermediate, or high enzyme activity, and testing for these variants can guide dosing to optimize therapy and minimize toxicity. Particularly, genetic polymorphisms like TPMT*2, TPMT*3A, and TPMT*3C are well-documented and lead to decreased enzyme activity. Patients with these variants typically require reduced doses of thiopurines. For instance, patients harboring two non-functional alleles (homozygous) generally exhibit severe or potentially life-threatening myelosuppression when treated with conventional doses of thiopurines, necessitating substantial dose adjustments or alternative therapies. Given these associations, TPMT genotype testing is recommended prior to initiating therapy with thiopurine drugs to tailor treatment regimens appropriately and enhance patient safety.


## Gene: ABCB4
##### Gene Summary
ABCB4 stands for ATP Binding Cassette Subfamily B Member 4, a gene encoding the protein Multidrug Resistance Protein 3 (MDR3), which is a member of the ABC transporter family. ABCB4 plays a crucial role in the transportation of phospholipids from hepatocytes into the bile, an essential process that protects the biliary tract from the detergent action of bile salts. The protein is primarily expressed in the liver, particularly in the canalicular (apical) membrane of hepatocytes. Mutations or dysfunction in ABCB4 are implicated in several liver-related disorders.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCB4 is prominently associated with several cholestatic liver diseases. Conditions linked to mutations or dysfunction in this gene include Progressive Familial Intrahepatic Cholestasis type 3 (PFIC3), a severe pediatric liver disorder; Bile Duct Cancer; Intrahepatic Cholestasis of Pregnancy (ICP); and Drug-induced liver injury (DILI). Moreover, ABCB4 dysfunction contributes to Low Phospholipid-Associated Cholelithiasis (LPAC) syndrome, characterized by the formation of gallstones. The gene operates within the lipid transport pathways and influences the composition and flow of bile, a key aspect influencing many of these conditions.

##### Pharmacogenetics
In the field of pharmacogenetics, ABCB4 has notable associations with the efficacy and safety profiles of certain medications, impacting patient management strategies. Ursodeoxycholic acid (UDCA), a commonly used treatment for cholestatic liver diseases, exhibits varying degrees of effectiveness potentially influenced by ABCB4 variants. In individuals with specific mutations in ABCB4, there is an observed resistance or diminished response to UDCA treatment. Additionally, variations in this gene are linked with differential risk and severity of Drug-induced liver injury (DILI) caused by various medications, influencing therapeutic decisions in clinical settings. Understanding the patient-specific ABCB4 genotype can guide the selection and dosing of medications to optimize therapy and minimize adverse effects.


## Gene: HLA-DRB1
##### Gene Summary
HLA-DRB1 (Human Leukocyte Antigen - DR Beta 1) is part of the human major histocompatibility complex (MHC) class II molecules located on chromosome 6. HLA-DRB1 plays a critical role in the immune system by presenting peptides derived from extracellular proteins to T cells. It is highly polymorphic, which allows it to present a wide range of antigens. The expression of HLA-DRB1 is mainly seen on antigen-presenting cells like macrophages, dendritic cells, and B cells. This gene's diversity is essential for the adaptive immune system to recognize and respond to the myriad of pathogens encountered by an individual.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-DRB1 is associated with several autoimmune and inflammatory diseases due to its fundamental role in immune response. It is notably linked with diseases such as rheumatoid arthritis, multiple sclerosis, and type 1 diabetes. The gene's involvement often relates to how immune cells recognize and interact with pathological and healthy human tissues, contributing to the disease's phenotype. The gene also plays a role in response pathways related to immune regulation, antigen presentation, and various inflammatory responses.

##### Pharmacogenetics
Pharmacogenetically, HLA-DRB1 is key in determining the risk of drug hypersensitivity reactions. Specific alleles of this gene are known to predispose individuals to adverse reactions to certain drugs. For example, HLA-DRB1*15:01 allele is associated with an increased risk of developing hypersensitivity reactions to abacavir, a nucleoside analog used in the treatment of HIV. Similarly, the presence of HLA-DRB1*07:01 has been linked with liver injury provoked by ximelagatran, formerly used as an anticoagulant. Moreover, its variations influence treatment efficacy and tolerance to several immunomodulatory and anti-inflammatory drugs, thus guiding personalized treatment plans in autoimmune diseases.


## Gene: SLC28A1
##### Gene Summary
SLC28A1, short for Solute Carrier Family 28 Member 1, encodes a sodium/nucleoside cotransporter predominantly expressed in liver, heart, and skeletal muscle tissues. This protein plays a critical role in the cellular uptake of nucleosides, which are basic building blocks for the synthesis of nucleic acids. SLC28A1 specifically facilitates the active transport of purine and pyrimidine analogs across cell membranes, utilizing a sodium gradient as its driving force for nucleoside uptake.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
The SLC28A1 gene is implicated in influencing cellular uptake of various pharmacologically active nucleoside derivatives used in antiviral and anticancer therapies. The pathways associated with SLC28A1 include nucleoside metabolic processes and purine metabolism. The altered function or expression of this transporter can potentially affect the therapeutic efficacy and toxicity profiles of nucleoside drugs. Although there are no direct associations currently reported with specific diseases, variations in SLC28A1 expression and function could potentially influence disease progression where altered nucleoside metabolism is a factor.

##### Pharmacogenetics
In the context of pharmacogenetics, SLC28A1 is significant for its role in modulating the efficacy and toxicity of several antiviral drugs such as ribavirin and zidovudine. These agents are used in the treatment of conditions like Hepatitis C and HIV/AIDS, respectively. Variations in the SLC28A1 gene might influence the transporter's efficiency, directly impacting drug absorption, plasma concentrations, cellular uptake, and consequently, clinical outcomes. Thus, genetic polymorphisms in SLC28A1 could serve as biomarkers for predicting patient response to nucleoside analog therapies, optimizing dosing regimens and minimizing adverse effects in personalized treatment plans.


## Gene: CTPS1
##### Gene Summary
CTPS1, or Cytidine triphosphate synthase 1, is involved in the biosynthesis of cytidine triphosphate (CTP) which plays a crucial role in RNA and DNA synthesis. The enzyme catalyzed by CTPS1 is essential for de novo CTP synthesis pathway. It is expressed in various tissues, with significant relevance in rapidly dividing cells, including those in the immune system and malignancies. CTPS1's activity is critical for cellular proliferation and DNA synthesis, making it a pivotal enzyme in metabolic and replication processes.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
CTPS1 has implications in several disorders primarily due to its role in nucleotide synthesis. It has been associated with immunodeficiency conditions, where defects in CTPS1 can lead to reduced immune cell function and abnormal development. Pathways involving CTPS1 include purine and pyrimidine metabolism, with particular emphasis on the salvage and de novo synthesis pathways of pyrimidines. Because of its fundamental role in nucleotide synthesis, CTPS1 is also considered in studies related to cancer, where proliferative signaling is abnormally activated.

##### Pharmacogenetics
The pharmacogenetics of CTPS1 is particularly relevant in the context of immunosuppressive and anticancer therapy. Drugs targeting nucleotide synthesis, like ribavirin, a nucleoside inhibitor used in the treatment of Hepatitis C and certain viral hemorrhagic fevers, have been studied in relation to CTPS1 activity. The efficacy and toxicity of such drugs can be influenced by variations in the CTPS1 gene, impacting drug metabolism and therapeutic outcomes. Understanding CTPS1 pharmacogenetics helps in tailor-making treatments and dosing for affected individuals to optimize efficacy and minimize adverse effects, although specific common variants with broad clinical implications are yet to be fully established.


## Gene: HFE
##### Gene Summary
HFE is a gene that encodes the Homeostatic Iron Regulator protein, which plays a crucial role in regulating iron absorption in the body. It primarily modulates the interaction between transferrin, the main iron-carrying protein in the blood, and its receptor, helping to maintain iron homeostasis. The HFE protein is mainly expressed in liver cells, intestinal epithelial cells, and immune system cells. Mutations in this gene are associated with hereditary hemochromatosis, a disorder characterized by excessive iron absorption and progressive iron overload in various organs.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
The HFE gene is directly linked to the development of hereditary hemochromatosis, which is often asymptomatic early on but can lead to conditions such as liver cirrhosis, heart disease, diabetes mellitus, and arthritis if left untreated. The gene's product, the HFE protein, interacts with several key proteins and pathways involved in iron metabolism, including hepcidin, transferrin, and transferrin receptors. This interaction is crucial in the body’s regulatory network that maintains iron homeostasis. Disruption of these interactions due to mutations can lead to the phenotypic manifestations of hemochromatosis.

##### Pharmacogenetics
The pharmacogenetics of HFE mainly involves its association with the risk and management of hereditary hemochromatosis. Genetic testing for mutations in HFE, such as the C282Y and H63D mutations, is used to confirm the diagnosis of hemochromatosis in individuals who exhibit symptoms or have elevated iron levels. Management of the condition often involves regular phlebotomy or iron chelation therapy, although there is no direct pharmacological intervention targeted at the mutated HFE protein. Understanding individual genetic variations in HFE can aid in predicting disease severity and tailoring management plans, potentially improving outcomes in affected patients.


## Gene: HCP5
##### Gene Summary
HCP5 (HLA Complex P5) is a gene located within the major histocompatibility complex (MHC) on chromosome 6. Although initially thought to be involved primarily in the immune response, HCP5 is actually a noncoding RNA gene hypothesized to play roles in the regulation of immune system processes. HCP5 is predominantly found in immune cells and is most notably expressed in high levels within the context of infections. The function of HCP5 appears to be linked to the regulation of genes associated with the immune response as well as antiviral activities.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HCP5 has been studied in the context of multiple diseases, particularly those with a significant immune component. It is notably associated with susceptibility to HIV-1 infection and its progression to AIDS. The gene has also been linked to autoimmune diseases such as ankylosing spondylitis and psoriasis. These associations are believed to be through its link with the HLA-B gene, particularly the HLA-B*5701 allele, which is influenced by the presence of HCP5. The gene’s role in immune pathways, inflammation, and its interactions with viral elements are key areas of ongoing research.

##### Pharmacogenetics
In pharmacogenetics, HCP5 has gained attention primarily due to its association with the response to antiretroviral drugs in HIV treatment. Particularly, the HCP5 rs2395029 polymorphism, linked to the expression of the HLA-B*5701 allele, has been found to correlate with hypersensitivity reactions to the antiretroviral drug abacavir. This hypersensitivity is a critical factor in the clinical management of HIV, as genetic testing for HLA-B*5701 has become a routine part of the treatment planning process to prevent severe adverse reactions. Therefore, HCP5 serves as an important genetic marker in predicting patient response to abacavir, demonstrating the importance of genetic background in the personalization of medical treatments.


## Gene: RRM1
##### Gene Summary
**RRM1** (Ribonucleotide Reductase Catalytic Subunit M1) encodes the M1 subunit of ribonucleotide reductase, which is crucial for DNA synthesis. RRM1 is a key player in the conversion of ribonucleotides to deoxyribonucleotides, an essential process for DNA replication and repair. The enzyme consists of two subunits: RRM1 provides the catalytic function, and a smaller subunit (RRM2 or RRM2B) that helps modulate activity. Expression of RRM1 is highest in proliferating cells, reflecting its fundamental role in DNA synthesis. RRM1 expression varies across different tissues, being particularly notable in rapidly dividing cells such as those found in bone marrow and certain tumors.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
RRM1 is implicated in several pathways, primarily those relating to nucleotide metabolism and the DNA damage response. Its function impacts the effectiveness and toxicity of certain chemotherapeutic agents, particularly in cancers like non-small cell lung cancer (NSCLC). High expression levels of RRM1 have been associated with resistance to drugs that target DNA replication and repair mechanisms, influencing treatment outcomes in oncology. Diseases such as pancreatic cancer, colon cancer, and various other carcinoma types have shown aberrations in RRM1 expression or activity, suggesting its role in tumor progression and chemoresistance.

##### Pharmacogenetics
The pharmacogenetics of RRM1 mainly concerns its influence on chemotherapy efficacy in cancer treatment. Higher RRM1 expression has been associated with resistance to gemcitabine, a nucleoside analog used to treat several cancers including pancreatic, breast, ovarian, and NSCLC. In NSCLC, for instance, low RRM1 expression is a predictor of improved survival and enhanced responsiveness to gemcitabine-based chemotherapy. Genetic variants within the RRM1 gene can affect mRNA stability and protein expression, subsequently altering drug efficacy and patient outcomes. Personalized cancer therapy, therefore, sometimes involves testing RRM1 levels to tailor treatment plans, optimizing the use of gemcitabine and potentially other related chemotherapeutic agents.


## Gene: ADORA2A-AS1
##### Gene Summary
ADORA2A-AS1, officially known as the ADORA2A antisense RNA 1, is a non-coding RNA gene. This gene is involved in the regulation of its sense counterpart, ADORA2A, which encodes the adenosine A2a receptor. The adenosine receptors play crucial roles in cardiovascular, neurological, and immune functions by modulating signaling pathways upon activation by the endogenous ligand adenosine. ADORA2A-AS1 is primarily expressed in various brain regions, influencing neuronal and cognitive functions.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ADORA2A-AS1 is indirectly related to various neurological disorders through its regulatory effects on ADORA2A. The dysfunction of ADORA2A has been linked to Parkinson's disease, schizophrenia, and other neurological conditions. In pathways, ADORA2A-AS1 is believed to play a role in adenosine signaling pathways, which are pivotal in neurotransmitter regulation, inflammation response, and neuroprotection. The precise role and mechanisms of ADORA2A-AS1 within these pathways remain a subject of ongoing research.

##### Pharmacogenetics
As an antisense RNA gene, ADORA2A-AS1 does not directly interact with drugs in a conventional pharmacokinetic sense. However, its influence on the expression and function of ADORA2A makes it a gene of interest in pharmacogenetics, particularly in the context of drugs targeting the adenosine A2a receptor. Such drugs include caffeine, which is a known antagonist of the A2a receptor, and potential therapeutic agents for Parkinson's disease like istradefylline. Understanding the regulatory mechanisms of ADORA2A-AS1 could have implications for the efficacy and side-effect profiles of these drugs, especially in neurological applications. Further research is needed to elucidate these pharmacogenetic associations comprehensively.


## Gene: C18orf56
##### Gene Summary
C18orf56, officially known as chromosome 18 open reading frame 56, is a protein-coding gene of uncertain function. Details about its specific role and mechanisms are minimally documented in scientific literature. Yet, as an open reading frame, it potentially encodes a protein product, though this product and its biological roles require further investigation. Expression of C18orf56 is presumed in various tissues, typical of many open reading frame genes, but precise expression patterns, along with functional impacts, remain to be thoroughly characterized.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
As of current knowledge, the associations of C18orf56 with specific drugs, diseases, or phenotypes have not been clearly established. Research into any involvement in specific biological pathways is also limited, which reflects the broader challenge of annotating and functionally categorizing many such open reading frame genes. The absence of well-defined links to particular diseases or drugs indicates a potential area of future exploratory research which could unveil critical biological implications or therapeutic targets.

##### Pharmacogenetics
Regarding pharmacogenetics, C18orf56 does not yet have documented associations with the efficacy, metabolism, or side effects of drugs. The gene’s impact on pharmacological responses or interactions remains unexplored, primarily due to the lack of detailed functional characterization. Continued research could provide insights into any pharmacogenetic roles that C18orf56 may play, aiding in the development of personalized medicine strategies or in the improvement of drug efficacy and safety profiles in diverse populations.


## Gene: C5orf56
##### Gene Summary
C5orf56, also known as "chromosome 5 open reading frame 56," is a human gene located on chromosome 5. The specific functions of C5orf56 remain largely uncharacterized; however, the gene is believed to be involved in inflammatory processes due to its association with various autoimmune and inflammatory disorders. Its expression patterns and regulatory mechanisms remain under investigation, indicating that it is an area rich for future research. This gene is particularly noted for its potential role in the immune system's response to external stimuli.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
C5orf56 is implicated in several autoimmune and inflammatory conditions, though the exact mechanistic connections have yet to be fully elucidated. Studies suggest links to systemic lupus erythematosus and potentially to other related autoimmune syndromes. The gene might play a part in regulating immune responses or inflammation based on observed expression levels in various tissues under different physiological and pathological conditions. Research into the specific pathways involving C5orf56 is ongoing, with indications that it may interact or participate in genetic networks influencing inflammation and immune function.

##### Pharmacogenetics
As of current knowledge, direct pharmacogenetic associations involving C5orf56 are limited, primarily because the gene’s functions and interactions are not comprehensively understood. However, recognizing the gene's potential role in inflammatory processes could guide future pharmacogenetic research, particularly in the context of drugs intended for diseases like lupus where C5orf56 might someday be identified as impacting drug response or efficacy. Consequently, while no specific drugs have yet been linked to C5orf56 genetically, understanding its function may be crucial for developing or optimizing therapies targeting immune and inflammatory pathways.


## Gene: HLA-DQB1
##### Gene Summary
HLA-DQB1 (Human Leukocyte Antigen DQ Beta 1) is a gene located on chromosome 6 and is part of the major histocompatibility complex class II (MHC class II). It plays a crucial role in the immune system by presenting peptide antigens to T cells, which is essential for the immune response to pathogens. HLA-DQB1 is highly polymorphic, which influences its function in antigen presentation. This gene's expression is most prominent in immune system cells, including macrophages and dendritic cells.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-DQB1 is associated with several autoimmune diseases, such as type 1 diabetes, celiac disease, and multiple sclerosis. Specific alleles of this gene can either increase the risk of developing these diseases or protect against them. The gene is also involved in the immune response to various pathogens, making it crucial in infectious disease susceptibility and outcomes. HLA-DQB1 operates within the MHC class II pathway, involved in the exogenous pathway of antigen processing and presentation, critical for activating helper T cells, a subset of T cells that aid in orchestrating the immune response.

##### Pharmacogenetics
In pharmacogenetics, HLA-DQB1 has notable associations with drug hypersensitivity reactions. For example, the HLA-DQB1*06:02 allele is strongly linked with hypersensitivity to the drug abacavir, used to treat HIV. Individuals carrying this allele are at significantly increased risk for developing abacavir hypersensitivity syndrome, an adverse drug reaction that can be severe and life-threatening. Therefore, genetic testing for HLA-DQB1*06:02 is recommended before initiating abacavir treatment. This is a prime example of how HLA-DQB1 genotype can be critical in guiding therapeutic decisions to avoid serious drug reactions.


## Gene: DCK
##### Gene Summary
DCK, or Deoxycytidine Kinase, is an enzyme pivotal in the nucleoside salvage pathway, catalyzing the phosphorylation of deoxycytidine, deoxyguanosine, and deoxyadenosine. DCK adds the first phosphate group, converting these nucleosides into their monophosphate forms, which are necessary precursors for DNA synthesis. The gene is expressed in various tissues but shows higher expression levels in proliferative tissues such as bone marrow and lymphoid organs. This expression pattern underlines its critical role in DNA repair and cell proliferation.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
DCK is directly involved in the metabolism of several anticancer and antiviral drugs. Its function affects the activation of chemotherapeutic agents such as gemcitabine, clofarabine, and cladribine. Due to its role in drug metabolism, DCK is linked to the therapeutic effectiveness and toxicity of these drugs. The gene's malfunction or altered expression is associated with resistance to chemotherapy in various cancers, including leukemia and lymphoma. In terms of pathways, DCK is a key component in the purine metabolism and pyrimidine metabolism pathways, crucial for DNA synthesis and repair processes.

##### Pharmacogenetics
The pharmacogenetics of DCK is particularly significant in cancer treatment. Variations in the DCK gene can influence the effectiveness of nucleoside analog-based therapies. For example, specific polymorphisms in DCK have been associated with altered response rates to drugs like gemcitabine, used in pancreatic, breast, and non-small cell lung cancer. Studies have shown that certain DCK gene variants can lead to either an enhanced or reduced activation of these drugs, affecting their efficacy and toxicity. This makes DCK a potential biomarker for predicting patient response to nucleoside analogs in chemotherapy, highlighting the importance of personalized medicine approaches in oncology based on DCK pharmacogenetics.


## Gene: SLCO1A2
##### Gene Summary
SLCO1A2 is the official symbol for the gene encoding Solute Carrier Organic Anion Transporter Family Member 1A2. This gene plays a crucial role in the transport of various endogenous and exogenous organic anions. Primarily expressed in the liver and to a lesser extent in the kidney and brain, SLCO1A2 facilitates the uptake of anions into cells, which impacts the disposition and clearance of various compounds, including drugs, toxins, and hormones. This transporter is particularly important for the hepatic uptake of several negatively charged molecules from blood plasma.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
SLCO1A2 is involved in critical pathways pertaining to drug metabolism and the handling of xeno- and endobiotics. Alterations or deficiencies in SLCO1A2 function have been linked with variations in drug efficacy and toxicity. Furthermore, genetic variations in SLCO1A2 have been implicated in susceptibility to certain diseases, although direct associations with specific phenotypes or diseases are less well-defined compared to its role in pharmacokinetics. The gene is part of important biochemical pathways like the transport and metabolism of bile acids, steroid hormones, and various pharmaceutical agents, influencing both therapeutic outcomes and adverse drug reactions.

##### Pharmacogenetics
The pharmacogenetics of SLCO1A2 suggests that genetic variants can significantly impact the transporter's function, affecting the pharmacokinetics of several drugs. Clinically, this has implications for the absorption, distribution, and elimination of medications such as methotrexate, rifampin, and rosiglitazone. Variants in SLCO1A2 might alter the transporter activity, leading to differences in drug plasma levels and response variability among individuals. For example, certain polymorphisms in SLCO1A2 have been associated with altered transport activity for methotrexate, which can affect the drug's therapeutic efficacy and risk of toxicity. Understanding these pharmacogenetic interactions is crucial for optimizing drug dosing regimens and minimizing adverse effects, particularly in treatments involving drugs with narrow therapeutic windows.


## Gene: HLA-DRA
##### Gene Summary
HLA-DRA (Human Leukocyte Antigen-DR Alpha) is a gene located on chromosome 6, and it encodes the alpha chain of the HLA-DR protein, a component of the major histocompatibility complex (MHC) class II molecule. This gene is responsible for presenting peptide antigens to the immune system, particularly important for the activation of T cells and the regulation of the immune response. HLA-DRA is expressed ubiquitously in antigen-presenting cells including B cells, dendritic cells, and macrophages, highlighting its vital role in immune function.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-DRA is centrally involved in the immune response pathways and is inherently linked to several autoimmune diseases. Expression of this gene can influence susceptibility to conditions such as multiple sclerosis, rheumatoid arthritis, and type 1 diabetes. Phenotypically, variations in HLA-DRA and its associated pathways can affect antigen presentation and immune system adaptability. This gene plays a key role in immune regulation pathways, which could potentially interact with various immunomodulatory drugs.

##### Pharmacogenetics
The pharmacogenetic profile of HLA-DRA chiefly involves its role in modulating responses to certain drugs in the context of linked autoimmune diseases. While directly specific drug associations for HLA-DRA in pharmacogenetics are not well established compared to other genes in the HLA family, exploratory research suggests its potential involvement in differential immune responses to treatments in autoimmune disorders. Further studies are required to substantiate precise drug-gene interactions and to leverage this knowledge for personalized medicine approaches in conditions associated with antigen presentation dysregulation.


## Gene: RUNDC3B
##### Gene Summary
RUNDC3B, short for RUN Domain Containing 3B, is a human gene which is mainly recognized for its role in intracellular trafficking. Its encoded protein features a RUN domain, which is often implicated in various intracellular processes like cytoskeletal rearrangements, gene expression, and vesicle-mediated transport. The expression of RUNDC3B is observed in multiple tissues, pointing towards a potential involvement in diverse biological processes and pathways. The exact physiological functions of RUNDC3B remain relatively unexplored, however, initial studies suggest a role in cellular localization and dynamics.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
Currently, no specific drugs or diseases are directly linked to RUNDC3B. As knowledge about this gene is still evolving, its relation to specific phenotypes or medical conditions has not been firmly established. In cellular pathways, RUNDC3B could be implicated in vesicular transport pathways due to its domain structure and subcellular localization features. Further research is necessary to conclusively determine its pathways and interactions at the molecular level, which could potentially link RUNDC3B to specific cellular dysfunctions or diseases.

##### Pharmacogenetics
The pharmacogenetic associations of RUNDC3B are currently unclear, as there has not been substantial research linking this gene directly to the metabolism, efficacy, or adverse reactions of specific drugs. Given its potential involvement in cellular trafficking, future pharmacogenetic studies might explore whether variations in the RUNDC3B gene could influence drug absorption or delivery at the cellular level, particularly for medications targeting intracellular sites or pathways. Ongoing research may provide insights into the implications of this gene in pharmacogenetics and personalized medicine.


## Gene: G6PD
##### Gene Summary
G6PD, or Glucose-6-Phosphate Dehydrogenase, is an enzyme that plays a crucial role in the pentose phosphate pathway, a metabolic pathway that supplies reducing energy to cells (via NADPH) and contributes to the formation of ribose 5-phosphate (a precursor for the synthesis of nucleotides). G6PD is particularly important for the normal processing of carbohydrates and is critical in red blood cells where it protects them from damage and destruction. The gene is highly expressed in the liver, kidney, and erythrocytes. Deficiencies in G6PD can lead to hemolytic anemia triggered by stresses such as infections, certain foods, and medications.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
Deficiency in G6PD is linked to various clinical manifestations, including neonatal jaundice, acute hemolytic anemia, and chronic hemolytic anemia. This condition is known as G6PD deficiency, which is the most common enzyme deficiency worldwide, affecting more than 400 million people. It is more prevalent in certain malaria-endemic regions, an evolutionary adaptation thought to confer some protection against malaria. G6PD is part of the pentose phosphate pathway, which is integral in maintaining redox balance and producing nucleotides and nucleic acids. The enzyme’s activity is also relevant to certain chemotherapy drugs and antibacterial agents.

##### Pharmacogenetics
In pharmacogenetics, the significance of G6PD primarily centers on its role in drug-induced hemolysis. Individuals with G6PD deficiency have increased sensitivity to a range of drugs that can trigger hemolysis. Prominent examples include antimalarials such as primaquine and chloroquine, certain antibiotics like dapsone and sulfa drugs, and some non-steroidal anti-inflammatory drugs (NSAIDs). The reaction to these drugs can range from mild anemia to severe life-threatening hemolysis, necessitating that those with G6PD deficiency avoid these triggers. Additionally, variant alleles of G6PD, which can differ widely in their impact on enzyme activity, affect the severity and specific drug sensitivities, making genetic testing a critical tool for personalized medicine in populations at risk.


## Gene: MLN
##### Gene Summary
MLN (Motilin) is a gene that encodes the motilin protein, a peptide hormone. This hormone plays a critical role in gastrointestinal motility by stimulating gastric activity between meals, a process known as the interdigestive migrating contractions. Motilin is predominantly expressed in the small intestine's mucosal epithelial cells, particularly in the duodenum and jejunum. It functions through its interaction with the motilin receptor (MLNR), affecting gastrointestinal motility, and has been implicated in the physiological regulation of hunger signals and digestive patterns.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
MLN is primarily associated with the regulation of gastrointestinal functions. Abnormal motilin signaling has been linked with gastrointestinal disorders such as diabetic gastroparesis, a condition characterized by delayed gastric emptying. In terms of drug interactions, motilin agonists are used to treat this condition by enhancing gastric contraction rates. The pathways involving MLN include various signaling mechanisms regulating gut motility and possibly impacting conditions like irritable bowel syndrome (IBS) and small intestinal bacterial overgrowth (SIBO).

##### Pharmacogenetics
In pharmacogenetics, variations in the MLN gene or its receptor can alter patient responses to drugs targeting the motilin pathway. For instance, macrolide antibiotics, which also act as motilin receptor agonists, may exhibit variable efficacy due to genetic differences in MLN or MLNR expression. This interaction can affect the therapeutic outcomes in treating gastroparesis or enhancing gastric motility in critical care settings. Understanding genetic variations in MLN pathways can aid in tailoring therapeutic strategies for gastrointestinal disorders by optimizing dosages and choosing the most effective treatment plans. This approach assists in reducing adverse effects and improving clinical outcomes in pharmacotherapy related to motility disorders.


## Gene: DCTD
##### Gene Summary
DCTD is the official symbol for the gene encoding deoxycytidylate deaminase, an enzyme involved in the pyrimidine salvage pathway, which is essential for nucleotide metabolism. DCTD catalyzes the deamination of dCMP (deoxycytidine monophosphate) to dUMP (deoxyuridine monophosphate), which is a precursor for thymidylate synthesis. Expression of DCTD is critical in rapidly dividing cells where DNA synthesis is significant, including various tissues and cancer cells, thus underscoring its importance in cellular proliferation and growth.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
DCTD plays a role in several key pathways, including thymidylate biosynthesis and pyrimidine metabolism, which are crucial for DNA replication and repair. Disturbances in these pathways can lead to genomic instability and contribute to oncogenesis. DCTD has been studied in the context of cancer, particularly due to its role in nucleotide metabolism, which is often altered in malignant cells. The enzyme's function makes it a potential target for chemotherapeutic agents that aim to disrupt DNA synthesis in cancer cells.

##### Pharmacogenetics
DCTD's pharmacogenetic profile is significant in the context of cancer treatment, where drugs targeting nucleotide metabolism can be influenced by variations in the DCTD gene. For instance, the antimetabolite drug cytarabine, used in the treatment of various leukemias, is converted within the body into its active triphosphate form, which can be influenced by the activity of DCTD. Genetic variations in DCTD could affect drug efficacy and toxicity, impacting patient response to therapy. Personalized medicine approaches often consider such genetic factors to optimize dosing and select the best therapeutic strategies for individual patients based on their DCTD gene profile.


## Gene: ABCC5
##### Gene Summary
ABCC5 (ATP Binding Cassette Subfamily C Member 5) is a member of the ATP-binding cassette (ABC) transporter superfamily, which are integral membrane proteins involved in the transport of various molecules across extra- and intra-cellular membranes. ABCC5 primarily acts as an efflux transporter, facilitating the movement of organic anions and drugs out of cells. It is ubiquitously expressed but shows higher expression levels in the brain, heart, and skeletal muscle. The protein encoded by ABCC5 can influence cellular processes by modulating the concentration of signaling molecules and metabolites, impacting cellular signaling and metabolism.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCC5 is linked with the handling and resistance to multiple drugs, particularly in the context of cancer chemotherapy. It is shown to transport substrates such as cyclic nucleotides, which have a role in cellular signaling pathways, including those involved in phosphodiesterase inhibitors action. Diseases associated with ABCC5 include various types of cancer, where its expression can be related to a reduction in the effective intracellular accumulation of chemotherapeutic drugs, thus contributing to multi-drug resistance. Additionally, its role in modulating the transport of crucial metabolites and drugs may implicate it in neurological disorders and cardiovascular diseases.

##### Pharmacogenetics
In the realm of pharmacogenetics, ABCC5 has been studied for its effects on the pharmacokinetics and dynamics of several drugs, particularly in cancer treatment. It has been associated with alterations in response to anti-cancer agents like methotrexate, 5-fluorouracil, and thiopurines. Variants in ABCC5 can alter the transporter activity, potentially influencing the efflux and thus the bioavailability and toxicity of these drugs. Research indicates that certain single nucleotide polymorphisms (SNPs) in ABCC5 may correlate with the survival outcomes and adverse effects profiles in patients treated with specific chemotherapeutic regimens. Given its role in drug transport, pharmacogenetic testing for variants in the ABCC5 gene may help to predict patient responses to certain medications and guide personalized medicine approaches in oncology.


## Gene: IGF2-AS
##### Gene Summary
IGF2-AS, officially known as "IGF2 antisense RNA" or often referred to as IGF2 antisense gene, is involved in the complex regulation of the insulin-like growth factor 2 (IGF2) gene. IGF2 is a key growth regulatory factor in human development, and its regulation is crucial for normal growth and development. The IGF2-AS gene produces a non-coding RNA that is involved in the imprinting and regulation of IGF2 expression, primarily through mechanisms of antisense transcription and possibly by influencing the local chromatin structure. The function and expression of IGF2-AS are implicated in controlling the differential expression of the IGF2 gene.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
IGF2-AS plays a significant role in growth and metabolic pathways due to its regulatory impact on IGF2. Aberrant regulation or expression of this antisense RNA or its associated genomic imprinting might contribute to various growth disorders and metabolic diseases, such as Beckwith-Wiedemann syndrome, which is characterized by overgrowth and an increased risk of embryonal tumors. Moreover, alteration in IGF2-AS has also been studied in the context of cancer, as dysregulation of IGF2 is known to promote tumorigenesis in various tissues. The gene is also associated with insulin resistance and type 2 diabetes pathways, showing its broader impact on metabolic regulation.

##### Pharmacogenetics
In terms of pharmacogenetics, understanding the role of IGF2-AS could provide insights into individual variability in drug response, especially for treatments aimed at metabolic and growth disorders. Though direct pharmacogenetic associations with specific drugs are currently less explored and might not be widely documented, the regulatory influence IGF2-AS exerts over IGF2 suggests it could impact the efficacy and safety of drugs that target growth factors or hormonal pathways. Drugs modulating the insulin-like growth factor pathway, such as growth hormone or insulin therapies, might be influenced by alterations in IGF2-AS expression. Further research into the pharmacogenetic implications of IGF2-AS could potentially enhance personalized treatment strategies in growth-related conditions and cancers associated with IGF2 dysregulation.


## Gene: SLC22A11
##### Gene Summary
SLC22A11 (Solute Carrier Family 22 Member 11) is a gene that encodes a protein known as the organic anion transporter 4 (OAT4). This protein belongs to the organic anion transporters (OATs) subgroup within the larger family of solute carriers. It is primarily expressed in the kidney, particularly in the proximal tubule cells, where it functions in the renal handling of endogenous and exogenous organic anions. OAT4 facilitates the exchange of intracellular dicarboxylates for extracellular organic anions, playing a crucial role in the secretion and reabsorption processes of various substances in the kidney.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
SLC22A11 is involved in the transport of several drugs, including popular diuretics, antivirals, and antibiotics. It plays a significant role in renal drug excretion and can affect the pharmacokinetic behavior of drugs. The alteration in function of SLC22A11 can lead to variations in drug response and toxicity. Diseases associated with SLC22A11 mainly concern renal function impairments and disorders such as hypertension and renal tubular acidosis. Pathways involving SLC22A11 include drug metabolism and the transport of metabolic products and xenobiotics, integral to understanding the pharmacokinetics of many therapeutic agents.

##### Pharmacogenetics
In pharmacogenetics, SLC22A11 is of notable interest due to its influence on the renal clearance of medications. Variants in this gene can affect the transporter activity, which is critical for drugs whose elimination is heavily dependent on renal excretion. Specific genetic variations in SLC22A11 have been linked to altered responses to certain diuretics such as furosemide and thiazides, which are used to treat hypertension and congestive heart failure. Research into the pharmacogenetics of SLC22A11 aims to better predict individual responses to these drugs and adjust dosages more accurately to improve therapeutic outcomes and reduce adverse effects. Further studies on the gene-disease associations and gene-drug interactions continue to enhance personalized medicine efforts.


## Gene: TAPBP
##### Gene Summary
TAPBP, also known as TAP binding protein, is integral in the adaptive immune system, primarily known for its role in antigen processing. TAPBP is crucial for the proper functioning of the Transporter Associated with Antigen Processing (TAP) involved in the MHC class I antigen presentation pathway. This pathway is essential for presenting intracellular antigens to cytotoxic T cells. TAPBP acts by bridging the interaction between TAP and MHC class I molecules, thereby facilitating the translocation of peptides from the cytosol into the endoplasmic reticulum, where they bind to MHC class I molecules before being presented on the cell surface.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
TAPBP is primarily associated with the immune response pathway and antigen presentation mechanism. Disruptions or alterations in TAPBP functions can lead to a range of immune system disorders, including susceptibility to viral infections and potentially influencing the efficacy of tumor immune surveillance. In terms of diseases, changes in the expression or function of TAPBP have been studied in the context of autoimmune disorders and several cancers, where antigen processing and presentation are crucial for disease progression and immune escape.

##### Pharmacogenetics
In pharmacogenetics, TAPBP has not been directly linked to specific drug responses or adverse drug reactions in a manner as clearly defined as some other genes known for their pharmacogenetic implications. However, given its pivotal role in immune modulation, TAPBP could have indirect implications in treatments involving immune checkpoint inhibitors and other immunotherapies used in cancer treatment. This suggests a potential avenue for future pharmacogenetic research, particularly in determining the variability of patient responses to immunotherapies depending on TAPBP function or expression levels. Understanding variations in TAPBP could, therefore, enhance personalized approaches to treatments in oncology and infectious diseases.


## Gene: GBP6
##### Gene Summary
GBP6, or Guanylate Binding Protein 6, is a member of the guanylate-binding protein (GBP) family, which is part of the larger GTPase superfamily. These proteins are involved in a variety of cellular processes including cell signaling, proliferation, and immune responses. GBPs, including GBP6, are particularly known for their role in immune responses against microbial and viral pathogens. GBP6 is expressed in a variety of tissues but is notably upregulated in response to interferons, which are cytokines critical for antiviral defense.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
GBP6 is significantly implicated in the immune response pathways, especially in the context of viral infections. It is believed to play a role in the body's defense mechanism against intracellular pathogens, including viruses. While specific diseases directly linked to GBP6 are not extensively documented, its function suggests involvement in viral infectious diseases and possibly autoimmune or inflammatory disorders. The protein is involved in pathways related to interferon signaling and modulation of the immune system.

##### Pharmacogenetics
The pharmacogenetics of GBP6 is not extensively studied as of the last updated research and knowledge bases. No direct pharmacogenetic associations with specific drugs have been robustly established. However, given GBP6's role in immune response pathways and interferon signaling, it could potentially influence the effectiveness or adverse responses to antiviral and immunomodulatory drugs. Research in this area could provide valuable insights into personalized treatment strategies for infectious and inflammatory diseases. Further pharmacogenetic investigations are required to understand its potential role in drug response and resistance mechanisms.


## Gene: HLA-DPB1
##### Gene Summary
HLA-DPB1 (Major Histocompatibility Complex, Class II, DP Beta 1) encodes a protein found in the human leukocyte antigen (HLA) system. This gene is part of the HLA complex on chromosome 6 and is crucial in the immune system's function. HLA-DPB1 is highly polymorphic, which means it has many different alleles contributing to its varied expression in the population. The protein encoded by this gene is one of the two chains of the HLA class II protein DP. It plays an essential role in the immune system's management of foreign pathogens by presenting peptides derived from extracellular proteins. HLA-DPB1 is expressed in antigen presenting cells, including dendritic cells, B cells, and macrophages.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
HLA-DPB1 is involved in the pathogenesis of several autoimmune and inflammatory conditions. Its polymorphic nature contributes to susceptibility or resistance against various diseases such as rheumatoid arthritis, juvenile diabetes, and celiac disease. Additionally, certain alleles of this gene are linked to differential responses to infectious diseases like tuberculosis and hepatitis B. Pathways involving HLA-DPB1 include immune response regulation, antigen processing and presentation. The gene's relevance extends to transplantation medicine, notably in hematopoietic stem cell transplantation, where matching donor and recipient HLA alleles, including those of HLA-DPB1, can affect graft versus host disease outcomes and transplant success.

##### Pharmacogenetics
In the realm of pharmacogenetics, HLA-DPB1 is significant mainly due to its implications in drug hypersensitivity reactions. Certain alleles of this gene are associated with adverse reactions to specific medications. For instance, the HLA-DPB1*06:01 allele has been linked to an increased risk of developing Stevens-Johnson syndrome and toxic epidermal necrolysis upon taking certain drugs. This association emphasizes the importance of genetic testing in personalized medicine to foresee potential adverse drug reactions based on an individual’s HLA-DPB1 allele profile. Also, therapeutics used in treating diseases associated with HLA-DPB1 alleles might have differential effectiveness, underscoring the need for tailored therapeutic approaches based on genetic makeup.


## Gene: ADA
##### Gene Summary
ADA (Adenosine Deaminase) is a critical enzyme involved in purine metabolism, primarily responsible for the deamination of adenosine to inosine and deoxyadenosine to deoxyinosine. This reaction plays a crucial role in the breakdown and hence the regulation of adenosine and deoxyadenosine levels in tissues. ADA is expressed ubiquitously, with significant expression in the lymphoid tissues and the gastrointestinal tract. Its activity is essential for the proliferation and maintenance of lymphocyte function, influencing immune system responses.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ADA deficiency is predominantly associated with Severe Combined Immunodeficiency (SCID), characterized by a drastic reduction in both B and T lymphocytes which leads to severe immunodeficiency and vulnerability to infectious diseases. The enzymatic activity of ADA is also pertinent to some cancers, autoimmune disorders, and pulmonary diseases due to its role in cellular metabolism and apoptosis. ADA is involved in multiple biochemical pathways including purine metabolism, adenosine salvage, and the methionine salvage pathway. This enzyme’s function impacts crucial cellular processes like DNA synthesis and repair, and therefore, its anomalies can have profound pathological effects.

##### Pharmacogenetics
The pharmacogenetic aspects of ADA primarily focus on the implications of its deficiency and the therapeutic strategies to manage ADA-linked SCID. Pegademase bovine (Adagen) is a modified bovine form of adenosine deaminase used as enzyme replacement therapy in ADA-SCID patients. This treatment has significantly improved survival and quality of life by reducing infections and mitigating metabolic abnormalities caused by ADA deficiency. Genetic variations influencing ADA activity can also affect the efficacy and toxicity of drugs that interact with purine metabolism, such as azathioprine and 6-mercaptopurine. Understanding ADA genetic mutations is also crucial for optimization of gene therapy approaches, which have been used increasingly for treating ADA-SCID, providing a functional gene copy to correct the genetic deficiency.


## Gene: SLC29A2
##### Gene Summary
SLC29A2 stands for solute carrier family 29 member 2, also known as equilibrative nucleoside transporter 2 (ENT2). This gene is a part of the equilibrative nucleoside transporters family, which plays a critical role in the transport of nucleosides and nucleobases across cellular membranes. ENT2 facilitates the bidirectional transport of nucleosides and is capable of transporting a broad spectrum of purine and pyrimidine nucleosides. SLC29A2 is expressed in a wide variety of tissues including the liver, intestine, heart, and brain. Its expression and functionality are pivotal for maintaining nucleoside homeostasis in cells and may influence various physiological processes such as purine and pyrimidine metabolism.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
SLC29A2 influences the pharmacokinetics of drugs that are nucleoside analogs, which are commonly used as antiviral or anticancer agents. This gene is implicated in several cellular and biochemical pathways, primarily involving the metabolism and transport of nucleosides and nucleotides. Diseases associated with dysregulation or mutations in SLC29A2 include certain types of cardiac abnormalities and sensitivity to infectious diseases, due to its role in nucleoside transport and metabolism. Its involvement extends to phenotypes related to drug absorption and metabolism, which can significantly affect therapeutic outcomes in treatments involving nucleoside analogs.

##### Pharmacogenetics
In the context of pharmacogenetics, SLC29A2 has significant implications due to its role in the transport of nucleoside-derived drugs. It influences the effectiveness and toxicity profiles of drugs such as cladribine, a purine nucleoside analog used primarily for treating hairy cell leukemia. Variants in the SLC29A2 gene can affect the cellular uptake and efficacy of such drugs, potentially leading to variability in treatment response among individuals. Additionally, understanding the genetic variants of SLC29A2 can help predict patient sensitivity to certain chemotherapeutic agents, which can be crucial for optimizing dosages and minimizing adverse effects. This gene's pharmacogenetic profile is important for personalized medicine, especially in cancer chemotherapy and antiviral therapies where nucleoside analogs are extensively used.


## Gene: LILRB5
##### Gene Summary
LILRB5, or leukocyte immunoglobulin-like receptor subfamily B member 5, is a gene that encodes an immunoreceptor expressed predominantly on the surfaces of certain immune cells, including monocytes and natural killer cells. This receptor is involved in the regulation of immune responses by recognizing and binding to various class I major histocompatibility complex (MHC) molecules, acting generally as an inhibitory receptor that helps to maintain immune system balance. LILRB5’s expression and functional roles in immune modulation suggest its involvement in immune tolerance and possibly the regulation of inflammatory responses.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
The expression and function of LILRB5 are linked to its role in several immune-related pathways, primarily involving the inhibition of cell activation via its interactions with MHC class I molecules. Through these interactions, it can potentially impact the pathogenesis of diseases where immune regulation and inflammation are disrupted, such as autoimmune diseases, some forms of cancer, and infectious diseases. Although specific diseases directly attributed to mutations or dysregulation of LILRB5 are not well-documented, the gene’s role in immune regulation suggests it could be significant in conditions involving immune system dysfunction.

##### Pharmacogenetics
Currently, specific pharmacogenetic associations involving LILRB5 and therapeutic drugs are limited, indicating a gap in current research that could be explored further as our understanding of immune checkpoint pathways in disease treatment, particularly in cancer immunotherapy, evolves. However, knowing the gene's regulatory role on the immune response offers a theoretical basis for considering it a potential target in developing treatments for diseases where the immune system plays a critical role. Future pharmacogenetic studies might reveal how variations in LILRB5 could affect individual responses to treatments, especially in therapies aimed at modulating immune checkpoints or treating autoimmune disorders and cancer.


## Gene: HLA-DRB5
##### Gene Summary
HLA-DRB5, part of the human leukocyte antigen system, is a component located within the Major Histocompatibility Complex (MHC) class II region on chromosome 6. This gene produces a beta-chain that is a component of the MHC class II protein complex. The MHC class II proteins play a critical role in the immune system by presenting peptides derived from extracellular proteins to T cells. Expression of HLA-DRB5 is variable and can be highly influenced by genetic polymorphism. The protein encoded by this gene forms heterodimers with the alpha chains of other DR antigens, and the combinations influence the repertoire of antigens presented which affects the immune response.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
Due to its central role in immune response modulation, HLA-DRB5 has been associated with a susceptibility to several autoimmune and inflammatory conditions, such as multiple sclerosis, rheumatoid arthritis, and possibly type 1 diabetes. The gene's product is involved in antigen presentation pathways, which are crucial for initiating specific immune responses. Variations in the presentation pathway influenced by HLA-DRB5 can result in either protective or susceptibility effects regarding these diseases.

##### Pharmacogenetics
HLA-DRB5 has important pharmacogenetic implications, particularly in the modulation of drug responses through immune mechanisms. For instance, variations in HLA-DRB5 are associated with differential responses to drugs in medical conditions like multiple sclerosis. While specific drug interactions with HLA-DRB5 are not as well characterized as for other HLA genes, the understanding of its role in disease context suggests potential influences on treatment outcomes in diseases where immune response is crucial. Consequently, studying HLA-DRB5 polymorphisms could enhance personalized treatment approaches in autoimmune diseases.


## Gene: ABCC11
##### Gene Summary
ABCC11, also known as ATP-binding cassette sub-family C member 11, is a protein-coding gene that plays a significant role in the ATP-dependent transport of various molecules across cellular membranes. This gene is involved in the transport of organic anions and drug conjugates and is particularly noted for its contribution to apocrine gland secretion. ABCC11 is expressed in numerous tissues including the liver, kidney, and especially in the apocrine glands where it affects sweat composition and earwax type.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
ABCC11 is associated with multiple phenotypic traits, the most notable being earwax type (wet or dry) which is influenced by a single nucleotide polymorphism in this gene. Differences in earwax type have been linked to varied susceptibilities to certain diseases, including breast cancer and axillary osmidrosis, where body odor becomes pronounced due to the breakdown of apocrine gland secretions. Also, pathways involving ABCC11 include those related to drug transport and metabolism, impacting the pharmacokinetics of several medicinally relevant compounds.

##### Pharmacogenetics
The pharmacogenetic relevance of ABCC11 mainly revolves around its ability to modulate the transport and efficacy of several drugs. Variant alleles of this gene have been shown to alter the effectiveness and side effects profile of certain medications. Notably, it impacts the metabolism and response to drugs like axitinib, a cancer therapy agent, by altering drug excretion rates which could potentially affect both efficacy and toxicity. In genetic testing, the status of ABCC11 can inform personalized treatment plans, particularly in cancer therapy, by predicting patient response to specific drugs based on their earwax type (and by extension, their ABCC11 genotype). This aspect of personalized medicine highlights the growing importance of understanding individual genetic backgrounds in achieving optimal therapeutic outcomes.


## Gene: SLC28A2
##### Gene Summary
SLC28A2, or solute carrier family 28 member 2, is part of the concentrative nucleoside transporter (CNT) family. Primarily expressed in the liver and kidney, SLC28A2 facilitates the active transport of nucleosides, which are key components of nucleic acids, across cell membranes. This process is essential for the salvage and recycling of nucleosides in the body. The transporter shows high affinity for purine nucleosides and pyrimidine nucleosides and also transports nucleoside-derived drugs, which are often used in antiviral and anticancer therapies.

##### Gene Drugs, Diseases, Phenotypes, and Pathways
SLC28A2 plays a critical role in the pharmacokinetics of several nucleoside analogs that are used as therapeutic agents. Dysfunction or variations in the expression of SLC28A2 are linked to alterations in drug absorption and disposition, potentially leading to variable therapeutic outcomes or toxicity. The gene is also part of significant biochemical pathways such as the purine and pyrimidine metabolism pathways which are crucial for cell viability and function. Studies suggest a potential link between the abnormal expression of SLC28A2 and certain metabolic disorders, though concrete associations with specific diseases are still under exploration.

##### Pharmacogenetics
In pharmacogenetics, SLC28A2 is particularly important due to its role in mediating the cellular uptake of drugs like ribavirin, a nucleoside analog used in the treatment of Hepatitis C, and gemcitabine, used in cancer chemotherapy. Variants in SLC28A2 can significantly affect the efficacy and toxicity of these drugs, influencing patient responses to treatment. For instance, certain allelic variants are associated with an increased risk of adverse effects from ribavirin, such as hemolytic anemia. Research into the pharmacogenetic impact of SLC28A2 is ongoing, with the goal of improving personalized medicine approaches and optimizing drug dosing to enhance therapeutic efficacy and reduce toxicity.
