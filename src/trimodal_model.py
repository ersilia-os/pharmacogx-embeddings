# WIP - untested

import numpy as np
from sklearn.ensemble import RandomForestClassifier


class TrimodalStackedModel(object):
    def __init__(self, df_A, df_B, df_C):
        self.dict_A = dict((r[0], r[1:]) for r in df_A.values)
        self.dict_B = df_B((r[0], r[1:]) for r in df_B.values)
        self.dict_C = df_C((r[0], r[1:]) for r in df_C.values)
        self.model = RandomForestClassifier

    def fit(self, triplets, y):
        A = []
        B = []
        C = []
        y_ = []
        for i, t in enumerate(triplets):
            if t[0] not in self.dict_A:
                continue
            if t[1] not in self.dict_B:
                continue
            if t[2] not in self.dict_C:
                continue
            A += [self.dict_A[t[0]]]
            B += [self.dict_B[t[1]]]
            C += [self.dict_C[t[2]]]
            y_ += [y[i]]
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        X = np.hstack([A, B, C])
        y = np.array(y).astype(np.int)
        self.model.fit(X, y)

    def predict(self, triplets):
        A = []
        B = []
        C = []
        idxs = []
        for i, t in enumerate(triplets):
            if t[0] not in self.dict_A:
                continue
            if t[1] not in self.dict_B:
                continue
            if t[2] not in self.dict_C:
                continue
            A += [self.dict_A[t[0]]]
            B += [self.dict_B[t[1]]]
            C += [self.dict_C[t[2]]]
            idxs += [i]
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        X = np.hstack([A, B, C])
        y_ = self.model.predict_proba(X)[:, 1]
        y_hat = np.full((len(triplets),), np.nan)
        y_hat[idxs] = y_
        return y_hat
