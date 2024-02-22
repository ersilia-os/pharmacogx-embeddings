import os
import h5py
import numpy as np
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(root, "..", "data", "protein_models")


class ProteinSequenceEmbedding(object):
    def __init__(self, embedding_type="esm1b"):
        assert embedding_type in self.available()
        self.embedding_type = embedding_type

    def available(self):
        return ["esm1b", "uniprot"]

    def _get_prots5(self):
        with h5py.File(os.path.join(data_folder, "human_proteome_prots5.h5"), "r") as f:
            keys = [k for k in f.keys()]
            uniprot_acs = []
            X = np.zeros((len(keys), 1024), dtype=np.float32)
            for i, k in enumerate(keys):
                uniprot_ac = f[k].attrs["original_id"].split("|")[1]
                uniprot_acs += [uniprot_ac]
                X[i, :] = np.array(f[k][:], dtype=np.float32)
        return X, uniprot_acs

    def _get_esm1b(self):
        with h5py.File(os.path.join(data_folder, "human_proteome_esm1b.h5"), "r") as f:
            uniprot_acs = [x.decode() for x in f["Keys"][:]]
            X = f["Values"][:]
        return X, uniprot_acs

    def _get_uniprot(self):
        with h5py.File(
            os.path.join(data_folder, "human_proteome_uniprot.h5"), "r"
        ) as f:
            X = np.zeros((len(f.items()), 1024))
            uniprot_acs = []
            for i, r in enumerate(f.items()):
                uniprot_acs += [r[0]]
                X[i, :] = np.array(r[1])
        return X, uniprot_acs

    def get(self, as_dataframe=True):
        if self.embedding_type == "esm1b":
            X, keys = self._get_esm1b()
        if self.embedding_type == "prot5":
            X, keys = self._get_prots5()
        if self.embedding_type == "uniprot":
            X, keys = self._get_uniprot()
        if not as_dataframe:
            return X, keys
        cols = ["key"] + ["f-{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]
        R = []
        for i in range(X.shape[0]):
            r = [keys[i]] + [r for r in X[i]]
            R += [r]
        df = pd.DataFrame(R, columns=cols)
        return df
