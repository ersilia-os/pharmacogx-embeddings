# Bash script to fetch and precalculate the descriptors for molecules
# can be edited to incorporate more descriptors

ersilia -v fetch $1
ersilia serve $1
ersilia -v run -i "$2/drug_molecules.csv" -o "$2/$1.h5"