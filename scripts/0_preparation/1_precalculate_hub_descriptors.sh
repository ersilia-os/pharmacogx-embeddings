# Bash script to fetch and precalculate the descriptors for molecules
# can be edited to incorporate more descriptors

#ersilia -v fetch eos4u6p 
ersilia serve eos4u6p
ersilia -v run -i "$1/drug_molecules.csv" -o "$1/eos4u6p.h5"

ersilia -v fetch eos2gw4
ersilia serve eos2gw4
ersilia -v run -i "$1/drug_molecules.csv" -o "$1/eos2gw4.h5"

ersilia -v fetch eos8a4x
ersilia serve eos8a4x
ersilia -v run -i "$1/drug_molecules.csv" -o "$1/eos8a4x.h5"