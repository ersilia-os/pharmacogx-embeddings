# PharmacoGx Embeddings
Calculate drug, gene, variant and disease graph embeddings based on pharmacogenomics knowledge.

## :construction: This is library is in continuous development and it is currently intended for internal use. We are currently working on it. Stay tuned! :contruction: 

## Project overview

![Project overview](assets/GradientProposalScheme-01.png)

## Knowledge graph

The knowledge graph leverages mainly [PharmGKB](https://pharmgkb.org) and the [Bioteque](https://bioteque.org):
* **PharmGKB** is used as a source of pharmacogenomics knowledge, and is the core 

### Ontology

We have adapted the light-weight pharmacogenomics ontology ([PGxO](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2693-9)) to capture the main PharmacoGx relationships and concepts in our knowledge graph. To the template PGxO, we have added edges related to levels of evidence, population genetics, etc.

![PGx Ontology]()

### Statistics

#### PharmacoGx core graph



#### Peripheral (orthogonal data) graph


## Installation instructions

This is a Python based package. The repository can be installed with `pip` as follows.

```bash
git clone https://github.com/ersilia-os/pharmacogx-embeddings
cd pharmacogx-embeddings
python -m pip install -e .
```

## Python API

We have written 

```python
from pgxembeddings import Chemical

ch = Chemical()
ch.name = "izoniazid"

print(ch.get_associated_variants())
```

## Repository structure

* `data`: 
* `scripts`: 
* `notebooks`:

## About Us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission or [volunteer](https://www.ersilia.io/volunteer) with us!
