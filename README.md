# PharmacoGx Embeddings
Calculate drug, gene, variant and disease graph embeddings based on pharmacogenomics knowledge.

## Project overview



## Knowledge graph

The knowledge graph leverages mainly [PharmGKB](https://pharmgkb.org) and the [Bioteque](https://bioteque.org):
* **PharmGKB** is used as a source of pharmacogenomics knowledge, and is the core 

### Ontology



### Statistics

#### PharmacoGx core


#### Peripheral (orthogonal data) graph




### Python API

We have written 

```python
from pgxembeddings import Chemical

ch = Chemical()
ch.name = "izoniazid"

print(ch.get_associated_variants())
```

## About Us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission or [volunteer](https://www.ersilia.io/volunteer) with us!
