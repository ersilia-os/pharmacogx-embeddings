import pandas as pd
import numpy as np
import re
import os
from tqdm import tqdm
from biogpt import BioGPTEmbedder
from protein_sequences import ProteinSequencePerResidueEmbedding

root = os.path.dirname(os.path.abspath(__file__))


class SnpEffTableEncoder(object):
    def __init__(self, subset):
        assert subset in self.available()
        self.subset = subset

    def available(self):
        return ["basic", "population", "prediction", "other"]

    def _basic(self, data):
        embedder = BioGPTEmbedder()

        df = data
        gene_biotypes = {
            "Protein-coding related": {
                "protein_coding": "Genes that code for proteins.",
                "nonsense_mediated_decay": "Genes with transcripts that are subject to Nonsense-Mediated Decay.",
                "non_stop_decay": "Transcripts that have an open reading frame but lack a stop codon.",
                "ambiguous_orf": "Transcripts with an uncertain coding potential.",
                "disrupted_domain": "Transcripts that contain a frameshift within their coding sequence.",
            },
            "Non-coding RNA genes": {
                "lncRNA": "Long non-coding RNA genes.",
                "miRNA": "MicroRNA genes, which produce small RNAs involved in gene silencing.",
                "snRNA": "Small nuclear RNA genes, usually involved in splicing.",
                "snoRNA": "Small nucleolar RNA genes, mainly involved in rRNA modification.",
                "rRNA": "Ribosomal RNA genes.",
                "tRNA": "Transfer RNA genes.",
                "pseudogene": "Non-functional sequences that resemble functional genes.",
                "Mt_tRNA": "Mitochondrial tRNA genes.",
                "Mt_rRNA": "Mitochondrial rRNA genes.",
            },
            "Immunoglobulin/T-cell receptor genes": {
                "IG_C_gene": "Immunoglobulin Constant gene.",
                "IG_D_gene": "Immunoglobulin Diversity gene.",
                "IG_J_gene": "Immunoglobulin Joining gene.",
                "IG_V_gene": "Immunoglobulin Variable gene.",
                "TR_C_gene": "T-cell receptor Constant gene.",
                "TR_D_gene": "T-cell receptor Diversity gene.",
                "TR_J_gene": "T-cell receptor Joining gene.",
                "TR_V_gene": "T-cell receptor Variable gene.",
            },
            "Other types": {
                "misc_RNA": "Miscellaneous RNA genes not classified elsewhere.",
                "scaRNA": "Small Cajal body-specific RNA genes.",
                "vaultRNA": "Vault RNA genes.",
                "bidirectional_promoter_lncRNA": "Non-coding RNA genes that originate from bidirectional promoters.",
                "retained_intron": "Transcripts that retain an intron.",
            },
            "Pseudogenes": {
                "processed_pseudogene": "Pseudogenes derived from retrotransposition.",
                "unprocessed_pseudogene": "Direct duplications of genes.",
                "polymorphic_pseudogene": "Pseudogenes with some functional alleles in the population.",
                "transcribed_processed_pseudogene": "Transcribed processed pseudogenes.",
                "transcribed_unprocessed_pseudogene": "Transcribed unprocessed pseudogenes.",
                "transcribed_unitary_pseudogene": "Transcribed pseudogenes with no functional counterparts.",
                "unitary_pseudogene": "Pseudogenes with no functional counterparts in the genome.",
            },
            "Others": {
                "TEC": "To be Experimentally Confirmed.",
                "macro_lncRNA": "Very long non-coding RNA genes.",
            },
        }

        gene_biotypes = dict(
            (l, w) for k, v in gene_biotypes.items() for l, w in v.items()
        )

        columns = list(df.columns)

        basic_columns = columns[slice(0, columns.index("ANN[*].ERRORS") + 1)]

        texts = []

        for r in df[basic_columns].values:
            text = ""
            c = r[basic_columns.index("CHROM")]
            if c == ".":
                text += "Variant with no known chromosome. "
            else:
                text += "Variant on chromosome {0}. ".format(c)
            text += "Reference allele is {0} and variant allele is {1}. ".format(
                r[basic_columns.index("REF")], r[basic_columns.index("ALT")]
            )
            text += "Annotated gene is {0}. ".format(
                r[basic_columns.index("ANN[*].GENE")]
            )
            feat = r[basic_columns.index("ANN[*].FEATURE")]
            text += "It is reported on a {0}. ".format(feat)
            biot = r[basic_columns.index("ANN[*].BIOTYPE")]
            if biot in gene_biotypes:
                text += "The biotype is {0}. ".format(gene_biotypes[biot].rstrip("."))
            eff = r[basic_columns.index("ANN[*].EFFECT")].replace("_", " ")
            imp = r[basic_columns.index("ANN[*].IMPACT")].lower()
            rnk = r[basic_columns.index("ANN[*].RANK")]
            text += "The effect is {0} with a {1} impact ranked {2}. ".format(
                eff, imp, rnk
            )
            hgvs = r[basic_columns.index("ANN[*].HGVS_P")]
            if hgvs != ".":
                text += "The point mutation is {0}. ".format(hgvs)
            text = text.rstrip(" ")
            texts += [text]

        return embedder.calculate(texts)

    def _frequency(self, data):
        df = data
        columns = list(df.columns)
        population_frequencies_columns = columns[
            slice(columns.index("AF"), columns.index("dbNSFP_ExAC_SAS_AF") + 1)
        ]
        dfreq = pd.DataFrame(df[population_frequencies_columns])
        X_freq = np.array(dfreq)
        return X_freq

    def _predictions(self, data):
        df = data
        columns = list(df.columns)
        prediction_scores_columns = columns[
            slice(
                columns.index("dbNSFP_CADD_phred"),
                columns.index("dbNSFP_VEST4_score") + 1,
            )
        ]
        df["dbNSFP_Polyphen2_HDIV_pred"].replace({"B": 0, "P": 1, "D": 2}, inplace=True)
        df["dbNSFP_SIFT_pred"].replace({"D": 1, "T": 0}, inplace=True)
        df["dbNSFP_MutationAssessor_pred"].replace(
            {"H": 3, "M": 2, "L": 1, "N": 0}, inplace=True
        )
        df["dbNSFP_MutationTaster_pred"].replace(
            {"A": 2, "D": 1, "N": 0, "P": 0}, inplace=True
        )

        def calculate_value(s):
            values = s.split(",")
            values = [v for v in values if v != "."]
            if not values:
                return float("NaN")
            mean_value = sum([1 if v == "D" else 0 for v in values]) / len(values)
            return mean_value

        df["dbNSFP_PROVEAN_pred"] = df["dbNSFP_PROVEAN_pred"].apply(calculate_value)
        dpred = pd.DataFrame(df[prediction_scores_columns])
        dpred.replace(".", np.nan, inplace=True)
        X_pred = np.array(dpred)
        return X_pred

    def _other(self, data):
        embedder = BioGPTEmbedder()
        df = data
        texts = []
        for v in df[
            ["dbNSFP_clinvar_clnsig", "dbNSFP_clinvar_trait", "COSV_ID"]
        ].values:
            t = ""
            if v[0] != ".":
                t += "The clinical relevance of the variant is {0}. ".format(v[0])
            else:
                t += "The clinical relevance of the variant is not annotated. "
            if v[1] != ".":
                t += "The traits are {0}. ".format(v[1].replace("_", " "))
            else:
                t += "No traits are known. "
            if v[2] != ".":
                t += "The affected domains of the variant in COSMIC are {0}.".format(
                    v[2]
                )
            else:
                t += "No domains in COSMIC."
            texts += [t]
        X_other = embedder.calculate(texts)
        return X_other

    def calculate(self, data):
        if self.subset == "basic":
            return self._basic(data)
        if self.subset == "population":
            return self._frequency(data)
        if self.subset == "prediction":
            return self._predictions(data)
        if self.subset == "other":
            return self._other(data)


