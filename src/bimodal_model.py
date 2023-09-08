from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from lol import LOL
import joblib
import numpy as np
import shutil
import json
import os
import datetime
import random
import string
from flaml.default import LGBMClassifier as ZeroShotBaseClassifier
from lightgbm import LGBMClassifier as BaseClassifier


root = os.path.dirname(os.path.abspath(__file__))


def load_base_bimodal_model(file_name):
    single_reducer_1, single_reducer_2, stacked_reducer, model = joblib.load(file_name)
    mdl = BaseBimodalModel()
    mdl.single_reducer_1 = single_reducer_1
    mdl.single_reducer_2 = single_reducer_2
    mdl.stacked_reducer = stacked_reducer
    mdl.model = model
    return mdl


class BaseBimodalModel(object):
    def __init__(
        self,
        n_components_single_reducer_1=100,
        n_components_single_reducer_2=100,
        n_components_stacked_reducer=50,
    ):
        self.n_components_single_reducer_1 = n_components_single_reducer_1
        self.n_components_single_reducer_2 = n_components_single_reducer_2
        self.n_components_stacked_reducer = n_components_stacked_reducer

    def fit(self, X1, X2, y):
        if X1.shape[1] < self.n_components_single_reducer_1:
            self.n_components_single_reducer_1 = X1.shape[1]
        if X2.shape[1] < self.n_components_single_reducer_2:
            self.n_components_single_reducer_2 = X2.shape[1]
        ncs = self.n_components_single_reducer_1 + self.n_components_single_reducer_2
        if ncs < self.n_components_stacked_reducer:
            self.n_components_stacked_reducer = ncs
        self.single_reducer_1 = PCA(
            n_components=self.n_components_single_reducer_1, svd_solver="randomized"
        )
        self.single_reducer_2 = PCA(
            n_components=self.n_components_single_reducer_2, svd_solver="randomized"
        )
        self.stacked_reducer = LOL(n_components=self.n_components_stacked_reducer)
        print("... single reducer 1")
        X1 = self.single_reducer_1.fit_transform(X1)
        print("... single reducer 2")
        X2 = self.single_reducer_2.fit_transform(X2)
        print("... stacked reducer")
        X = np.hstack([X1, X2])
        X = self.stacked_reducer.fit_transform(X, y)
        print("... classifier", X.shape)
        hyperparameters = ZeroShotBaseClassifier().suggest_hyperparams(X, y)[0]
        self.model = BaseClassifier(**hyperparameters)
        self.model.fit(X, y)
        print("... fitting done")

    def predict(self, X1, X2):
        X1 = self.single_reducer_1.transform(X1)
        X2 = self.single_reducer_2.transform(X2)
        X = np.hstack([X1, X2])
        X = self.stacked_reducer.transform(X)
        return self.model.predict(X)

    def predict_proba(self, X1, X2):
        X1 = self.single_reducer_1.transform(X1)
        X2 = self.single_reducer_2.transform(X2)
        X = np.hstack([X1, X2])
        X = self.stacked_reducer.transform(X)
        return self.model.predict_proba(X)

    def save(self, file_name):
        data = (
            self.single_reducer_1,
            self.single_reducer_2,
            self.stacked_reducer,
            self.model,
        )
        joblib.dump(data, file_name)


def load_bimodal_stacked_model(file_name):
    emb_name_A, emb_name_B, model_file_name, is_fitted = joblib.load(file_name)
    mdl = BimodalStackedModel(emb_name_A, emb_name_B)
    mdl._is_fitted = is_fitted
    mdl.model = load_base_bimodal_model(model_file_name)
    return mdl


