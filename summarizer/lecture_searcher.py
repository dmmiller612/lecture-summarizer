import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel
import numpy as np
from annoy import AnnoyIndex


class BertSearcher(object):

    def __init__(self, vocab='data/vocab.txt', model='bert-base-uncased', n_trees=50):
        self.tokenizer = BertTokenizer.from_pretrained(vocab)
        self.model = BertModel.from_pretrained(model)
        self.n_trees = n_trees
        self.model.eval()

    def tokenize_input(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        return torch.tensor([indexed_tokens])

    def index_items(self, contents):
        t = AnnoyIndex(768, metric='angular')
        for content_id, content in enumerate(contents):
            token = self.tokenize_input(content)
            hidden_states, pooled = self.model(token)
            pooled = pooled.detach().numpy().squeeze()
            t.add_item(content_id, pooled)

        t.build(self.n_trees)
        t.save('tree_builder')
        return t


class BertMatcher(object):

    def __init__(self, content, annoy_index, vocab='data/vocab.txt', model='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(vocab)
        self.model = BertModel.from_pretrained(model)
        self.annoy_index = annoy_index
        self.content = content

    def tokenize_input(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        return torch.tensor([indexed_tokens])

    def process(self, user_input):
        token = self.tokenize_input(user_input)
        hidden_states, pooled = self.model(token)
        pooled = pooled.detach().numpy().squeeze()
        idx_dists = self.annoy_index.get_nns_by_vector(pooled, 3, include_distances=True)
        return [{
            'sim': i[1],
            'data': self.content[i[0]],
            'idx': i[0]
        } for i in zip(idx_dists[0], idx_dists[1])]


if __name__ == '__main__':
    with open('data/sdp.txt', 'r') as f:
        content = f.readlines()
    content = [c for c in content if len(c) > 20]

    t = BertSearcher().index_items(content)
    #t = AnnoyIndex(768, metric='dot')
    #t.load('tree_builder')
    bert_matcher = BertMatcher(content, t).process("on the contrary if we choose the wrong model that can be a constant source of problems and ultimately it can make the project fail")
    print(bert_matcher)


