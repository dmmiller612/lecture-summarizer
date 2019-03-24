from summarizer.tables import Summarization, Engine
from typing import List, Set, Dict
from summarizer.lecture_summarizer import SingleModelProcessor
from nltk import tokenize


class SummarizationService(object):

    bert_model = SingleModelProcessor()

    def __init__(self, use_memory=False):
        self.use_memory = use_memory

    def __process_content_sentences(self, body: str) -> List[str]:
        sentences = tokenize.sent_tokenize(body)
        return [c for c in sentences if len(c) > 80 and not c.lower().startswith('but') and
                not c.lower().startswith('and')
                and not c.lower().__contains__('quiz') and
                not c.lower().startswith('or')]

    def create_summary(self):
        pass

    def get_summary(self):
        pass

    def list_summaries(self):
        pass

    def delete_summary(self):
        pass