class BimodalStackedModel(object):
    def __init__(self, emb_name_A, emb_name_B):
        self.emb_name_A = emb_name_A
        self.emb_name_B = emb_name_B
        self.df_A = self.load_embedding_df(emb_name_A)
        self.df_B = self.load_embedding_df(emb_name_B)
        self.dict_A = dict((r[0], r[1:]) for r in self.df_A.values)
        self.dict_B = dict((r[0], r[1:]) for r in self.df_B.values)
        self.model = BaseBimodalModel()
        self._is_fitted = False

    def load_embedding_df(self, emb_name):
        embeddings_folder = os.path.join(root, "..", "embeddings")
        for l in os.listdir(embeddings_folder):
            if not l.endswith(".joblib"):
                continue
            l_ = l.split("---")[1].split(".joblib")[0]
            if l_ == emb_name:
                file_name = os.path.join(embeddings_folder, l)
        file_name = os.path.abspath(file_name)
        df = joblib.load(file_name)
        return df

    def fit(self, df):
        pairs = np.array(df[["inchikey", "uniprot_ac"]].values)
        y = np.array(df["y"])
        A = []
        B = []
        y_ = []
        for i, t in enumerate(pairs):
            if t[0] not in self.dict_A:
                continue
            if t[1] not in self.dict_B:
                continue
            A += [self.dict_A[t[0]]]
            B += [self.dict_B[t[1]]]
            y_ += [y[i]]
        A = np.array(A)
        B = np.array(B)
        y = np.array(y_).astype(int)
        self.model.fit(A, B, y)
        self._is_fitted = True

    def predict(self, df):
        assert self._is_fitted
        pairs = np.array(df[["inchikey", "uniprot_ac"]])
        A = []
        B = []
        idxs = []
        for i, t in enumerate(pairs):
            if t[0] not in self.dict_A:
                continue
            if t[1] not in self.dict_B:
                continue
            A += [self.dict_A[t[0]]]
            B += [self.dict_B[t[1]]]
            idxs += [i]
        A = np.array(A)
        B = np.array(B)
        y_ = self.model.predict_proba(A, B)[:, 1]
        y_hat = np.full((len(pairs),), np.nan)
        y_hat[idxs] = y_
        df["y_hat"] = y_hat
        return df

    def evaluate(self, df):
        df = self.predict(df)
        y_hat = np.array(df["y_hat"])
        y = np.array(df["y"])
        idxs = [i for i in range(len(y_hat)) if not np.isnan(y_hat[i])]
        y_hat = [y_hat[i] for i in idxs]
        y = [y[i] for i in idxs]
        auroc = roc_auc_score(y, y_hat)
        n = len(y)
        results = {"data": df, "auroc": auroc, "n_eval": n}
        return results

    def save(self, file_name):
        model_file_name = file_name.split(".joblib")[0] + "_base.joblib"
        self.model.save(model_file_name)
        data = (
            self.emb_name_A,
            self.emb_name_B,
            model_file_name,
            self._is_fitted,
        )
        joblib.dump(data, file_name)


def get_embedding_names():
    with open(
        os.path.join(root, "..", "embeddings", "available_embeddings.json"), "r"
    ) as f:
        return json.load(f)


def load_ensemble_bimodal_stacked_model(model_folder):
    emb = joblib.load(os.path.join(model_folder, "embeddings.joblib"))
    cemb_list = emb["cemb_list"]
    pemb_list = emb["pemb_list"]
    model = EnsembleBimodalStackedModel(cemb_list, pemb_list, model_folder=model_folder)
    return model


