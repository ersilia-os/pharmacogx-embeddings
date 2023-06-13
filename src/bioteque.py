import h5py
import os
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
bioteque_path = os.path.abspath(os.path.join(root, "..", "data", "bioteque"))


class BiotequeGeneEmbeddings(object):
    def __init__(self, metapath, dataset):
        self.metapath = metapath
        self.dataset = dataset
        self.h5_file = os.path.join(bioteque_path, metapath, dataset, "GEN_emb.h5")
        self.ids_file = os.path.join(bioteque_path, metapath, dataset, "GEN_ids.txt")

    def available(self):
        R = []
        for fn in os.listdir(bioteque_path):
            if not os.path.isdir(os.path.join(bioteque_path, fn)):
                continue
            for fm in os.listdir(os.path.join(bioteque_path, fn)):
                R += [(fn, fm)]
        df = pd.DataFrame(R, columns=["metapath", "dataset"])
        return df

    def get(self, as_dataframe=True):
        with h5py.File(self.h5_file, "r") as f:
            X = f["m"][:]
        keys = []
        with open(self.ids_file, "r") as f:
            for l in f:
                keys += [l.rstrip()]
        if not as_dataframe:
            return X, keys
        cols = ["key"] + ["f-{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]
        R = []
        for i in range(X.shape[0]):
            r = [keys[i]] + [r for r in X[i]]
            R += [r]
        df = pd.DataFrame(R, columns=cols)
        return df
