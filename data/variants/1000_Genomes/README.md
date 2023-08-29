# 1000 Genomes data

This dataset comes from an original set of 564752 variants from 1000 Genomes, processed with SnpEff. The types of selected variants are the following (see [documentation](https://pcingola.github.io/SnpEff/se_inputoutput/#ann-field-vcf-output-files)):

| Effect Seq. Ontology                 | Effect Classic                      | Note and Example                                                                      | Impact   |
|-------------------------------------|-------------------------------------|--------------------------------------------------------------------------------------|----------|
| coding_sequence_variant              | CDS                                 | The variant hits a CDS.                                                               | MODIFIER |
| coding_sequence_variant              | CODON_CHANGE                        | One or many codons are changed<br>e.g.: An MNP of size multiple of 3                  | LOW      |
| Inversion                     | EXON_INVERSION                      | Inversion of an exon                                                                  | HIGH     |
| Inversion                     | EXON_INVERSION_CLASSIC              | Inversion affecting part of an exon                                                   | HIGH     |
| missense_variant                    | NON_SYNONYMOUS_START                | Variant causes a codon that produces a different amino acid<br>e.g.: Tgg/Cgg, W/R     | MODERATE |
| initiator_codon_variant              | NON_SYNONYMOUS_START                | Variant causes start codon to be mutated into another start codon (the new codon produces a different AA).<br>e.g.: Atg/Ctg, M/L (ATG and CTG can be START codons) | LOW      |
| protein_protein_contact              | PROTEIN_PROTEIN_INTERACTION_LOCUS   | Protein-Protein interaction loci.                                                     | HIGH     |
| structural_interaction_variant       | PROTEIN_STRUCTURAL_INTERACTION_LOCUS| Within protein interaction loci (e.g. two AA that are in contact within the same protein, possibly helping structural conformation). | HIGH     |
| rare_amino_acid_variant              | RARE_AMINO_ACID                     | The variant hits a rare amino acid thus is likely to produce protein loss of function | HIGH     |
| splice_acceptor_variant              | SPLICE_SITE_ACCEPTOR                | The variant hits a splice acceptor site (defined as two bases before exon start, except for the first exon). | HIGH     |
| splice_donor_variant                 | SPLICE_SITE_DONOR                   | The variant hits a Splice donor site (defined as two bases after coding exon end, except for the last exon). | HIGH     |
| stop_lost                            | STOP_LOST                           | Variant causes stop codon to be mutated into a non-stop codon<br>e.g.: Tga/Cga, */R  | HIGH     |
| start_lost                           | START_LOST                          | Variant causes start codon to be mutated into a non-start codon.<br>e.g.: aTg/aGg, M/R| HIGH     |
| stop_gained                          | STOP_GAINED                         | Variant causes a STOP codon<br>e.g.: Cag/Tag, Q/*                                    | HIGH     |

Sometimes types of mutations are selected that have more than one effect, some of which we may not have explicitly selected. For example, when selecting missense_variant, we might end up with a missense_variant&splice_region_variant (quite common). In principle, a splice_region_variant is not of interest to us because it most likely falls within an intron, and that's why we don't select it. However, if it is also annotated as a missense_variant, it means that it is having an effect at the protein level and therefore it is of interest to us. It should also be noted that there are types of variants that will never occur at the same time, for example a missense_variant (snv) and a frameshift_variant (indel). The types of variants we are seeing in the original file of 564,752 variants are as follows:

| Effect sequence ontology                         | Number of snvs |
|--------------------------------------------------|----------------|
| initiator_codon_variant                          | 98             |
| initiator_codon_variant&splice_region_variant    | 2              |
| missense_variant                                 | 548844         |
| missense_variant&splice_region_variant           | 14495          |
| rare_amino_acid_variant                          | 1              |
| start_lost                                       | 835            |
| start_lost&splice_region_variant                 | 27             |
| stop_lost                                        | 427            |
| stop_lost&splice_region_variant                  | 23             |
| **Total**                                        | **564752**     |

> This information was provided by Dr. Anna Montaner on August 9, 2023.

# Data columns

## 1. Basic Genomic Information

- **SAMPLE**: 
    - The sample ID or name for the given data row.
- **CHROM**: 
    - The chromosome on which the variant is located.
- **POS**: 
    - Position of the variant on the chromosome.
- **REF**: 
    - Reference allele.
- **ALT**: 
    - Alternate allele.
- **ID**: 
    - Variant ID, often a dbSNP rsID.

## 2. Annotations

- **ANN[*.]** columns:
    - Annotations of the variant's effect on genes and proteins, including:
        * The gene affected
        * The impact of the variant
        * The HGVS nomenclature for coding and protein changes

## 3. Population Frequency Information

### General Frequencies
- **AF, AC, NS, AN, EAS_AF, etc.**: 
    - Allele frequency, allele count, number of samples, total number of alleles, respectively, in various populations such as East Asian (EAS), European (EUR), African (AFR), American (AMR), South Asian (SAS), etc.

### Database-Specific Frequencies
- **dbNSFP_gnomAD**, **dbNSFP_1000Gp3**, **dbNSFP_ESP6500**, **dbNSFP_ExAC**:
    - Allele frequencies, counts, and other related information from major genome databases.

## 4. Variant Predictive Scores and ClinVar Information

### Predictive Scores
- **dbNSFP_CADD_phred**, **dbNSFP_Polyphen2_HDIV_score**, **dbNSFP_SIFT_score**, etc.:
    - Scores predicting the potential impact or pathogenicity of a variant. For instance, SIFT, Polyphen2, and CADD are tools used to predict whether an amino acid substitution affects protein function.

### ClinVar Data
- **dbNSFP_clinvar_** columns:
    - Data from ClinVar, a database of interpretations of clinical significance of genetic variants.

## 5. Other Annotations

- **COSV_ID**: 
    - Possibly an ID related to a specific variant database or consortium.
- **dbNSFP_Interpro_domain**: 
    - Indicates any protein domains, as per the Interpro database, that might be impacted by the variant.
