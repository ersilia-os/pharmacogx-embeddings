# Curation of data

We compare the data curated using our pipeline with the data that can be retrieved online in PharmGKB (keep in mind data was accessed on January 2023, so slight additions in the online version are expected).

## Drug annotations
We randomly select 10 chemical compounds (see `00_PharmGKB_DataCleaning.ipynb`) and obtain a summary of the information collected from that compound.

### PA450640
Genes:     1
Variants:  172

* Name: Nitrofurantoin
* Prescribing Info: 2 (Annotation of CPIC Guideline for nitrofurantoin and G6PD)
* Drug Label Annotations: 3 (FDA, HCSC, Swissmedic for G6PD)
* Clinical Annotations: 1 (Haplotype G6PD A- 202A_376G, which has two SNP annotated:rs1050829, rs1050828) Level 3
* Variant Annotations: 4 (all on G6PD deficiency)

We find 127 unique variants because these are all the variants associated to the Reference allele of G6PD, which actually DOES NOT have significance. This might be an isolated case of the G6PD, but I have added a check to eliminate "reference" alleles. It seems only G6PD is easily labelled as reference or wiltdype. --> Should we add this check across all data (i.e in the variant_processing file)? For example, for warfarin, CYP2C9 gene allele *1 is described as the WT allele, so should its variants not be annotated as significant?

Also, we only find evidence 3, but there are actually DRUG LABEL annotations, so these are not level 3 but 1A, why we are not capturing this? - The drug labels did not have the evidence information, so this gets lost. I have now added the evidence level 1A (variant available) or 1B (no variant) to all drug-gene combinations that are found in the drug_labels table.

Check the warfain example - variant rs9923231 from VKROC gene has several similar annotations at different evidence levels. How do we collate that?

There are some haplotypes, at least in automated annotations, that do not appead in the hid_vid_complete file nor on pharmgkb when searching, so they will be eliminated from the list (like CYP2D6*4H, POR37 or VKORC*1). 
Check some associations of variants that are only from one gene but appear linked to more than one? (PRSS53 with variant rs7294 from VKROC, or gene BCKDK and variant rs9923231 - test automated annotations)
To be sure, since we are deconvoluting the genes as follows: if two genes appear but only one variant is mentioned, both genes will be associated to that variant. We use as source truth the variant_complete file, and then if the gene-variant association is not found there we leave the gene only and add a None in the variant vid fields.



We are adding the study group to the variant_drug_annotation and the variant_phenotype_annotation to get the biogroup, but if this is not relevant (we get the variant uniqueness from the variant analysis by Anna) we can remove the vaid and eliminate the duplicates (which are really a lot)


I have created a variants_processing file with general functions, such as the cleaning of the specific HLA variants and/or G6PD variants, with functions that can be reused across scripts