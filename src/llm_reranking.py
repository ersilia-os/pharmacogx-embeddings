import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import collections
from tqdm import tqdm

root = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(root, "..", ".env"))

openai_api_key = os.getenv("OPENAI_API_KEY")


class LLMCompoundGeneReranker(object):

    def __init__(self, df, results_dir=None, round=0):
        self.client = OpenAI(api_key=openai_api_key)
        self.df = pd.DataFrame(df)
        self._gene2gid = self._get_gene2gid()
        if results_dir is None:
            self.results_dir = None
            self.output_prompts_dir = None
            self.output_responses_dir = None
        else:
            self.results_dir = os.path.abspath(results_dir)
            if not os.path.exists(self.results_dir):
                os.makedirs(self.results_dir)
            self.output_prompts_dir = os.path.join(self.results_dir, "reranking", "prompts")
            self.output_responses_dir = os.path.join(self.results_dir, "reranking", "responses", f"round_{round}")
            if not os.path.exists(self.output_prompts_dir):
                os.makedirs(self.output_prompts_dir)
            if not os.path.exists(self.output_responses_dir):
                os.makedirs(self.output_responses_dir)
            if not os.path.exists(os.path.join(self.output_responses_dir, "json")):
                os.makedirs(os.path.join(self.output_responses_dir, "json"))
            if not os.path.exists(os.path.join(self.output_responses_dir, "markdown")):
                os.makedirs(os.path.join(self.output_responses_dir, "markdown"))

    def _get_gene2gid(self):
        gene2gid = {}
        for r in self.df[["gid", "gene"]].values:
            gene2gid[r[1]] = r[0]
        return gene2gid

    def _system_prompt(self):
        prompt = '''
            # Main instructions
            - You are a pharmacogenetics expert. You goal is to identify pharmacogenetic drug-gene pairs.
            - The user will give you a drug of interest. You need to rank a set of candidate genes according to their likelihood of being pharmacogenetically related to the drug.
            - Prioritize pharmacokinetic interactions, such as those affecting drug metabolism, transport, and excretion.
            - The user will provide a pre-ranked list of 50 genes, along with a z-score. Z-scores above 1.96 are more significant. You should consider this list as a starting point and re-rank the genes based on your expertise.
            - Up-rank genes with a known pharmacogenetic relationship with the drug.
            - Do not include genes that are not in the pre-ranked list. Only rerank the genes that are already in the list.
            - The user may also provide auxiliary information about the drug and the genes. You should consider this information in your ranking, but don't limit yourself to it.
            - Do not focus only on known associations. Use your expertise to infer new pharmacogenetic relationships. Make logical and mechanistic reasoning based on gene function, gene expression, drug mechanism of action, pharmacokinetics, etc.
            - For example, consider known pharmacogenetic relationships of similar drugs and similar genes in your reasoning.
            - You should return a ranked list of genes in JSON format. The list should be sorted in descending order of likelihood. Give me only the top 10 genes.
            - For each gene, offer an explanation of why you think there is a pharmacogenetic relationship with the given drug. This explanation should be 500 words long. Be as detailed as possible.
            - The explanation is important. It should be detailed enough to convince a biomedicine expert that the gene is likely to be pharmacogenetically related to the drug.
            - Do not make any other comment. Do not suggest that further research is necessary and do not say trivial or generalistic sentences about pharmacogenetics. Do not ask questions. Do not mention PharmGKB or any other database.
            - Do not mention the z-score in your response. You can consider it in your ranking, but you should not include it in your final response.
            - Do not include any code or comments in your response.
            - Make it clear if you are making an inference.
            - Do not mention the rank explicitly in your response. The rank should be implicit in the order of the genes.
            - Only return a JSON string. Do not make comments before or after. Your response should be directly parseable with the Python command `json.loads`. The schema of the JSON file should be strictly as follows:
              [
                {gene: GENE_SYMBOL, rank: INTEGER, explanation: TEXT},
                {gene: GENE_SYMBOL, rank: INTEGER, explanation: TEXT},
                ...
              ]
            '''
        return prompt.lstrip().rstrip().replace("    ", "") + "\n"
    
    def _auxiliary_drug_prompt(self, chemical_name):
        pgkb_id = self.df[self.df["chemical"] == chemical_name]["cid"].tolist()[0]
        print(pgkb_id, chemical_name)
        drug_file_name = os.path.join(root, "..", "data", "tldr_explanations", "drugs", f"{pgkb_id}.md")
        if not os.path.exists(drug_file_name):
            return None
        with open(drug_file_name, "r") as f:
            text = f.read()
        prompt = '''
            # Auxiliary information about the drug
            Below is some auxiliary information about the drug of interest:

            **{0}**: {1}
            '''.format(chemical_name, text)
        return prompt.rstrip().lstrip().replace("    ", "") + "\n\n"
    
    def _auxiliary_genes_prompt(self, gene_names):
        prompt = '''
        # Auxiliary information about the genes
        Below is some auxiliary information about the genes in the pre-ranked list:
        '''.rstrip().lstrip().replace("    ", "") + "\n"
        texts = []
        for gene_name in gene_names:
            if not gene_name in self._gene2gid:
                continue
            gid = self._gene2gid[gene_name]
            gene_file_name = os.path.join(root, "..", "data", "tldr_explanations", "genes", f"{gid}.md")
            if not os.path.exists(gene_file_name):
                continue
            with open(gene_file_name, "r") as f:
                text = f.read()
            texts += [(gene_name, text)]
        if len(texts) == 0:
            prompt += "No auxiliary information available for the genes in the pre-ranked list.\n\n"
        else:
            for gene_name, text in texts:
                prompt += '''
                    **{0}**: {1}
                    '''.format(gene_name, text).rstrip().lstrip().replace("    ", "") + "\n\n"
        return prompt.rstrip().lstrip().replace("    ", "") + "\n"

    def _user_message(self, chemical_name):
        df = self.df[self.df["chemical"] == chemical_name]
        print("Number of candidates", df.shape)
        df = df.sort_values("consensus_zscore", ascending=False).reset_index(drop=True)
        ranked_list_of_genes = df["gene"].tolist()
        z_scores = df["consensus_zscore"].tolist()
        known_pharmacogenes = df[df["train_set_pk"] == 1]["gene"].tolist()

        prompt = '''
            # Drug of interest
            My drug of interest is {0}.
        '''.format(list(set(df["chemical"].tolist()))[0]).rstrip().lstrip().replace("    ", "") + "\n\n"

        ranked_genes_txt = ["{0} (z: {1})".format(g, round(z, 2)) for g, z in zip(ranked_list_of_genes, z_scores)]
        ranked_genes_txt = ["{0}. {1}".format(i+1, g) for i, g in enumerate(ranked_genes_txt)]
        ranked_genes_txt = "\n".join(ranked_genes_txt)

        prompt += '''
            # Pre-ranked list of genes
            These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
            {0}
            '''.format(ranked_genes_txt).rstrip().lstrip().replace("    ", "") + "\n\n"

        if len(known_pharmacogenes) > 0:
            known_pharmacogenes_txt = ["- {0}".format(g) for g in known_pharmacogenes]
            known_pharmacogenes_txt = "\n".join(known_pharmacogenes_txt)
            prompt += '''
                # Known pharmacogenetic associations
                In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
                {0}
            '''.format(known_pharmacogenes_txt).rstrip().lstrip().replace("    ", "") + "\n\n"

        prompt = prompt.lstrip().rstrip().replace("    ", "") + "\n\n"

        aux_drug_prompt = self._auxiliary_drug_prompt(chemical_name)
        if aux_drug_prompt is not None:
            prompt += aux_drug_prompt

        aux_genes_prompt = self._auxiliary_genes_prompt(ranked_list_of_genes)
        if aux_genes_prompt is not None:
            prompt += aux_genes_prompt

        return prompt
    
    def _save_prompt(self, chemical_name, user_prompt):
        if self.output_prompts_dir is not None:
            prompt_file_name = os.path.join(self.output_prompts_dir, f"{chemical_name}.md")
            with open(prompt_file_name, "w") as f:
                f.write(user_prompt)

    def _serialize_to_json(self, response):
        if response.startswith("```json") and response.endswith("```"):
            response = response.split("\n")[1:-1].rsrip().lstrip()
        try:
            data = json.loads(response)
        except:
            return None
        if not isinstance(data, list):
            return None
        d = data[0]
        if not isinstance(d, dict):
            return None
        keys = sorted(d.keys())
        if keys != ["explanation", "gene", "rank"]:
            return None
        ranks = [x["rank"] for x in data]
        if ranks != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return None
        return data

    def _save_response(self, chemical_name, data):
        if self.output_responses_dir is not None:
            response_file_name = os.path.join(self.output_responses_dir, "json", f"{chemical_name}.json")
            with open(response_file_name, "w") as f:
                json.dump(data, f, indent=4)
            response_file_name = os.path.join(self.output_responses_dir, "markdown", f"{chemical_name}.md")
            with open(response_file_name, "w") as f:
                text = "# {0}\n\n".format(chemical_name.capitalize())
                for d in data:
                    text += "## {0}. {1}\n".format(d["rank"], d["gene"])
                    text += "{0}\n\n".format(d["explanation"])
                f.write(text)

    def _run(self, chemical_name):
        system_prompt = self._system_prompt()
        user_prompt = self._user_message(chemical_name)
        self._save_prompt(chemical_name, user_prompt)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model = "gpt-4",
        )
        response = chat_completion.choices[0].message.content
        print(response)
        return response
    
    def _get_available(self, chemical_name):
        if self.output_responses_dir is None:
            return None
        response_file_name = os.path.join(self.output_responses_dir, "json", f"{chemical_name}.json")
        if not os.path.exists(response_file_name):
            return None
        with open(response_file_name, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return None
        return data

    def run(self, chemical_name):
        available_data = self._get_available(chemical_name)
        if available_data is not None:
            print("{0} already available".format(chemical_name))
            return available_data
        for i in range(10):
            print("Attempt", i+1)
            response = self._run(chemical_name)
            data = self._serialize_to_json(response)
            if data is not None:
                break
        if data is None:
            print("Failed to get a valid response for {0}".format(chemical_name))
            return None
        self._save_response(chemical_name, data)
        return data
    

class LLMCompoundGeneRerankerConsensus(object):
    def __init__(self, results_dir, lazy=False):
        self.client = OpenAI(api_key=openai_api_key)
        self.lazy = lazy
        self.results_dir = results_dir
        self.output_dir = os.path.join(self.results_dir, "reranking", "consensus")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(os.path.join(self.output_dir, "json")):
            os.makedirs(os.path.join(self.output_dir, "json"))
        if not os.path.exists(os.path.join(self.output_dir, "markdown")):
            os.makedirs(os.path.join(self.output_dir, "markdown"))

    def _get_consensus_from_rounds(self, chemical_name):
        data = []
        for round in range(3):
            response_file_name = os.path.join(self.results_dir, "reranking", "responses", "round_{0}".format(round), "json", f"{chemical_name}.json")
            if not os.path.exists(response_file_name):
                continue
            with open(response_file_name, "r") as f:
                d = json.load(f)
            data += [d]
        gene_scores = collections.defaultdict(list)
        for d in data:
            for x in d:
                gene_scores[x["gene"]] += [10 - (x["rank"]-1)]
        gene_scores = dict((k, sum(v)) for k, v in gene_scores.items())
        sorted_genes = sorted(gene_scores.keys(), key=lambda x: gene_scores[x], reverse=True)[:10]
        data_sel = []
        for i, g in enumerate(sorted_genes):
            explanations = []
            for x in data:
                for y in x:
                    if y["gene"] == g:
                        explanations += [y["explanation"]]
            d = {
                "gene": g,
                "rank": i+1,
                "explanations": explanations
            }
            data_sel += [d]
        return data_sel

    def _system_prompt(self):
        prompt = '''
        - You are a pharmacogenetics expert. Your goal is to select the most trustworthy explanation of the pharmacogenetic relationship between a drug and a gene.
        - You will be given a drug and a gene. You need to select the best explanation from a set of options.
        - Options will be labeled from 1 to 3, at most.
        - You should return the number of the best explanation. Nothing else. Do not make any other comment.
        - The output should be a single number, from 1 to 3. The Python function int() will be used to parse the output.
        '''
        return prompt.lstrip().rstrip().replace("    ", "") + "\n"
    
    def _user_prompt(self, chemical_name, gene_name, explanations):
        prompt = '''
        Select the most trusthworthy explanation.
        - Drug: {0}
        - Gene: {1}

        Options:
        '''.format(chemical_name, gene_name).rstrip().lstrip().replace("    ", "") + "\n\n"
        for i, e in enumerate(explanations):
            prompt += "{0}. {1}\n".format(i+1, e).rstrip().lstrip().replace("    ", "") + "\n"
        return prompt.rstrip().lstrip().replace("    ", "") + "\n"

    def _save_data(self, chemical_name, data):
        response_file_name = os.path.join(self.output_dir, "json", f"{chemical_name}.json")
        with open(response_file_name, "w") as f:
            json.dump(data, f, indent=4)
        response_file_name = os.path.join(self.output_dir, "markdown", f"{chemical_name}.md")
        with open(response_file_name, "w") as f:
            text = "# {0}\n\n".format(chemical_name.capitalize())
            for d in data:
                text += "## {0}. {1}\n".format(d["rank"], d["gene"])
                text += "{0}\n\n".format(d["explanation"])
            f.write(text)

    def run(self, chemical_name):
        data = self._get_consensus_from_rounds(chemical_name)
        data_ = []
        for d in tqdm(data):
            gene_name = d["gene"]
            explanations = d["explanations"]
            if self.lazy:
                data_ += [
                    {
                        "gene": gene_name,
                        "rank": d["rank"],
                        "explanation": explanations[0]
                    }
                ]
            else:
                system_prompt = self._system_prompt()
                user_prompt = self._user_prompt(chemical_name, gene_name, explanations)
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    model = "gpt-4-turbo",
                )
                response = chat_completion.choices[0].message.content
                response = response.rstrip().lstrip()
                try:
                    response = int(response)
                    explanation = explanations[response-1]
                except:
                    print("Explanation failed...")
                    explanation = explanations[0]
                data_ += [
                    {
                        "gene": gene_name,
                        "rank": d["rank"],
                        "explanation": explanation
                    }
                ]
        self._save_data(chemical_name, data_)
        return data_