from pyltp import Segmentor
from pyltp import SentenceSplitter
import gensim
import re
import os

LTP_DATA_DIR = '/home/tangxuan/programming/ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor = Segmentor()
segmentor.load(cws_model_path)

root = "/home/tangxuan/data/law"


def find_files(root, filenames):
    if os.path.isdir(root):
        for d in os.listdir(root):
            find_files(os.path.join(root, d), filenames)
    else:
        filenames.append(root)


stopwords = open("/home/tangxuan/PycharmProjects/synonyms/data/stopwords.txt").read().split('\n')

stopwords[-1] = stopwords[-1][:-1]
stopwords = set(stopwords)


class Sentences(object):
    def __init__(self, root):
        self.root = root
        self.filenames = []
        find_files(root, self.filenames)

        self.cnt = 0
        # self.filenames = self.filenames[:10]

    def __iter__(self):
        for fname in self.filenames:
            self.cnt += 1
            if self.cnt % 1000 == 0:
                print(self.cnt)

            for line in open(fname):
                sents = SentenceSplitter.split(line)
                sents = [re.sub(r'[^\u4e00-\u9fa5]+', '', sent) for sent in sents]
                for sent in sents:
                    if len(sent) > 1:
                        words = segmentor.segment(sent)
                        temp = []
                        for word in words:
                            if word not in stopwords:
                                temp.append(word)
                        yield temp


sents = Sentences(root)

model = gensim.models.Word2Vec(sents, min_count=5, size=100, workers=4)
model_path = '/home/tangxuan/data/wordvec.model'
model.save(model_path)
segmentor.release()