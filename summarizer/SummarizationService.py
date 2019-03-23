from summarizer.tables import Summarization, Engine
from typing import List, Set, Dict


class SummarizationService(object):

    def __init__(self, use_memory=False):
        self.use_memory = use_memory

    def create_summary(self):
        pass

    def get_summary(self):
        pass

    def list_summaries(self):
        pass

    def delete_summary(self):
        pass