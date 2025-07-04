import os
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
import joblib
import topicwizard
import seaborn as sns
import matplotlib.pyplot as plt

TFIDF = True

SCOPE = "all_outcomes_all_genes"

root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(root, "..", "..","data")) #use original data
results_dir = os.path.abspath(os.path.join(root, "..", "results", "topicmodeling_two", SCOPE)) #save new results
if not os.path.exists(results_dir):
    os.makedirs(results_dir, exist_ok=True)

df = pd.read_csv(os.path.join(data_dir, "ml_datasets_matrix", "df_{0}.csv".format(SCOPE)))

print(df.shape)

prot_names_df = pd.read_csv(os.path.join(data_dir, "other", "pgkb_gene_uniprot_mapping.tsv"), sep="\t")

prot2gene = {}
for v in prot_names_df.values:
    prot2gene[v[2]] = v[1]

df.rename(columns=prot2gene, inplace=True)

inchikeys = list(df["Unnamed: 0"])
df = df.drop(columns=["Unnamed: 0"], inplace=False)
df.index = inchikeys

# Create documents
documents_list = []
cols = list(df.columns)
kept_idxs = []

# OLD WEIGHTS
# 1-9: weight 1
# 10-49: weight 2
# 50+: weight 3
"""
for j, v in enumerate(df.values):
    document = []
    for i, x in enumerate(v):
        if x == 0:
            continue
        elif x < 10:
            n = 1
        elif x < 50:
            n = 2
        else:
            n = 3
        document += [cols[i]] * n
    if len(set(document)) < 5:
        continue
    kept_idxs.append(j)
    documents_list += [" ".join(document)]
"""
# WEIGHTS ONE
# 1-4: weight 1
# 5-14: weight 2
# 15-39: weight 3
# 40-99: weight 4
# 100+: weight 5

for j, v in enumerate(df.values):
    document = []
    for i, x in enumerate(v):
        if x == 0:
            continue
        elif x <= 4:
            n = 1
        elif x <= 14:
            n = 2
        elif x <= 39:
            n = 3
        elif x <= 99:
            n = 4
        else:
            n = 5
        document += [cols[i]] * n
    if len(set(document)) < 5:
        continue
    kept_idxs.append(j)
    documents_list += [" ".join(document)]

# WEIGHTS TWO
# 1-10: weight 1
# 11-20: weight 2
# 21-30: weight 3
# 31-40: weight 4
# 41-50: weight 5
# 51-60: weight 6
# 61-70: weight 7
# 71-80: weight 8
# 81-90: weight 9
# 91-100: weight 10
# 100+: weight 11

for j, v in enumerate(df.values):
    document = []
    for i, x in enumerate(v):
        if x == 0:
            continue
        elif x <= 10:
            n = 1
        elif x <= 20:
            n = 2
        elif x <= 30:
            n = 3
        elif x <= 40:
            n = 4
        elif x <= 50:
            n = 5
        elif x <= 60:
            n = 6
        elif x <= 70:
            n = 7
        elif x <= 80:
            n = 8
        elif x <= 90:
            n = 9
        elif x <= 100:
            n = 10
        else:
            n = 11
        document += [cols[i]] * n
    if len(set(document)) < 5:
        continue
    kept_idxs.append(j)
    documents_list += [" ".join(document)]

def create_documents():
    f0 = open("{0}/compound_docs.txt".format(results_dir), "w")
    f1 = open("{0}/inchikeys.txt".format(results_dir), "w")
    for i, g in enumerate(documents_list):
        f0.write(g + "\n")
        f1.write(inchikeys[kept_idxs[i]] + "\n")
    f0.close()
    f1.close()

create_documents()

# Topic modeling

def tokenizer(x):
    return x.split(" ")

if not TFIDF:
    vectorizer = CountVectorizer(lowercase=False, tokenizer=tokenizer)
else:
    vectorizer = TfidfVectorizer(lowercase=False, tokenizer=tokenizer)

def get_texts():
    with open("{0}/compound_docs.txt".format(results_dir), "r") as f:
        texts = [x.rstrip() for x in f.readlines()]
    return texts

def get_doc_names():
    with open("{0}/inchikeys.txt".format(results_dir), "r") as f:
        doc_names = [x.rstrip() for x in f.readlines()]
    return doc_names

texts = get_texts()
doc_names = get_doc_names()
 
