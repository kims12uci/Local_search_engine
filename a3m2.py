import json
from nltk.stem import PorterStemmer

class SearchEngine:
    def __init__(self, index_file='index.json', url_file='hash_url.json'):
        self.index = self.read_file(index_file) #{token: [frequency in number of docs, {doc_id: [tf, [index of occurrence]]}, idf]}
        self.urls = self.read_file(url_file)
        self.toks = []

    def read_file(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
            return data

    def get_tok(self, tok):
        return self.index[tok]

    def tokenize(self, line):
        if not line:
            return None

        ps = PorterStemmer()
        ret = []
        for char in line:
            if not char.isalnum():
                line = line.replace(char, ' ')

        for words in line.split(' '):
            if words != "":
                ret.append(ps.stem(words.lower()))
        return ret


    def search(self, inp):
        self.toks = []
        query = self.tokenize(inp)
        if not query:
            return None

        temp = {}
        for token in set(query):
            if token in self.index:
                temp[token] = self.index[token][2]

        if not temp:
            return None

        sorted_toks = [k for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)]
        if len(sorted_toks) > 3:
            sorted_toks = sorted_toks[:len(sorted_toks) - (len(sorted_toks)//3)]

        docs = set(self.index[sorted_toks[0]][1].keys())
        self.toks = sorted_toks

        if len(sorted_toks) > 1:
            for toks in sorted_toks[1:]:
                docs = set(self.index[toks][1].keys()).union(docs)

        return docs

    def rank(self, docs):
        if not docs:
            return None

        temp = {}
        if len(self.toks) > 1:
            for doc in docs:
                temp[doc] = 0
                for tok in self.toks:
                    if tok in self.index and doc in self.index[tok][1]:
                        temp[doc] += self.index[tok][1][doc][0] * self.index[tok][2]
        else:
            for doc in docs:
                temp[doc] = 0
                temp[doc] += self.index[self.toks[0]][1][doc][0]

        return [k for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)]


    def output(self, docs):
        if not docs:
            print("No Result Found")
            return None

        lim = 5
        for doc in docs:
            print(self.urls[doc])
            lim -= 1
            if lim == 0:
                break

    def run(self):
        qu = input("please enter search query, or type 'q' to end: ")
        while qu != "q":
            self.output(self.rank(self.search(qu)))
            qu = input("please enter search query, or type 'q' to end: ")


if __name__ == '__main__':
    SearchEngine().run()