class EnsembleBimodalStackedModel(object):
    def __init__(self, emb_name_list_A, emb_name_list_B, model_folder=None):
        self.emb_name_list_A = emb_name_list_A
        self.emb_name_list_B = emb_name_list_B
        if model_folder is None:
            model_folder = os.path.join(
                root, "..", "models", self.generate_folder_name()
            )
            self.model_folder = model_folder
            if os.path.exists(model_folder):
                shutil.rmtree(model_folder)
            os.makedirs(model_folder)
            self.save()
        else:
            if not os.path.exists(model_folder):
                os.makedirs(model_folder)
                self.model_folder = model_folder
                self.save()
            else:
                self.model_folder = model_folder

    def generate_folder_name(self):
        dt_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        rand_string = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(5)
        )
        folder_name = f"{dt_string}_{rand_string}"
        return folder_name

    def get_name(self, cn, pn):
        if type(pn) is str:
            return cn + "---" + pn
        else:
            return cn + "---" + "--".join(list(pn))

    def get_filename(self, name):
        return os.path.join(self.model_folder, name + ".joblib")

    def get_evaluation_filename(self):
        return os.path.join(self.model_folder, "evaluation.json")

    def get_embeddings_filename(self):
        return os.path.join(self.model_folder, "embeddings.json")

    def _get_roc_auc_score(self, df, y_hat):
        y_hat = np.array(y_hat)
        y = np.array(df["y"])
        idxs = [i for i in range(len(y_hat)) if not np.isnan(y_hat[i])]
        y_hat = [y_hat[i] for i in idxs]
        y = [y[i] for i in idxs]
        auroc = roc_auc_score(y, y_hat)
        return {"auroc": auroc, "n_eval": len(y)}

    def average(self, pred_stack):
        R = []
        for _, r in pred_stack.items():
            R += [r]
        X = np.array(R).T
        y = []
        supports = []
        for i in range(X.shape[0]):
            r = X[i, :]
            mask = ~np.isnan(r)
            if np.any(mask):
                y += [np.mean(r[mask])]
                supports += np.sum(mask)
            else:
                y += [np.nan]
                supports += [0]
        y = np.array(y)
        supports = np.array(supports)
        return y, supports

    def weighted_average(self, pred_stack, eval_data):
        keys = sorted(pred_stack.keys())
        aurocs = [eval_data[k]["auroc"] for k in keys]
        aurocs = np.clip(aurocs, 0.5, 1)
        weights = np.array([(x - 0.5) / 0.5 for x in aurocs])
        R = []
        for k in keys:
            r = np.array(pred_stack[k])
            R += [r]
        X = np.array(R).T
        y = []
        supports = []
        for i in range(X.shape[0]):
            r = X[i, :]
            mask = ~np.isnan(r)
            if np.any(mask):
                y += [np.average(r[mask], weights=weights[mask])]
                supports += [np.sum(weights[mask])]
            else:
                y += [np.nan]
                supports += [0]
        y = np.array(y)
        supports = np.array(supports)
        return y, supports

    def fit(self, df):
        for emb_name_A in self.emb_name_list_A:
            for emb_name_B in self.emb_name_list_B:
                name = self.get_name(emb_name_A, emb_name_B)
                model = BimodalStackedModel(emb_name_A, emb_name_B)
                print("Fitting:", name)
                model.fit(df)
                model.save(self.get_filename(name))

    def evaluate(self, df):
        data = {}
        pred_stack = {}
        for emb_name_A in self.emb_name_list_A:
            for emb_name_B in self.emb_name_list_B:
                name = self.get_name(emb_name_A, emb_name_B)
                file_name = self.get_filename(name)
                if not os.path.exists(file_name):
                    continue
                model = load_bimodal_stacked_model(file_name)
                results = model.evaluate(df)
                print(name, results["n_eval"], results["auroc"])
                data[name] = {"auroc": results["auroc"], "n_eval": results["n_eval"]}
                pred_stack[name] = np.array(results["data"]["y_hat"])
        y_hat, _ = self.average(pred_stack)
        y_hat_w, _ = self.weighted_average(pred_stack, data)
        data["average"] = self._get_roc_auc_score(df, y_hat)
        data["weighted_average"] = self._get_roc_auc_score(df, y_hat_w)
        with open(self.get_evaluation_filename(), "w") as f:
            json.dump(data, f, indent=4)
        print(json.dumps(data, indent=4))
        return data

    def predict(self, df):
        pred_stack = {}
        for emb_name_A in self.emb_name_list_A:
            for emb_name_B in self.emb_name_list_B:
                name = self.get_name(emb_name_A, emb_name_B)
                file_name = self.get_filename(name)
                if not os.path.exists(file_name):
                    continue
                model = load_bimodal_stacked_model(file_name)
                df = model.predict(df)
                pred_stack[name] = np.array(df["y_hat"])
        eval_file = self.get_evaluation_filename()
        if os.path.exists(eval_file):
            with open(eval_file, "r") as f:
                eval_data = json.load(f)
        else:
            eval_data = None
        if eval_data is None:
            y_hat, supports = self.average(pred_stack)
        else:
            y_hat, supports = self.weighted_average(pred_stack, eval_data)
        df["y_hat"] = y_hat
        df["support"] = supports
        return df

    def save(self):
        data = {
            "emb_name_list_A": self.emb_name_list_A,
            "emb_name_list_B": self.emb_name_list_B,
        }
        with open(self.get_embeddings_filename(), "w") as f:
            json.dump(data, f, indent=4)
