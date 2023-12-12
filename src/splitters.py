import random
import pandas as pd
import collections


class RandomSplitter(object):
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


class RandomPairSplitter(RandomSplitter):
    def __init__(self, test_size=0.2):
        RandomSplitter.__init__(self, test_size=test_size)


class RandomTripletSplitter(RandomSplitter):
    def __init__(self, test_size=0.2):
        RandomSplitter.__init__(self, test_size=test_size)


class LeaveColumnOutSplitter(object):
    def __init__(self, column_name, test_size=0.2):
        self.test_size = test_size
        self.column_name = column_name

    def split(self, df):
        column_idx = list(df.columns).index(self.column_name)
        data = collections.defaultdict(list)
        for r in df.values:
            k = r[column_idx]
            data[k] += [list(r)]
        keys = list(data.keys())
        idxs = [i for i in range(len(keys))]
        random.shuffle(idxs)
        n_tr = int(len(idxs) * (1 - self.test_size)) + 1
        idxs_tr = idxs[:n_tr]
        idxs_te = idxs[n_tr:]
        R_tr = [data[keys[idx]] for idx in idxs_tr]
        R_te = [data[keys[idx]] for idx in idxs_te]
        df_tr = pd.DataFrame(R_tr, columns=list(df.columns))
        df_te = pd.DataFrame(R_te, columns=list(df.columns))
        return df_tr, df_te


class LeaveGenesOutPairSplitter(LeaveColumnOutSplitter):
    def __init__(self, test_size=0.2):
        LeaveColumnOutSplitter.__init__(self, column_name="gid", test_size=test_size)


class LeaveDrugsOutPairSplitter(LeaveColumnOutSplitter):
    def __init__(self, test_size=0.2):
        LeaveColumnOutSplitter.__init__(self, column_name="cid", test_size=test_size)


class LeaveGenesOutTripletSplitter(LeaveColumnOutSplitter):
    def __init__(self, test_size=0.2):
        LeaveColumnOutSplitter.__init__(self, column_name="gid", test_size=test_size)


class LeaveDrugsOutTripletSplitter(LeaveColumnOutSplitter):
    def __init__(self, test_size=0.2):
        LeaveColumnOutSplitter.__init__(self, column_name="cid", test_size=test_size)


class LeaveVariantsOutTripletSplitter(LeaveColumnOutSplitter):
    def __init__(self, test_size=0.2):
        LeaveColumnOutSplitter.__init__(self, column_name="vid", test_size=test_size)
