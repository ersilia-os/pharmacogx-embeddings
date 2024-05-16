import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

root = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(root, "..", ".env"))

openai_api_key = os.getenv("OPENAI_API_KEY")


class LLMCompoundGeneReranker(object):

    def __init__(self, df, results_dir=None):
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
            self.output_responses_dir = os.path.join(self.results_dir, "reranking", "responses")
            if not os.path.exists(self.output_prompts_dir):
                os.makedirs(self.output_prompts_dir)
            if not os.path.exists(self.output_responses_dir):
                os.makedirs(self.output_responses_dir)

    def _get_gene2gid(self):
        gene2gid = {}
        for r in self.df[["gid", "gene"]].values:
            gene2gid[r[1]] = r[0]
        return gene2gid

    def _system_prompt(self):
        prompt = '''
            # Main instructions
            - You are a biomedicine expert. You help me identify pharmacogenetic drug-gene pairs. Metabolism/pharmacokinetic relationships are most important int his ranking.
            - The user will give you a drug of interest. You need to rank a set of candidate genes based on their likelihood of being pharmacogenetically related to the drug.
            - The user will provide a pre-ranked list of genes. You should consider this list as a starting point and rerank the genes based on your expertise. Feel free to make significant changes to the ranking.
            - Do not include genes that are not in the pre-ranked list. Only rerank the genes that are already in the list.
            - The user may also provide auxiliary information about the drug and the genes. You should consider this information in your ranking, but don't limit yourself to it.
            - Do not focus only on known associations. Use your expertise to infer new pharmacogenetic relationships. Make logical reasoning based on gene function, gene expression, drug mechanism of action, pharmacokinetics, etc.
            - You should return a ranked list of genes in JSON format. The list should be sorted in descending order of likelihood. Give me only the top 10 genes.
            - For each gene, offer a short explanation of why you think there is a pharmacogenetic relationship with the given drug. This explanation should be between 200 and 500 words.
            - The explanation is important. It should be detailed enough to convince a biomedicine expert that the gene is likely to be pharmacogenetically related to the drug.
            - Only return a JSON string. Do not make any other comment. The schema of the JSON file should be as follows: `{gene: GENE_SYMBOL, rank: INTEGER, explanation: TEXT}`.
            '''
        return prompt.lstrip().rstrip().replace("    ", "") + "\n"
    
    def _auxiliary_drug_prompt(self, chemical_name):
        pgkb_id = self.df[self.df["chemical"] == chemical_name]["cid"].tolist()[0]
        print(pgkb_id, chemical_name)
        drug_file_name = os.path.join(root, "..", "data", "tldr", "drugs", f"{pgkb_id}.md")
        if not os.path.exists(drug_file_name):
            return None
        with open(drug_file_name, "r") as f:
            text = f.read()
        prompt = '''
            # Auxiliary information about the drug
            Below is some auxiliary information about the drug of interest:
            {0}
            '''.format(text)
        return prompt.rstrip().lstrip().replace("    ", "") + "\n"
    
    def _auxiliary_genes_prompt(self, gene_names):
        prompt = '''
        # Auxiliary information about the genes
        Below is some auxiliary information about the genes in the pre-ranked list:
        ''' + "\n"
        texts = []
        for gene_name in gene_names:
            if not gene_name in self._gene2gid:
                continue
            gid = self._gene2gid[gene_name]
            gene_file_name = os.path.join(root, "..", "data", "tldr", "genes", f"{gid}.md")
            if not os.path.exists(gene_file_name):
                continue
            with open(gene_file_name, "r") as f:
                text = f.read()
            text = text.replace("# ", "### ")
            text = text.replace("## ", "### ")
            texts += [(gene_name, text)]
        if len(texts) == 0:
            prompt += "No auxiliary information available for the genes in the pre-ranked list."
        else:
            for gene_name, text in texts:
                prompt += '''
                    ## Gene: {0}
                    {1}
                    '''.format(gene_name, text) + "\n"
        return prompt.rstrip().lstrip().replace("    ", "") + "\n"

    def _user_message(self, chemical_name):
        df = self.df[self.df["chemical"] == chemical_name]
        print("Number of candidates", df.shape)
        ranked_list_of_genes = df["gene"].tolist()
        known_pharmacogenes = df[df["train_set_pk"] == 1]["gene"].tolist()

        prompt = '''
            # Drug of interest
            My drug of interest is {0}.
        '''.format(list(set(df["chemical"].tolist()))[0]) + "\n"

        prompt += '''
            # Pre-ranked list of genes
            These are the candidate genes for this drugs, tentatively ranked by the likelihood of a pharmacogenetic relationship:
            {0}
            '''.format(", ".join(ranked_list_of_genes)) + "\n"
        
        if len(known_pharmacogenes) > 0:
            prompt += '''
                # Known pharmacogenetic associations
                In addition, please consider that the following pharmacogenetic interactions are already known for this drug, according to PharmGKB:
                {0}
            '''.format(", ".join(known_pharmacogenes)) + "\n"

        prompt = prompt.lstrip().rstrip().replace("    ", "") + "\n"

        aux_drug_prompt = self._auxiliary_drug_prompt(chemical_name)
        if aux_drug_prompt is not None:
            prompt += aux_drug_prompt

        aux_genes_prompt = self._auxiliary_genes_prompt(ranked_list_of_genes)
        if aux_genes_prompt is not None:
            prompt += aux_genes_prompt

        return prompt
    
    def _save_prompt(self, chemical_name, system_prompt, user_prompt):
        if self.output_prompts_dir is not None:
            prompt_file_name = os.path.join(self.output_prompts_dir, f"{chemical_name}.md")
            with open(prompt_file_name, "w") as f:
                f.write(system_prompt + "\n" + user_prompt)

    def _save_response(self, chemical_name, response):
        data = json.loads(response)
        if self.output_responses_dir is not None:
            response_file_name = os.path.join(self.output_responses_dir, f"{chemical_name}.json")
            with open(response_file_name, "w") as f:
                json.dump(data, f, indent=4)
            response_file_name = os.path.join(self.output_responses_dir, f"{chemical_name}.md")
            with open(response_file_name, "w") as f:
                text = "# {0}\n".format(chemical_name.capitalize())
                for d in data:
                    text += "## {0}. {1}\n".format(d["rank"], d["gene"])
                    text += "{0}\n".format(d["explanation"])
                f.write(text)

    def run(self, chemical_name):
        system_prompt = self._system_prompt()
        user_prompt = self._user_message(chemical_name)
        self._save_prompt(chemical_name, system_prompt, user_prompt)
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
        self._save_response(chemical_name, response)
        return response
    

if __name__ == "__main__":
    chemical_name = "isoniazid"
    results_dir = os.path.join(root, "..", "results", "results_pairs")
    df = pd.read_csv(os.path.join(root, "..", "results", "results_pairs", "chemical_gene_pairs_prediction_with_zscore_and_filtered_with_variant_aggregates.csv"))
    ranker = LLMCompoundGeneReranker(df, results_dir=results_dir)
    data = ranker.run(chemical_name)
    print(data)
    