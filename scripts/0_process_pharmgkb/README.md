# Building a KG from PharmGKB
This folder contains the necessary scripts to process the raw data downloaded from PharmGKB (assumed in .csv format). The end goal is to deconvolute all associations so that we have a final table with *gene - variant - compound-evidence* (and associated PharmGKB ID's for easy querying).

There are a few fields that have been converted to numerical. In general:
* 1: Yes
* -1: No
* 0: Not Stated

The processing starts with the _simple_ files:

`0_chemical.py` takes the chemicals.csv file and queries Pubmed to obtain all the SMILES. Returns the name, ID (cid), SMILES, dosing_guideline and drug label (1 to 4, from more to less informative, -1 if not existing). Many chemicals do not have the SMILES available. This is solved by first, querying the PharmGKB API and, if not found, querying PubMed. Combinations of drugs remain as combination (hence, no SMILES available) and chemical types such as Drug Class could be further deconvoluted into its composing drugs.

`0_disease.py` takes the phenotypes.csv file and gets the disease and its ID (did)

`0_gene.py` takes the genes.csv file and gets the gene and several of its identifiers (gid, hgnc_id, ensemble_id). Also collects if it is a very important gene (vip), if it has dosing guidelines and if it has variant annotations.

`manual_tables.py` manually creates the tables Biogeographical group and evidence.csv for reference #NEEDED?

Then, to properly deconvolute the field variant/haplotype, we need to make sure that each haplotype is associated to all the variants it contains. For it, we need to process the haplotypes and make sure we have all of them and the gene they are associated to:
`1_haplotype_from_rlx.py` gets the haplotypes present in the relationships.csv file (haplotype, hid) and obtains also the gene to which the haplotype or variant relates to. Gene ID (gid) is pulled from the 0_gene.csv file. This is used as a way of getting all genes with associated haplotypes, because we will systematically download and process all haplotypes using the API (there are 24k genes and only 1.5k with variant/haplotype information, so we want to save resources in downloading the individual haplotype information). Haplotypes not associated with any gene will not be considered.

`2_download_haplotype.py`gets all the genes that have any haplotype associated (from 0_haplotype_rlx.csv) and saves the {gene}_allele_definition_table as a xlsx (original) and csv files in the pharmgkb/haplotyes/original. Genes for which the file is not downloadable are saved in the no_file.csv and curated manually afterwards, and their .csvs added in the folder pharmgkb/haplotypes/original.

`3_haplotype_from_url.py` gets the haplotypes downloaded from PharmGKB and processes them individually, creating the processed_pharmgkb/haplotypes/{gene_name}_haplotypes.csv file. This also adds the haplotype ID from PharmGKB. The manual_curation.csv contains haplotypes for which the default API URL is not working, in this case we have manually added the HID by searching the database.

`4_haplotype.py` finally gets all the processed haplotype files and merges them also checking for any that might be only present in the 1_haplotype_rlx.csv file. It joins with more gene information from 0_gene.csv to create the 2_haplotype.csv master file (haplotype, hid, gene, gid and other information about the start/stop of the haplotype etc if available)

`5_haplotype_to_variant.py` gets the variants of each haplotype from an online query and deconvolutes any missing or double haplotype-variant pairs, to get the hid_vid_complete.csv file (hap-hid-var-vid). Each haplotype will correspond to several vids.

Then, we look into the variants:

`6_variant.py` starting from the original variants.csv downloaded from PharmGKB, obtains the genes corresponding to each variant using an API query and deconvolutes them (if var1 is associated to gene1 and gene2, there will be two lines with var1|vid1, one per gene). It also gets the gene ID (gid) from the 0_genes.csv file

`6_orphan_vars.py` uses a manually curated list of variants that have popped up during the data analysis and are not found in the variants.csv file provided by PharmGKB and creates the 4_oprhan_vars.csv file, with the same structure as 4_variant.csv

`7_variant_complete.py` joins 4_variant.csv, and 4_orphan_vars.csv into a single one using the [variant, vid, gene, gid] fields. This is the master variant file for reference.

Then we process the other files to deconvolute the gene-variant-chemical associations (in this first step, we separate the vid from hid, which are used together in pharmgkb tables). These are the files: `clinical_annotation.py`, `clinical_variant.py`, `drug_labels.py`,  `var_pheno_ann.py`, `var_drug_ann.py`, `clinical_ann_allele.py`, `autom_ann.py`

`study_parameters.py`gets the parameters of individual studies, most importantly biogeographical groups 


## Final tables
Final tables are created to keep only the following fields: ["cid","chemical","smiles","gid","gene","ensembl_id","vid","variant","evidence","significance","phenotype","did","disease","biogroup","caid","vaid"]
Here, we do separate the haplotypes into each of its variants using the hid_vid_complete.csv file

The merged files are currently:
Clinical_annotation, Clinical_variant, Drug_labels, Var_pheno_ann, Var_drug_ann, Autom_ann

In addition, the variant_assembly.py is used to gather more information on the variants (from all_variants.csv, which contains both independent and haplotype variants) for processing on the genome pipelines

`variant_assembly.py` takes all the variants and adds information about them using an online query 