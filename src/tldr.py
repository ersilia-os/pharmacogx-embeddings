import os
import json
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


if __name__ == "__main__":

    dt = DrugTLDR()
    db_id = "DB00951"
    print(dt.get(db_id))

    dg = GeneTLDR()
    gene = "CYP2D6"
    print(dg.get(gene))

