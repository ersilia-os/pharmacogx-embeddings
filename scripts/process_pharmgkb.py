import os
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))
data_folder = os.path.abspath(os.path.join(root, "..", "data", "pharmgkb"))


def stringify(x):
    if str(x) == "nan":
        return None
    else:
        return str(x)


def inline_quote_splitter(x):
    if str(x) == "nan":
        return None
    x = str(x)
    x = [x_ for x_ in x.split('"') if len(x_) > 1]
    x = [x_.rstrip(",") for x_ in x]
    return x


def inline_comma_splitter(x):
    if str(x) == "nan":
        return None
    return x.split(", ")


# chemicals table
def get_chemical_name2id():
    df = pd.read_csv(os.path.join(data_folder, "chemicals", "chemicals.csv"))
    name2id = {}
    for r in df.values:
        cid = stringify(r[0])
        name = stringify(r[1])
        if cid is None or name is None:
            continue
        name2id[name] = cid
    return name2id


# genes table
def get_gene_name2id():
    df = pd.read_csv(
        os.path.join(data_folder, "genes", "genes.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    name2id = {}
    for r in df.values:
        gid = stringify(r[0])
        name = stringify(r[5])
        if name is None or gid is None:
            continue
        name2id[name] = gid
    return name2id


# variants table
def get_variant_name2id():
    df = pd.read_csv(
        os.path.join(data_folder, "variants", "variants.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    name2id = {}
    for r in df.values:
        vid = stringify(r[0])
        name = stringify(r[1])
        if name is None or vid is None:
            continue
        name2id[name] = vid
    df = pd.read_csv(
        os.path.join(data_folder, "occurrences", "occurrences.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    df_ = df[df["Object Type"] == "Haplotype"]
    for r in df_.values:
        vid = stringify(r[-2])
        name = stringify(r[-1])
        if name is None or vid is None:
            continue
        name2id[name] = vid
    df_ = df[df["Object Type"] == "Variant"]
    for r in df_.values:
        vid = stringify(r[-2])
        name = stringify(r[-1])
        if name is None or vid is None:
            continue
        if name in name2id:
            continue
        name2id[name] = vid
    return name2id


# drug_var_ann table
def var_drug_ann():
    df = pd.read_csv(
        os.path.join(data_folder, "variantAnnotations", "var_drug_ann.csv")
    )
    R = []
    for r in df.values:
        aid = stringify(r[0])
        variants = inline_comma_splitter(r[1])
        genes = inline_quote_splitter(r[2])
        if not genes:
            continue
        drugs = inline_quote_splitter(r[3])
        if not drugs:
            continue
        pmid = stringify(r[4])
        phenotype_category = inline_quote_splitter(r[5])
        if not phenotype_category:
            phenotype_category = [None]
        significance = stringify(r[6])
        notes = stringify(r[7])
        sentence = stringify(r[8])
        alleles = stringify(r[9])
        specialty_population = stringify(r[10])
        for v in variants:
            if v not in variant_name2id:
                vid = None
            else:
                vid = variant_name2id[v]
            for g in genes:
                if g not in gene_name2id:
                    continue
                else:
                    gid = gene_name2id[g]
                for d in drugs:
                    if d not in chemical_name2id:
                        continue
                    cid = chemical_name2id[d]
                    for pc in phenotype_category:
                        r = [
                            aid,
                            vid,
                            gid,
                            cid,
                            v,
                            g,
                            d,
                            pc,
                            alleles,
                            pmid,
                            significance,
                            notes,
                            sentence,
                            specialty_population,
                        ]
                        R += [r]
    columns = [
        "aid",
        "vid",
        "gid",
        "cid",
        "variant",
        "gene",
        "chemical",
        "phenotype",
        "alleles",
        "pmid",
        "significance",
        "notes",
        "sentence",
        "specialty_population",
    ]
    return pd.DataFrame(R, columns=columns)


def gene_chem_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Gene" and et2 == "Chemical":
            gid = stringify(r[0])
            gene = stringify(r[1])
            cid = stringify(r[3])
            chemical = stringify(r[4])
        elif et1 == "Chemical" and et2 == "Gene":
            gid = stringify(r[3])
            gene = stringify(r[4])
            cid = stringify(r[0])
            chemical = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [gid, cid, gene, chemical, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "gid",
            "cid",
            "gene",
            "chemical",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


def var_chem_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Variant" and et2 == "Chemical":
            vid = stringify(r[0])
            variant = stringify(r[1])
            cid = stringify(r[3])
            chemical = stringify(r[4])
        elif et1 == "Chemical" and et2 == "Variant":
            vid = stringify(r[3])
            variant = stringify(r[4])
            cid = stringify(r[0])
            chemical = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [vid, cid, variant, chemical, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "vid",
            "cid",
            "variant",
            "chemical",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


def hapl_chem_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Haplotype" and et2 == "Chemical":
            vid = stringify(r[0])
            variant = stringify(r[1])
            cid = stringify(r[3])
            chemical = stringify(r[4])
        elif et1 == "Chemical" and et2 == "Haplotype":
            vid = stringify(r[3])
            variant = stringify(r[4])
            cid = stringify(r[0])
            chemical = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [vid, cid, variant, chemical, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "vid",
            "cid",
            "variant",
            "chemical",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


def var_gene_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Variant" and et2 == "Gene":
            vid = stringify(r[0])
            variant = stringify(r[1])
            gid = stringify(r[3])
            gene = stringify(r[4])
        elif et1 == "Gene" and et2 == "Variant":
            vid = stringify(r[3])
            variant = stringify(r[4])
            gid = stringify(r[0])
            gene = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [vid, gid, variant, gene, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "vid",
            "gid",
            "variant",
            "gene",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


def hapl_gene_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Haplotype" and et2 == "Gene":
            vid = stringify(r[0])
            variant = stringify(r[1])
            gid = stringify(r[3])
            gene = stringify(r[4])
        elif et1 == "Gene" and et2 == "Haplotype":
            vid = stringify(r[3])
            variant = stringify(r[4])
            gid = stringify(r[0])
            gene = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [vid, gid, variant, gene, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "vid",
            "gid",
            "variant",
            "gene",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


def disease_gene_relationships():
    df = pd.read_csv(
        os.path.join(data_folder, "relationships", "relationships.csv"),
        encoding="utf-8",
        encoding_errors="ignore",
    )
    R = []
    for r in df.values:
        et1 = stringify(r[2])
        et2 = stringify(r[5])
        if et1 == "Disease" and et2 == "Gene":
            did = stringify(r[0])
            disease = stringify(r[1])
            gid = stringify(r[3])
            gene = stringify(r[4])
        elif et1 == "Gene" and et2 == "Disease":
            did = stringify(r[3])
            disease = stringify(r[4])
            gid = stringify(r[0])
            gene = stringify(r[1])
        else:
            continue
        evidence = stringify(r[6]).split(",")
        association = stringify(r[7])
        pkin = stringify(r[8])
        pdyn = stringify(r[9])
        for evid in evidence:
            r = [did, gid, disease, gene, evid, association, pkin, pdyn]
            R += [r]
    df = pd.DataFrame(
        R,
        columns=[
            "did",
            "gid",
            "disease",
            "gene",
            "evidence",
            "association",
            "pk",
            "pd",
        ],
    )
    return df.drop_duplicates(inplace=False)


if __name__ == "__main__":
    chemical_name2id = get_chemical_name2id()
    gene_name2id = get_gene_name2id()
    variant_name2id = get_variant_name2id()
    print(var_drug_ann())
    print(var_chem_relationships())
    print(var_chem_relationships())
