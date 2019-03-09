from pytorch_pretrained_bert import BertTokenizer, BertModel, GPT2Model, GPT2Tokenizer
import logging
import torch
import numpy as np
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


class BertParent(object):

    model_handler = {
        'bert': BertModel,
        'openApi': GPT2Model
    }

    token_handler = {
        'open_api': GPT2Tokenizer,
        'bert': BertTokenizer
    }

    size_handler = {
        'base': {
            'bert': 'bert-base-uncased',
            'openApi': 'gpt2'
        },
        'large': {
            'bert': 'bert-large-uncased',
            'openApi': 'gpt2'
        }
    }

    vector_handler = {
        'base': {
            'bert': 768,
            'openApi': 1024
        },
        'large': {
            'bert': 1024,
            'openApi': 1024
        }
    }

    def __init__(self, model_type, size):
        self.model = self.model_handler[model_type](self.size_handler[size, model_type])
        self.tokenizer = self.token_handler[model_type](self.size_handler[size, model_type])
        self.vector_size = self.vector_handler[model_type][self.size_handler[size, model_type]]
        self.model.eval()

    def tokenize_input(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        return torch.tensor([indexed_tokens])

    def extract_embeddings(self, text, use_hidden=False, squeeze=False):
        tokens_tensor = self.tokenize_input(text)
        hidden_states, pooled = self.model(tokens_tensor)
        if use_hidden:
            return hidden_states[-2].mean(dim=1)
        if squeeze:
            return pooled.detach().numpy().squeeze()
        return pooled

    def create_matrix(self, content, use_hidden=False):
        train_vec = np.zeros((len(content), self.vector_size))
        for i, t in tqdm(enumerate(content)):
            train_vec[i] = self.extract_embeddings(t, use_hidden).data.numpy()
        return train_vec
