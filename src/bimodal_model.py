from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from lol import LOL
import joblib
import numpy as np
import shutil
import json
import os
import datetime
import random
import string


root = os.path.dirname(os.path.abspath(__file__))


def load_bimodal_stacked_model(file_name):
    df_A, df_B, reducer, model, is_fitted = joblib.load(file_name)
    mdl = BimodalStackedModel(df_A, df_B)
    mdl._is_fitted = is_fitted
    mdl.reducer = reducer
    mdl.model = model
    return mdl


class BimodalStackedModel(object):
    def __init__(self, df_A, df_B):
        self.df_A = df_A
        self.df_B = df_B
        self.dict_A = dict((r[0], r[1:]) for r in df_A.values)
        self.dict_B = dict((r[0], r[1:]) for r in df_B.values)
        self.reducer = LOL(n_components=10)
        self.model = RandomForestClassifier()
        self._is_fitted = False

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
        X = np.hstack([A, B])
        y = np.array(y_).astype(int)
        self.reducer.fit(X, y)
        X = self.reducer.transform(X)
        self.model.fit(X, y)
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
        X = np.hstack([A, B])
        X = self.reducer.transform(X)
        y_ = self.model.predict_proba(X)[:, 1]
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
        data = (self.df_A, self.df_B, self.reducer, self.model, self._is_fitted)
        joblib.dump(data, file_name)


def load_ensemble_bimodal_stacked_model(model_folder):
    emb = joblib.load(os.path.join(model_folder, "embeddings.joblib"))
    cemb_list = emb["cemb_list"]
    pemb_list = emb["pemb_list"]
    model = EnsembleBimodalStackedModel(cemb_list, pemb_list, model_folder=model_folder)
    return model


class EnsembleBimodalStackedModel(object):
    def __init__(self, cemb_list, pemb_list, model_folder=None):
        self.cemb_list = cemb_list
        self.pemb_list = pemb_list
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
        return os.path.join(self.model_folder, "embeddings.joblib")

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
        for i in range(X.shape[0]):
            r = X[i, :]
            mask = ~np.isnan(r)
            if np.any(mask):
                y += [np.mean(r[mask])]
            else:
                y += [np.nan]
        y = np.array(y)
        return y

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
        for i in range(X.shape[0]):
            r = X[i, :]
            mask = ~np.isnan(r)
            if np.any(mask):
                y += [np.average(r[mask], weights=weights[mask])]
            else:
                y += [np.nan]
        y = np.array(y)
        return y

    def fit(self, df):
        for cemb in self.cemb_list:
            for pemb in self.pemb_list:
                name = self.get_name(cemb[0], pemb[0])
                model = BimodalStackedModel(cemb[1], pemb[1])
                print("Fitting:", name)
                model.fit(df)
                model.save(self.get_filename(name))

    def evaluate(self, df):
        data = {}
        pred_stack = {}
        for cemb in self.cemb_list:
            for pemb in self.pemb_list:
                name = self.get_name(cemb[0], pemb[0])
                file_name = self.get_filename(name)
                if not os.path.exists(file_name):
                    continue
                model = load_bimodal_stacked_model(file_name)
                results = model.evaluate(df)
                print(name, results["n_eval"], results["auroc"])
                data[name] = {"auroc": results["auroc"], "n_eval": results["n_eval"]}
                pred_stack[name] = np.array(results["data"]["y_hat"])
        y_hat = self.average(pred_stack)
        y_hat_w = self.weighted_average(pred_stack, data)
        data["average"] = self._get_roc_auc_score(df, y_hat)
        data["weighted_average"] = self._get_roc_auc_score(df, y_hat_w)
        with open(self.get_evaluation_filename(), "w") as f:
            json.dump(data, f, indent=4)
        print(json.dumps(data, indent=4))
        return data

    def predict(self, df):
        pred_stack = {}
        for cemb in self.cemb_list:
            for pemb in self.pemb_list:
                name = self.get_name(cemb[0], pemb[0])
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
            y_hat = self.average(pred_stack)
        else:
            y_hat = self.weighted_average(pred_stack, eval_data)
        df["y_hat"] = y_hat
        return df

    def save(self):
        data = {
            "cemb_list": self.cemb_list,
            "pemb_list": self.pemb_list,
        }
        joblib.dump(data, self.get_embeddings_filename())
