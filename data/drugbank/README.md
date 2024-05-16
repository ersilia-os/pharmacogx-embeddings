# How to get data from DrugBank.

An academic license is required.

The following command will download data from DrugBank:
```bash
curl -Lfv -o filename.zip -u miquel@ersilia.io:PASSWORD https://go.drugbank.com/releases/5-1-12/downloads/all-full-database
```

I have manually unzipped the file and named it `full_database.xml`.