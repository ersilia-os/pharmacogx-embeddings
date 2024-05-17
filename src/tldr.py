import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

root = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(root, "..", ".env"))

OPENAI_MODEL = "gpt-4-turbo"


class DrugTLDR(object):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _system_prompt(self):
        prompt = """
            You are a pharmacogenetics experts. You are asked to provide a summary of a given drug.
            You will be provided with two pieces of information: (a) one or multiple drug names and (b) a JSON object containing information from DrugBank, including text data as well as targets, enzymes, transporters and carriers.
            You should use the information in (b) but you should also use your own knowledge to provide a summary of the drug as specified in (a).
            Do not restrict yourself to DrugBank information, especially for pharmacogentics and pharmacogenomics. Other useful resources are PharmGKB, FDA drug labels and the scientific literature.
            Feel free to infer pharmacogenetic interactions, but clarify if you are making an inference.
            In case the JSON object is empty, just proceed based on your own knowledge. Do not raise any error message.
            Your summary should be structured as follows:
                - A brief summary of the drug, including its name, therapeutic class, and general knowledge about its pharmacokinetics, pharmacodynamics and metabolism
                - A brief summary of the drug's targets, enzymes, transporters, and carriers.
                - A brief summary of the drug's pharmacogenetics, including any known pharmacogenetic associations.
            Be as succinct as possible. Your response should be at most 500 words long. Do not use full gene names. Use the official gene symbols.
            Structure your answer in three paragraphs, in markdown format (header ## for each paragraph, no number) as follows:
                1. Drug Summary
                2. Drug Targets, Enzymes, Transporters, and Carriers
                3. Pharmacogenetics
            Strictly limit yourself to these 3 paragraphs.
            """
        return prompt.rstrip().lstrip().replace("    ", "")

    def _user_prompt(self, drug):
        json_file = os.path.join(root, "..", "data", "drugbank", "json", f"{drug}.json")
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                data = json.load(f)
                drug_name = ", ".join(data["names"])
        else:
            drug_name = drug
            data = {}
        prompt = """
            Provide a summary of the drug given the following information:
            (a) Drug name: {0}
            (b) DrugBank information: {1}
            """.format(drug_name, data)
        return prompt.rstrip().lstrip().replace("    ", "")

    def get(self, drug):
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": self._user_prompt(drug)},
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content
    


class GeneTLDR(object):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _system_prompt(self):
        prompt = """
            You are a pharmacogenetics expert. You are asked to provide a summary of a given gene. You will be provided with a gene symbol.
            You should use your own knowledge to provide a summary of the gene. Useful resources include PharmGKB, UniProt, Gene Cards, and the scientific literature.
            Your summary should be structured as follows:
                - A brief summary of the gene, including its official symbol, official name, and general knowledge about its function and expression
                - A brief summary of the gene's drugs, diseases, phenotypes, and pathways.
                - A brief summary of the gene's pharmacogenetics, including any known pharmacogenetic associations with drugs. Mention as many drugs as possible
            Be as succinct as possible. Your response should be at most 500 words long. Do not use full gene names. Use the official gene symbols.
            Structure your answer in three paragraphs, in markdown format (header ## for each paragraph, no number, no *) as follows:
                1. Gene Summary
                2. Gene Drugs, Diseases, Phenotypes, and Pathways
                3. Pharmacogenetics
            Striclty limit yourself to these 3 paragraphs.
            """
        return prompt.rstrip().lstrip().replace("    ", "")
    
    def _user_prompt(self, gene):
        prompt = """
            Provide a summary of the gene {0}
            """.format(gene)
        return prompt.rstrip().lstrip().replace("    ", "")
    
    def get(self, gene):
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": self._user_prompt(gene)},
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content


