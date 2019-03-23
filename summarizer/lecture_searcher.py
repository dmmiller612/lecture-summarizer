from annoy import AnnoyIndex
from summarizer.BertParent import BertParent
import numpy as np
from sklearn.decomposition import PCA


class BertSearcher(BertParent):

    def __init__(self, model_type='bert', size='large', n_trees=40):
        BertParent.__init__(self, model_type, size)
        self.n_trees = n_trees

    def index_items(self, contents, use_pca=False):
        t = AnnoyIndex(768, metric='angular')
        for content_id, c in enumerate(contents):
            pooled = self.extract_embeddings(c, squeeze=True)
            t.add_item(content_id, pooled)
        t.build(self.n_trees)
        t.save('tree_builder')
        return t


class BertMatcher(BertParent):

    def __init__(self, content, annoy_index, model_type='bert', size='large'):
        BertParent.__init__(self, model_type, size)
        self.annoy_index = annoy_index
        self.content = content
        self.content_features = self.create_matrix(self.content, use_hidden=True)

    def scored(self, user_input):
        pooled = self.extract_embeddings(user_input, use_hidden=True)
        score = np.sum(pooled * self.content_features, axis=1)
        topk_idx = np.argsort(score)[::-1][:5]
        return [{
            'data': self.content[i],
            'idx': i
        } for i in topk_idx]

    def process(self, user_input):
        pooled = self.extract_embeddings(user_input, squeeze=True)

        idx_dists = self.annoy_index.get_nns_by_vector(pooled, 5, include_distances=True)
        return [{
            'sim': i[1],
            'data': self.content[i[0]],
            'idx': i[0]
        } for i in zip(idx_dists[0], idx_dists[1])]


if __name__ == '__main__':

    with open('data/sdp.txt', 'r') as f:
        content = f.readlines()
    content = [c for c in content if len(c) > 70]

    #t = BertSearcher('openApi', 'base').index_items(content)
    """
    t = AnnoyIndex(1024)
    t.load('tree_builder')
    """
    bert_matcher = BertMatcher(content, None, 'bert', 'large')

    while 1:
        search_question = input("Ask a question: ")
        print(bert_matcher.scored(search_question))


