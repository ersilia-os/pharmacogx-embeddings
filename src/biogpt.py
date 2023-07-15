import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np


class BioGPTEmbedder(object):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/biogpt")

    def calculate(self, text_inputs):
        X = np.zeros((len(text_inputs), 1024), dtype=np.float32)
        for i, text in enumerate(text_inputs):
            encoded_input = self.tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                hidden_states = self.model.base_model(**encoded_input).last_hidden_state
            mean_encoding = torch.mean(hidden_states, dim=1)
            mean_encoding_np = mean_encoding.numpy()
            X[i, :] = mean_encoding_np
        return X
