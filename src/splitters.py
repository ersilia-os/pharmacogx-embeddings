import random
import pandas as pd


class RandomPairSplitter(object):
    def __init__(self, test_size=0.2):
        self.test_size = test_size

    def split(self, df):
        idxs = [i for i in range(df.shape[0])]
        random.shuffle(idxs)
        n_tr = int(len(idxs) * (1 - self.test_size)) + 1
        idxs_tr = idxs[:n_tr]
        idxs_te = idxs[n_tr:]
        R = []
        for r in df.values:
            R += [list(r)]
        R_tr = [R[i] for i in idxs_tr]
        R_te = [R[i] for i in idxs_te]
        df_tr = pd.DataFrame(R_tr, columns=list(df.columns))
        df_te = pd.DataFrame(R_te, columns=list(df.columns))
        return df_tr, df_te
