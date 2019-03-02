import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from tqdm import tqdm
from sklearn.decomposition import PCA


class BertHandler(object):

    def __init__(self, vocab='data/vocab.txt', model='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(vocab)
        self.model = BertModel.from_pretrained(model)
        self.model.eval()

    def tokenize_input(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        return torch.tensor([indexed_tokens])

    def extract_embeddings(self, text, use_hidden=False):
        tokens_tensor = self.tokenize_input(text)
        hidden_states, pooled = self.model(tokens_tensor)
        if use_hidden:
            return hidden_states[-2].mean(dim=1)
        return pooled

    def process_whole_lecture(self, content, use_hidden=False):
        train_vec = np.zeros((len(content), 768))
        for i, t in tqdm(enumerate(content)):
            train_vec[i] = bert_handler.extract_embeddings(t, use_hidden).data.numpy()
        return train_vec


class ClusterFeatures(object):

    def __init__(self, features, algorithm='kmeans', pca_k=None):
        if pca_k:
            self.features = PCA(n_components=pca_k).fit_transform(features)
        else:
            self.features = features
        self.algorithm = algorithm

    def __get_model(self, k):
        if self.algorithm == 'gmm':
            return GaussianMixture(n_components=k)
        return KMeans(n_clusters=k)

    def __get_centroids(self, model):
        if self.algorithm == 'gmm':
            return model.means_
        return model.cluster_centers_

    def __find_closest_args(self, centroids):
        centroid_min = 1e7
        cur_arg = -1
        args = {}
        for j, centroid in enumerate(centroids):
            for i, feature in enumerate(self.features):
                value = np.sum(np.abs(feature - centroid))
                if value < centroid_min:
                    cur_arg = i
                    centroid_min= value
            args[j] = cur_arg
            centroid_min = 1e7
            cur_arg = -1
        return args

    def cluster(self, k=8):
        model = self.__get_model(k).fit(self.features)
        centroids = self.__get_centroids(model)
        cluster_args = self.__find_closest_args(centroids)
        sorted_values = sorted(cluster_args.values())
        return sorted_values


if __name__ == '__main__':
    bert_handler = BertHandler()
    with open('data/sdp.txt', 'r') as f:
        content = f.readlines()

    content = [c for c in content if len(c) > 60 and not c.startswith('but') and not c.startswith('and') and not c.__contains__('quiz')]

    train_vec = bert_handler.process_whole_lecture(content, True)
    res = ClusterFeatures(train_vec, 'gmm', pca_k=50).cluster(4)

    results = []
    for j in res:
        # results.append(content[j-1])
        results.append(content[j])
    for r in results:
        print(r)
    print(results)




