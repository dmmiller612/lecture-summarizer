import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from gensim.summarization.summarizer import summarize
from sklearn.cluster import AffinityPropagation
from summarizer.BertParent import BertParent


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
        if self.algorithm == 'affinity':
            return AffinityPropagation()
        return KMeans(n_clusters=k)

    def __get_centroids(self, model):
        if self.algorithm == 'gmm':
            return model.means_
        return model.cluster_centers_

    def __find_closest_args(self, centroids):
        centroid_min = 1e7
        cur_arg = -1
        args = {}
        used_idx = []
        for j, centroid in enumerate(centroids):
            for i, feature in enumerate(self.features):
                value = np.sum(np.abs(feature - centroid))
                if value < centroid_min and i not in used_idx:
                    cur_arg = i
                    centroid_min= value
            used_idx.append(cur_arg)
            args[j] = cur_arg
            centroid_min = 1e7
            cur_arg = -1
        return args

    def cluster(self, ratio=0.1):
        k = int(len(self.features) * ratio)
        model = self.__get_model(k).fit(self.features)
        centroids = self.__get_centroids(model)
        cluster_args = self.__find_closest_args(centroids)
        sorted_values = sorted(cluster_args.values())
        return sorted_values


class PostTextProcessor(object):

    REMOVAL_WORDS = ['whereas', 'finally', 'or']

    def __init__(self, results):
        self.results = results

    def process(self):
        final_results = []
        for result in self.results:
            start = result.split(' ')
            if start[0].lower() in self.REMOVAL_WORDS:
                start.pop(0)
            start = ''.join(start)
            final_results.append(start)
        return final_results


def text_rank(full_text):
    full_text = ''.join(full_text)
    res = summarize(full_text)
    return res.split('\n')


if __name__ == '__main__':
    bert_handler = BertParent('bert', 'large')
    with open('data/sdp.txt', 'r') as f:
        content = f.readlines()

    content = [c for c in content if len(c) > 60 and not c.startswith('but') and
               not c.startswith('and') and not c.__contains__('quiz') and not c.startswith('or')]

    train_vec = bert_handler.create_matrix(content, False)
    res = ClusterFeatures(train_vec, 'kmeans').cluster(0.1)

    results = []
    for j in res:
        # results.append(content[j-1])
        results.append(content[j])
    for r in results:
        print(r)
    print(results)




