import os
import pandas as pd

root = os.path.abspath(os.path.dirname(__file__))


class Chemical(object):
    def __init__(self, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(root, "..", "data")
        else:
            self.data_path = os.path.abspath(data_path)
        self._pgkb_id = None
        self._pgkb_folder = os.path.join(self.data_path, "pharmgkb")
        self._overview = None
        self._prescribing_info = None
        self._drug_label_annotations = None
        self._clinical_annotations = None
        self._variant_annotations = None
        self._literature = None
        self._pathways = None
        self._related_genes = None
        self._related_diseases = None
        self._automated_variant_annotations = None

    def get_all_pgkb_ids(self):
        df = pd.read_csv(os.path.join(self._pgkb_folder, "chemicals", "chemicals.tsv"), delimiters="\t")
        return df["PharmGKB "].tolist()

    @property
    def pgkb_id(self):
        if self._pgkb_id is not None:
            return self._pgkb_id

    @property
    def overview(self):
        if self._overview is not None:
            return self._overview
        df = pd.read_csv(os.path.join(self._pgkb_folder, "chemicals", "chemicals.tsv"), delimiter="\t")
        df = df[df["PharmGKB"] == self._pgkb_id]
        assert (df.shape[0] == 1)
        data
        return df

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


