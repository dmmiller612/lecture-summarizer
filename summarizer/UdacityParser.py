from nltk import tokenize


class UdacityParser(object):

    def __init__(self, file_path):
        with open(file_path) as d:
            self.all_data = d.readlines()

    def __isint(self, v):
        try:
            int(v)
            return True
        except:
            return False

    def __should_skip(self, v):
        return self.__isint(v) or v == '\n' or '-->' in v

    def __process_sentences(self, v):
        sentence = tokenize.sent_tokenize(v)
        return sentence

    def save_data(self, save_path, sentences):
        with open(save_path, 'w') as f:
            for sentence in sentences:
                f.write("%s\n" % sentence)

    def run(self):
        total = ''
        for data in self.all_data:
            if not self.__should_skip(data):
                cleaned = data.replace('&gt;', '').replace('\n', '')
                total += ' ' + cleaned
        sentences = self.__process_sentences(total)
        return sentences
