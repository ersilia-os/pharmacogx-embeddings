import os
import h5py
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root, "..", "data", "chemical_descriptors")


class CompoundStructureEmbedding(object):
    def __init__(self, embedding_type="ersilia"):
        assert embedding_type in self.available()
        self.embedding_type = embedding_type

    def available(self):
        return ["ersilia", "signaturizer", "grover"]

    def _get_ersilia_embedding(self):
        with h5py.File(
            os.path.join(data_dir, "ersilia_compound_embedding.h5"), "r"
        ) as f:
            keys = [x.decode() for x in f["Keys"][:]]
            X = f["Values"][:]
        return X, keys

    def _get_grover_embedding(self):
        with h5py.File(os.path.join(data_dir, "eos7w6n.h5"), "r") as f:
            keys = [x.decode() for x in f["Keys"][:]]
            X = f["Values"][:]
        return X, keys

    def _get_signaturizer_embedding(self):
        with h5py.File(os.path.join(data_dir, "eos4u6p.h5"), "r") as f:
            keys = [x.decode() for x in f["Keys"][:]]
            X = f["Values"][:]
        return X, keys

    def get(self, as_dataframe=True):
        if self.embedding_type == "ersilia":
            X, keys = self._get_ersilia_embedding()
        if self.embedding_type == "grover":
            X, keys = self._get_grover_embedding()
        if self.embedding_type == "signaturizer":
            X, keys = self._get_signaturizer_embedding()
        if not as_dataframe:
            return X, keys
        cols = ["key"] + ["f-{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]
        R = []
        for i in range(X.shape[0]):
            r = [keys[i]] + [r for r in X[i]]
            R += [r]
        df = pd.DataFrame(R, columns=cols)
        return df
