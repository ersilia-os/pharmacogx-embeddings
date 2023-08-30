# Protein embeddings

This folder contains embeddings downloaded or generated with external sources, mainly large language models applied to protein sequences.

In particular:
* `human_proteome_esm1b.h5`: Was generated locally with the [ESM-1b](https://github.com/facebookresearch/esm) model. The command to produce this embeddings was: `python esm/extract.py esm1b_t33_650M_UR50S pid2seq1000.fasta pid2seq1000 --repr_layers 0 32 33 --include mean per_tok`
* `human_proteome_prots5.h5`: Was downloaded from [this](https://zenodo.org/record/5047020#.ZDQUqOxBz0o) precomputed source (`reduced_embeddings_file.h5`)
* `uniprot_embeddings.h5`: Was downloaded [from UniProt](https://www.uniprot.org/help/downloads#embeddings).

We provide functionality to read these precalculated embeddings.