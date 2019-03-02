import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel

import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm


class BertHandler(object):

    def __init__(self, vocab='data/vocab.txt', model='data/bert-base-uncased.tar.gz'):
        self.tokenizer = BertTokenizer.from_pretrained(vocab)
        self.model = BertModel.from_pretrained(model)
        self.model.eval()

    def tokenize_input(self, text):
        tokenized_text = self.tokenizer.tokenize(text)

        # Convert token to vocabulary indices
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        # Convert inputs to PyTorch tensors
        return torch.tensor([indexed_tokens])

    def extract_embeddings(self, text):
        tokens_tensor = self.tokenize_input(text)
        hidden_states, pooled = self.model(tokens_tensor)
        #return hidden_states[-2].mean(dim=1)
        return pooled


if __name__ == '__main__':
    bert_handler = BertHandler()
    with open('data/sdp.txt', 'r') as f:
        content = f.readlines()

    content = [c for c in content if len(c) > 80 and not c.startswith('but') and not c.startswith('and') and not c.__contains__('quiz')]

    train_vec = np.zeros((len(content), 768))
    for i, t in tqdm(enumerate(content)):
        train_vec[i] = bert_handler.extract_embeddings(t).data.numpy()

    kmeans = KMeans(random_state=12345, n_clusters=4).fit(train_vec)

    centroids = kmeans.cluster_centers_
    args = {}
    minimum = 100000000

    centroid_min = 100000000
    cur_arg = -1
    for j, c in enumerate(centroids):
        for i, t in tqdm(enumerate(train_vec)):
            v = np.sum(np.abs(t-c))
            if v < centroid_min:
                cur_arg = i
                centroid_min = v
        args[j] = cur_arg
        centroid_min = 10000000
        cur_arg = -1

    res = sorted(args.values())

    results = []
    for j in res:
        # results.append(content[j-1])
        results.append(content[j])
    for r in results:
        print(r)
    print(results)