def fit_topic_pipeline(num_topics):
    mdl = NMF(n_components=num_topics, max_iter=10000)
    topic_pipeline = Pipeline(
       [
          ("vec", vectorizer),
          ("mdl", mdl),
       ]
    )
    texts = get_texts()
    topic_pipeline.fit(texts)
    return topic_pipeline

NUM_TOPICS = 10
topic_pipeline = fit_topic_pipeline(num_topics=NUM_TOPICS)
vec = topic_pipeline["vec"]
mdl = topic_pipeline["mdl"]
    
data_for_wizard = {"corpus": texts, "pipeline": topic_pipeline, "document_names": doc_names}

joblib.dump(data_for_wizard, os.path.join(results_dir, "data_for_wizard.joblib"))

data_for_wizard = joblib.load(os.path.join(results_dir, "data_for_wizard.joblib"))

topic_names = ["Topic {0}".format(i) for i in range(NUM_TOPICS)]

topic_data = {
    "document_names": doc_names,
    "corpus": texts,
    "vectorizer": vec,
    "topic_model": mdl,
    "topic_names": topic_names
}

print(topic_names)

joblib.dump(topic_data, os.path.join(results_dir, "topic_data.joblib"))

topic_data = joblib.load(os.path.join(results_dir, "topic_data.joblib"))

document_names = topic_data["document_names"]
corpus = topic_data["corpus"]
vectorizer = topic_data["vectorizer"]
topic_model = topic_data["topic_model"]
topic_names = topic_data["topic_names"]

vocab = topicwizard.prepare.utils.get_vocab(vectorizer)
document_term_matrix, document_topic_matrix, topic_term_matrix = topicwizard.prepare.utils.prepare_transformed_data(vectorizer, topic_model, corpus)
topic_importances, term_importances, topic_term_importances = topicwizard.prepare.topics.topic_importances(topic_term_matrix, document_term_matrix, document_topic_matrix)

word_pos = topicwizard.prepare.words.word_positions(topic_term_matrix)
R = []
for i,t in enumerate(vocab):
    r = [t] + [term_importances[i]] + [word_pos[0][i], word_pos[1][i]] + [x for x in topic_term_importances[:,i]]
    R += [r]

d_ = pd.DataFrame(R, columns=["gene_name", "importance"] + ["proj_x", "proj_y"] + topic_names)
d_.to_csv(os.path.join(results_dir, "ProteinHasTopic.csv"), index=False)

R = []
for i,t in enumerate(topic_names):
    R += [t] + [topic_importances[i]]

doc_pos = topicwizard.prepare.documents.document_positions(document_term_matrix)

ik2smi = pd.read_csv(os.path.join(data_dir, "chemical_descriptors", "drug_molecules.csv"))
ik2smi = dict(zip(ik2smi["inchikey"], ik2smi["smiles"]))

R = []
for i in range(len(doc_names)):
    ik_ = doc_names[i]
    smi_ = ik2smi[ik_]
    r = [ik_, smi_] + [doc_pos[0][i], doc_pos[1][i]] + [x for x in document_topic_matrix[i]]
    R += [r]

d_ = pd.DataFrame(R, columns=["inchikey", "smiles"] + ["proj_x", "proj_y"] + topic_names)
d_.to_csv(os.path.join(results_dir, "CompoundHasTopic.csv"), index=False)

processed_topicwizard_data = {
    "vocab": vocab,
    "document_term_matrix": document_term_matrix,
    "document_topic_matrix": document_topic_matrix,
    "topic_term_matrix": topic_term_matrix,
    "topic_importances": topic_importances,
    "term_importances": term_importances,
    "topic_term_importances": topic_term_importances,
    "document_topic_importances": topicwizard.prepare.documents.document_topic_importances(document_topic_matrix)
}

joblib.dump(processed_topicwizard_data, os.path.join(results_dir, "processed_topicwizard_data.joblib"))

W = document_topic_matrix

## Plotting
print("Plotting")

sns.clustermap(pd.DataFrame(W, index=document_names, columns=topic_names), cmap="YlGnBu")

plt.savefig(os.path.join(results_dir, "heatmap_docs_topic.png"), dpi=600)

H = topic_term_importances.T
sns.clustermap(pd.DataFrame(H, index=vocab, columns=topic_names), cmap="YlGnBu")

plt.savefig(os.path.join(results_dir, "heatmap_words_topic.png"), dpi=600)