class SnpEffMissensePositionEmbedding(object):
    def __init__(self):
        self.embedder = ProteinSequencePerResidueEmbedding(embedding_type="uniprot")

    def _extract_position(self, string):
        string = str(string)
        if not string.startswith("p."):
            return None
        match = re.search(r"\d+", string)
        if match:
            return int(match.group())
        else:
            return None

    def _extract_positions(self, mutations):
        positions = []
        for m in mutations:
            positions += [self._extract_position(m)]
        return positions

    def _map_genes_name_to_uniprot_acs(self, genes):
        g2p = {}
        df = pd.read_csv(
            os.path.join(
                root, "..", "data", "other", "human_proteome_with_genenames.tab"
            ),
            sep="\t",
        )
        for v in df[
            ["Entry", "Gene names", "Gene names  (primary )", "Gene names  (synonym )"]
        ].values:
            p = v[0]
            g = []
            for x in v[1:]:
                x = str(x)
                if x == "nan":
                    continue
                for y in x.split(" "):
                    g += [y]
            for x in g:
                g2p[x] = p
        uniprot_acs = []
        for gene in genes:
            if gene not in g2p:
                uniprot_acs += [None]
            else:
                uniprot_acs += [g2p[gene]]
        return uniprot_acs

    def get(self, data):
        genes = data["ANN[*].GENE"].tolist()
        mutations = data["ANN[*].HGVS_P"].tolist()
        uniprot_acs = self._map_genes_name_to_uniprot_acs(genes)
        positions = self._extract_positions(mutations)
        X = np.full((len(uniprot_acs), 1024), np.nan)
        for i in tqdm(range(len(uniprot_acs))):
            prot = uniprot_acs[i]
            pos = positions[i]
            if prot is None:
                continue
            if pos is None:
                continue
            try:
                d = self.embedder.get([prot])[prot]
                X[i, :] = d[pos - 1]
            except:
                continue
        return X