class DrugTLDRExplanation(object):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._cid2name = self._get_cid2name_mapping()

    def _get_cid2name_mapping(self):
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "chemical_gene_pairs_prediction_input.csv"))
        cid2name = {}
        for v in df[["cid", "chemical"]].values:
            cid2name[v[0]] = v[1]
        return cid2name

    def _system_prompt(self):
        prompt = """
            - You are a pharmacogenetics expert. You are asked to provide a short summary of a given drug's pharmacogenetic interactions profile.
            - You will be provided with a drug name and a short summary of the drug.
            - In addition, you may be provided with a list of genes (official gene symbols) that are known to interact with the drug.
            - If no genes are provided, you should still try to infer them based on your knowledge.
            - You should use your own knowledge to provide a summary of the drug's pharmacogenetic interactions profile. Your answer should be between 100 and 200 words.
            - Be as succinct as possible. Do not use full gene names. Use the official gene symbols only.
            - Mention all genes provided in the list and try to offer an explanation for each of them. You should try to distinguish between pharmacokinetics and pharmacodynamics.
            - If you are making an inference, please clarify that in your answer.
            - Do not raise disclaimers or comments on further studies needed.
            - Do not explain why understanding these interactions can be crucial. Focus on the interactions themselves.
            - Structure your answer in one paragraph, no special formatting.
        """
        return prompt.rstrip().lstrip().replace("    ", "")

    def _get_pharmgkb_knowledge(self, cid):
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_only_pk_only_adme_genes.csv"))
        df = df[df["cid"] == cid]
        pk_adme_genes = set(df["gene"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_only_pk_all_genes.csv"))
        df = df[df["cid"] == cid]
        pk_all_genes = set(df["gene"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_all_outcomes_only_adme_genes.csv"))
        df = df[df["cid"] == cid]
        all_outcomes_adme_genes = set(df["gene"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_all_outcomes_all_genes.csv"))
        df = df[df["cid"] == cid]
        all_outcomes_all_genes = set(df["gene"].unique().tolist())
        pk_other_genes = pk_all_genes.difference(pk_adme_genes)
        nopk_adme_genes = all_outcomes_adme_genes.difference(pk_adme_genes)
        nopk_other_genes = all_outcomes_all_genes.difference(pk_all_genes.union(pk_adme_genes.union(nopk_adme_genes)))
        data = {
            "pk_adme_genes": pk_adme_genes,
            "pk_other_genes": pk_other_genes,
            "nopk_adme_genes": nopk_adme_genes,
            "nopk_other_genes": nopk_other_genes,
        }
        print(data)
        return data

    def _get_drug_tldr(self, cid):
        file_name = os.path.join(root, "..", "data", "tldr", "drugs", "{0}.md".format(cid))
        with open(file_name, "r") as f:
            return f.read()

    def _user_prompt(self, cid):
        prompt = "# {0}\n".format(self._cid2name[cid])
        prompt += self._get_drug_tldr(cid)
        data = self._get_pharmgkb_knowledge(cid)
        prompt += "\n\n## Known Pharmacogenetic Interactions\n"
        prompt += "- **Pharmacokinetics and ADME genes**: {0}\n".format(", ".join(list(data["pk_adme_genes"])))
        prompt += "- **Pharmacokinetics and other genes**: {0}\n".format(", ".join(list(data["pk_other_genes"])))
        prompt += "- **Possibly Non-pharmacokinetics and ADME genes**: {0}\n".format(", ".join(list(data["nopk_adme_genes"])))
        prompt += "- **Possibly Non-pharmacokinetics and other genes**: {0}\n".format(", ".join(list(data["nopk_other_genes"])))
        return prompt

    def _get_primary_response(self, cid):
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": self._user_prompt(cid)},
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content
    
    def _get_oneliner(self, response):
        messages = [
            {"role": "system", "content": "Summarize the following text in one or two sentences. Focus on the genes and their interactions with the drug, and on the explanation. Discard all information about further information or further research needed, or why the information is crucial to understand the impact of the pharmacogenetic interaction."},
            {"role": "user", "content": response},
        
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content
    
    def get(self, cid):
        response = self._get_primary_response(cid)
        return self._get_oneliner(response)


class GeneTLDRExplanation(object):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._gid2name = self._get_gid2name_mapping()

    def _get_gid2name_mapping(self):
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "chemical_gene_pairs_prediction_input.csv"))
        gid2name = {}
        for v in df[["gid", "gene"]].values:
            gid2name[v[0]] = v[1]
        return gid2name

    def _system_prompt(self):
        prompt = """
            - You are a pharmacogenetics expert. You are asked to provide a short summary of a given gene's pharmacogenetic interactions profile with drugs.
            - You will be provided with a gene symbol and a short summary.
            - In addition, you may be provided with a list of drugs that are known to interact pharmacogenetically with the gene.
            - If no drugs are provided, you should still try to infer them based on your knowledge.
            - You should use your own knowledge to provide a summary of the genes's pharmacogenetic interactions profile. Your answer should be between 100 and 200 words.
            - Be as succinct as possible. Use drug names as provided.
            - Mention all drugs provided in the list and try to offer an explanation for each of them. You should try to distinguish between pharmacokinetics and pharmacodynamics.
            - If you are making an inference, please clarify that in your answer.
            - Do not raise disclaimers or comments on further studies needed.
            - Do not explain why understanding these interactions can be crucial. Focus on the interactions themselves.
            - Structure your answer in one paragraph, no special formatting.
        """
        return prompt.rstrip().lstrip().replace("    ", "")

    def _get_pharmgkb_knowledge(self, gid):
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_only_pk_only_adme_genes.csv"))
        df = df[df["gid"] == gid]
        pk_adme_genes = set(df["chemical"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_only_pk_all_genes.csv"))
        df = df[df["gid"] == gid]
        pk_all_genes = set(df["chemical"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_all_outcomes_only_adme_genes.csv"))
        df = df[df["gid"] == gid]
        all_outcomes_adme_genes = set(df["chemical"].unique().tolist())
        df = pd.read_csv(os.path.join(root, "..", "data", "ml_datasets_pairs", "df_all_outcomes_all_genes.csv"))
        df = df[df["gid"] == gid]
        all_outcomes_all_genes = set(df["chemical"].unique().tolist())
        pk = pk_adme_genes.union(pk_all_genes)
        nopk = all_outcomes_adme_genes.union(all_outcomes_all_genes).difference(pk)
        data = {
            "pk": pk,
            "nopk": nopk,
        }
        print(data)
        return data

    def _get_gene_tldr(self, gid):
        file_name = os.path.join(root, "..", "data", "tldr", "genes", "{0}.md".format(gid))
        with open(file_name, "r") as f:
            return f.read()

    def _user_prompt(self, gid):
        prompt = "# {0}\n".format(self._gid2name[gid])
        prompt += self._get_gene_tldr(gid)
        data = self._get_pharmgkb_knowledge(gid)
        prompt += "\n\n## Known Pharmacogenetic Interactions\n"
        prompt += "- **Pharmacokinetics**: {0}\n".format(", ".join(list(data["pk"])))
        prompt += "- **Possibly Non-pharmacokinetics**: {0}\n".format(", ".join(list(data["nopk"])))
        return prompt

    def _get_primary_response(self, gid):
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": self._user_prompt(gid)},
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content
    
    def _get_oneliner(self, response):
        messages = [
            {"role": "system", "content": "Summarize the following text in one or two sentences. Focus on the drugs and their interactions with the gene, and on the explanation. Discard all text about further information or further research needed, or why the information is crucial to understand the impact of the pharmacogenetic interaction."},
            {"role": "user", "content": response},
        
        ]
        response = self.client.chat.completions.create(model=OPENAI_MODEL, messages=messages)
        return response.choices[0].message.content
    
    def get(self, gid):
        response = self._get_primary_response(gid)
        return self._get_oneliner(response)


if __name__ == "__main__":

    #dt = DrugTLDR()
    #db_id = "DB00951"
    #print(dt.get(db_id))

    #dg = GeneTLDR()
    #gene = "CYP2D6"
    #print(dt.get(gene))

    #dt = DrugTLDRExplanation()
    #cid = "PA166153416"
    #cid = "nan-2b15062b-9e70-452d-bf7b-eb623e2d07a0"
    #print(dt.get(cid))

    dt = GeneTLDRExplanation()
    gid = "PA20"
    print(dt.get(gid))
