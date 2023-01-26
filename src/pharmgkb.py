import os
import pandas as pd
import csv

root = os.path.abspath(os.path.dirname(__file__))


class RawData(object):
    """
    This class reads the files downloaded from PharmGKB on the indicated CREATED_DATE.
    The folder and file structure is maintaind from PharmGKB.
    .tsv files have been manually converted to .csv files using Excel to avoid endline errors.
    """

    def __init__(self, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")
        self.reset()

    def reset(self):
        self._automated_annotations = None
        self._chemicals = None
        self._clinical_ann_alleles = None
        self._clinical_ann_evidence = None
        self._clinical_ann_history = None
        self._clinical_annotations = None
        self._clinical_variants = None
        self._genes = None
        self._var_drug_ann = None

    @property
    def automated_annotations(self):
        if self._automated_annotations is not None:
            return self._automated_annotations
        file_name = os.path.join(
            self._pgkb_folder, "automated_annotations", "automated_annotations.csv"
        )
        self._automated_annotations = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._automated_annotations

    @property
    def chemicals(self):
        if self._chemicals is not None:
            return self._chemicals
        file_name = os.path.join(self._pgkb_folder, "chemicals", "chemicals.csv")
        self._chemicals = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._chemicals

    @property
    def clinical_ann_alleles(self):
        if self._clinical_ann_alleles is not None:
            return self._clinical_ann_alleles
        file_name = os.path.join(
            self._pgkb_folder, "clinicalAnnotations", "clinical_ann_alleles.csv"
        )
        self._clinical_ann_alleles = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._clinical_ann_alleles

    @property
    def clinical_ann_evidence(self):
        if self._clinical_ann_evidence is not None:
            return self._clinical_ann_evidence
        file_name = os.path.join(
            self._pgkb_folder, "clinicalAnnotations", "clinical_ann_evidence.csv"
        )
        self._clinical_ann_evidence = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._clinical_ann_evidence

    @property
    def clinical_ann_history(self):
        if self._clinical_ann_history is not None:
            return self._clinical_ann_history
        file_name = os.path.join(
            self._pgkb_folder, "clinicalAnnotations", "clinical_ann_history.csv"
        )
        self._clinical_ann_history = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._clinical_ann_history

    @property
    def clinical_annotations(self):
        if self._clinical_annotations is not None:
            return self._clinical_annotations
        file_name = os.path.join(
            self._pgkb_folder, "clinicalAnnotations", "clinical_annotations.csv"
        )
        self._clinical_annotations = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._clinical_annotations

    @property
    def clinical_variants(self):
        if self._clinical_variants is not None:
            return self._clinical_variants
        file_name = os.path.join(
            self._pgkb_folder, "clinicalVariants", "clinical_variants.csv"
        )
        self._clinical_variants = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._clinical_variants

    @property
    def genes(self):
        if self._genes is not None:
            return self._genes
        file_name = os.path.join(self._pgkb_folder, "genes", "genes.csv")
        self._genes = pd.read_csv(file_name, encoding="utf-8", encoding_errors="ignore")
        return self._genes

    @property
    def var_drug_ann(self):
        if self._var_drug_ann is not None:
            return self._var_drug_ann
        file_name = os.path.join(
            self._pgkb_folder, "variantAnnotations", "var_drug_ann.csv"
        )
        self._var_drug_ann = pd.read_csv(
            file_name, encoding="utf-8", encoding_errors="ignore"
        )
        return self._var_drug_ann


class Chemical(RawData):
    def __init__(self, data_path=None):
        RawData.__init__(self, data_path=data_path)
        self._pgkb_id = None

    def get_all_pgkb_ids(self):
        df = pd.read_csv(
            os.path.join(self._pgkb_folder, "chemicals", "chemicals.tsv"),
            delimiters="\t",
        )
        return df["PharmGKB Accession Id"].tolist()

    @property
    def pgkb_id(self):
        if self._pgkb_id is not None:
            return self._pgkb_id

    @pgkb_id.setter
    def pgkb_id(self, pgkb_id):
        self._pgkb_id = pgkb_id

    @property
    def overview(self):
        if self._overview is not None:
            return self._overview
        df = pd.read_csv(
            os.path.join(self._pgkb_folder, "chemicals", "chemicals.tsv"),
            delimiter="\t",
        )
        df = df[df["PharmGKB Accession Id"] == self._pgkb_id]
        assert df.shape[0] == 1
        data = {"Type": df["Type"].tolist()[0], "SMILES": df["SMILES"].tolist()[0]}
        self._overview = data
        return self._overview

    @property
    def prescribing_info(self):
        if self._prescribing_info is not None:
            return self._prescribing_info
        pass

    @property
    def drug_label_annotations(self):
        if self._drug_label_annotations is not None:
            return self._drug_label_annotations

    @property
    def clinical_annotations(self):
        if self._clinical_annotations is not None:
            return self._clinical_annotations

    @property
    def variant_annotations(self):
        if self._variant_annotations is not None:
            return self._variant_annotations
        file_name = os.path.join(
            self._pgkb_folder, "variantAnnotations", "var_drug_ann.csv"
        )
        df = pd.read_csv(file_name)
        print(df[df["Drug(s)"] == "warfarin"])

    @property
    def literature(self):
        if self._literature is not None:
            return self._literature

    @property
    def pathways(self):
        if self._pathways is not None:
            return self._pathways

    @property
    def related_genes(self):
        if self._related_genes is not None:
            return self._related_genes

    @property
    def related_diseases(self):
        if self._related_diseases is not None:
            return self._related_diseases

    @property
    def automated_variant_annotations(self):
        if self._automated_variant_annotations is not None:
            return self._automated_variant_annotations


class Gene(object):
    def __init__(self, pgkb_id, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_id = pgkb_id
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")


class Variant(object):
    def __init__(self, pgkb_id, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_id = pgkb_id
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")


class Haplotype(object):
    def __init__(self, pgkb_id, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_id = pgkb_id
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")


class Disease(object):
    def __init__(self, pgkb_id, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_id = pgkb_id
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")