class VariantEmbedding(object):
    def __init__(self, embedding_type="snpeff_basic"):
        assert embedding_type in self.available()
        self.embedding_type = embedding_type

    def available(self):
        return [
            "snpeff_basic",
            "snpeff_population",
            "snpeff_prediction",
            "snpeff_other",
            "uniprot_missense",
        ]

    def _get_snpeff_basic_emb(self):
        encoder = SnpEffTableEncoder("basic")
        X, keys = encoder.calculate()
        return X, keys

    def _get_snpeff_population_emb(self):
        encoder = SnpEffTableEncoder("population")
        X, keys = encoder.calculate()
        return X, keys

    def _get_snpeff_prediction_emb(self):
        encoder = SnpEffTableEncoder("prediction")
        X, keys = encoder.calculate()
        return X, keys

    def _get_snpeff_other_emb(self):
        encoder = SnpEffTableEncoder("other")
        X, keys = encoder.calculate()
        return X, keys

    def _get_uniprot_missense_emb(self):
        encoder = SnpEffMissensePositionEmbedding()
        X, keys = encoder.get()
        return X, keys

    def get(self, as_dataframe=True):
        if self.embedding_type == "snpeff_basic":
            X, keys = self._get_snpeff_basic_emb()
        if self.embedding_type == "snpeff_population":
            X, keys = self._get_snpeff_population_emb()
        if self.embedding_type == "snpeff_prediction":
            X, keys = self._get_snpeff_prediction_emb()
        if self.embedding_type == "snpeff_other":
            X, keys = self._get_snpeff_other_emb()
        if self.embedding_type == "uniprot_missense":
            X, keys = self._get_uniprot_missense_emb()
        if not as_dataframe:
            return X, keys
        cols = ["key"] + ["f-{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]
        R = []
        for i in range(X.shape[0]):
            r = [keys[i]] + [r for r in X[i]]
            R += [r]
        df = pd.DataFrame(R, columns=cols)
        return df
