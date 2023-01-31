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

