import random
import pandas as pd


class PositiveNegativeSampler(object):
    def __init__(self, df, neg_ratio=10):
        self.df = df
        self.columns = list(df.columns)
        self.cid_dict = dict(
            (v[1], list(v)) for v in df[["inchikey", "cid", "chemical"]].values
        )
        self.gid_dict = dict(
            (v[2], list(v)) for v in df[["uniprot_ac", "gene", "gid"]].values
        )
        self.neg_ratio = neg_ratio
        self.pairs = list(set([tuple(x) for x in self.df[["cid", "gid"]].values]))
        self.pairs_set = set(self.pairs)
        self.expected_negatives = int(len(self.pairs_set) * neg_ratio) + 1
        self._sampling_trials = 1000

    def sample(self):
        neg_pairs = set()
        for _ in range(self._sampling_trials):
            x = list([x[0] for x in self.pairs])
            y = list([y[1] for y in self.pairs])
            random.shuffle(x)
            rand_pairs = set([(x_, y_) for x_, y_ in zip(x, y)]).difference(
                self.pairs_set
            )
            neg_pairs.update(rand_pairs)
            if len(neg_pairs) >= self.expected_negatives:
                neg_pairs = random.sample(list(neg_pairs), self.expected_negatives)
                break
        all_pairs = self.pairs + neg_pairs
        y = [1] * len(self.pairs) + [0] * len(neg_pairs)
        idxs = [i for i in range(len(y))]
        random.shuffle(idxs)
        all_pairs = [all_pairs[i] for i in idxs]
        y = [y[i] for i in idxs]
        R = []
        for p, v in zip(all_pairs, y):
            r = list(self.cid_dict[p[0]]) + list(self.gid_dict[p[1]]) + [v]
            R += [r]
        df = pd.DataFrame(
            R, columns=["inchikey", "cid", "chemical", "uniprot_ac", "gene", "gid", "y"]
        )
        return df
