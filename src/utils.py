import re
import h5py
import os
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.feature_selection import VarianceThreshold
import joblib


class CsvCleaner:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _str(x):
        if str(x) == "nan":
            return None
        if str(x) == "":
            return None
        if str(x) == "None":
            return None
        else:
            return str(x)

    def stringify(self, x):
        return self._str(x)

    def inline_quote_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        x = sorted(set([y for x_ in x for y in x_.split(" / ")]))
        return x

    def inline_quote_splitter_noslash(self, x):
        x = self._str(x)
        if x is None:
            return None
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        return x

    def inline_comma_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(",")

    def inline_comma_splitter_space(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(", ")

    def inline_semicolon_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(";")

    def inline_semicolon_splitter_space(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split("; ")

    def inline_comma_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        x = self._str(x)
        if x is None:
            return None
        else:
            elements = re.split(r",(?!\s)", x)
            if elements is None:
                return None
            else:
                # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements

    def inline_semicolon_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        x = self._str(x)
        if x is None:
            return None
        else:
            elements = re.split(r";(?!\s)", x)
            if elements is None:
                return None
            else:
                # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements


MAX_NA = 0.2


class NanFilter(object):
    def __init__(self):
        self._name = "nan_filter"

    def fit(self, X):
        max_na = int((1 - MAX_NA) * X.shape[0])
        idxs = []
        for j in range(X.shape[1]):
            c = np.sum(np.isnan(X[:, j]))
            if c > max_na:
                continue
            else:
                idxs += [j]
        self.col_idxs = idxs

    def transform(self, X):
        return X[:, self.col_idxs]

    def save(self, file_name):
        joblib.dump(self, file_name)

    def load(self, file_name):
        return joblib.load(file_name)


class Imputer(object):
    def __init__(self):
        self._name = "imputer"
        self._fallback = 0

    def fit(self, X):
        ms = []
        for j in range(X.shape[1]):
            vals = X[:, j]
            mask = ~np.isnan(vals)
            vals = vals[mask]
            if len(vals) == 0:
                m = self._fallback
            else:
                m = np.median(vals)
            ms += [m]
        self.impute_values = np.array(ms)

    def transform(self, X):
        for j in range(X.shape[1]):
            mask = np.isnan(X[:, j])
            X[mask, j] = self.impute_values[j]
        return X

    def save(self, file_name):
        joblib.dump(self, file_name)

    def load(self, file_name):
        return joblib.load(file_name)


class VarianceFilter(object):
    def __init__(self):
        self._name = "variance_filter"

    def fit(self, X):
        self.sel = VarianceThreshold()
        self.sel.fit(X)
        self.col_idxs = self.sel.transform([[i for i in range(X.shape[1])]]).ravel()

    def transform(self, X):
        return self.sel.transform(X)

    def save(self, file_name):
        joblib.dump(self, file_name)

    def load(self, file_name):
        return joblib.load(file_name)


class Normalizer(object):
    def __init__(self):
        self.nan_filter = NanFilter()
        self.imputer = Imputer()
        self.variance_filter = VarianceFilter()
        self.discretizer = KBinsDiscretizer(
            n_bins=16, encode="ordinal", strategy="quantile"
        )

    def fit(self, X):
        X = np.array(X, dtype=np.float32)
        self.nan_filter.fit(X)
        X = self.nan_filter.transform(X)
        self.imputer.fit(X)
        X = self.imputer.transform(X)
        self.variance_filter.fit(X)
        X = self.variance_filter.transform(X)
        self.discretizer.fit(X)

    def transform(self, X):
        X = np.array(X, dtype=np.float32)
        X = self.nan_filter.transform(X)
        X = self.imputer.transform(X)
        X = self.variance_filter.transform(X)
        X = self.discretizer.transform(X)
        return np.array(X, dtype=int)


class H5Normalizer(object):
    def __init__(self, h5_file):
        self.h5_file = os.path.abspath(h5_file)
        self.h5_output_file = self.h5_file[:-3] + "_norm.h5"
        self.normalizer = Normalizer()

    def run(self):
        with h5py.File(self.h5_file, "r") as f:
            print(f.keys())
            X = f["Values"][:]
            keys = f["Keys"][:]
            inputs = f["Inputs"][:]
            features = f["Features"][:]
            keys = [k.decode() for k in keys]
            inputs = [i.decode() for i in inputs]
            features = [feat.decode() for feat in features]
        self.normalizer.fit(X)
        X = self.normalizer.transform(X)
        with h5py.File(self.h5_output_file, "w") as f:
            f.create_dataset("Values", data=X)
            f.create_dataset("Keys", data=np.array(keys, dtype=h5py.string_dtype()))
            f.create_dataset("Inputs", data=np.array(inputs, dtype=h5py.string_dtype()))
            f.create_dataset(
                "Features", data=np.array(features, dtype=h5py.string_dtype())
            )
