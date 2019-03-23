import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from gensim.summarization.summarizer import summarize
from sklearn.cluster import AffinityPropagation
from summarizer.BertParent import BertParent
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class ClusterFeatures(object):

    def __init__(self, features, algorithm='kmeans', pca_k=None):
        if pca_k:
            self.features = PCA(n_components=pca_k).fit_transform(features)
        else:
            self.features = features
        self.algorithm = algorithm
        self.pca_k = pca_k

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

    def create_plots(self, k=4, plot_location='./cool_model.png', title = ''):
        if self.pca_k != 2:
            raise RuntimeError("Must be dimension of 2")
        model = self.__get_model(k)
        model.fit(self.features)
        y = model.predict(self.features)
        plt.title(title)
        plt.scatter(self.features[:, 0], self.features[:, 1], c=y, s=50, cmap='viridis')
        centers = model.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
        plt.savefig(plot_location)


class LectureEnsembler(object):

    def __init__(self, content):
        self.gp2 = BertParent('openApi', 'large')
        self.bert_model = BertParent('bert', 'large')
        self.gp2_non_hidden = self.gp2.create_matrix(content)
        self.bert_non_hidden = self.bert_model.create_matrix(content)
        self.bert_hidden = self.bert_model.create_matrix(content, True)
        self.content = content

    def __vote(self, arg_list):
        all_tally = {}
        for args in arg_list:
            for arg in args:
                if arg in all_tally:
                    all_tally[arg] += 1
                else:
                    all_tally[arg] = 1
        to_return = {k: v for k, v in all_tally.items() if v > 1}
        return to_return

    def run_clusters(self, cluster_percentage=0.2):
        bc_non_hidden_args = ClusterFeatures(self.bert_non_hidden).cluster(cluster_percentage)
        bc_hidden_args = ClusterFeatures(self.bert_hidden).cluster(cluster_percentage)
        gp2_non_hidden_args = ClusterFeatures(self.gp2_non_hidden).cluster(cluster_percentage)

        votes = self.__vote([bc_non_hidden_args, bc_hidden_args, gp2_non_hidden_args])
        sorted_keys = sorted(votes.keys())
        if sorted_keys[0] != 0:
            sorted_keys.insert(0, 0)
        to_return = []
        for key in sorted_keys:
            to_return.append(key)
        return to_return


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

    with open('data/health_today_1.txt', 'r') as f:
        content = f.readlines()

    content = [c for c in content if len(c) > 80 and not c.lower().startswith('but') and
               not c.lower().startswith('and')
               and not c.lower().__contains__('quiz') and
               not c.lower().startswith('or')]

    res = LectureEnsembler(content).run_clusters(0.2)

    results = []
    for j in res:
        # results.append(content[j-1])
        results.append(content[j])
    for r in results:
        print(r)
    print(results)




