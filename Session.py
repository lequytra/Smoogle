from Conversion import Conversion, is_operand, Et
import numpy as np
import pickle as p
from text_processing_utils import extract_keywords
from nltk.stem import PorterStemmer
from functools import reduce


class Session:
    def __init__(self):
        self.BIR = None
        self.scores = None
        self.tf_idf = None
        self.N = None

    def load(self, path_bir, pscore_path, tf_idf):
        try:
            with open(path_bir, "rb") as f:
                self.BIR, self.N = p.load(f)

            with open(pscore_path, "rb") as f:
                self.scores = np.load(f)

            with open(tf_idf, "rb") as f:
                self.tf_idf = p.load(f)

            return True

        except FileNotFoundError:
            print("The input path is not valid. Please check the input paths.")
            return False

    def advance_search(self, query, top_k=10):
        """
            Method takes in a query and evaluate it, retrieve relevant
            documents and rank it based on the PageRank scores.
        :param top_k:
        :param query:
        :return:
        """
        print("Searching through {} documents...".format(self.N))
        c = Conversion()

        if "AND" not in query and "NOT" not in query and "OR" not in query:
            self.search(query)
            return self.BIR.reduce_intersect()

        ps = PorterStemmer()
        kw = [ps.stem(word) if is_operand(word) else word for word in query.split()]
        query = " ".join(kw)
        del kw

        postfix = c.infix_to_postfix(query)
        root = c.constructTree(postfix)
        del c, postfix

        found = self._solve(root)

        found_scores = self.scores[found]

        pairs = [(f, s) for f, s in zip(found, found_scores)]
        pairs = list(set(pairs))

        pairs.sort(key=lambda x: x[1], reverse=True)

        docs, scores = zip(*pairs)

        print("Found {} in {} documents!!".format(len(docs), self.N))
        print("Returning {}".format(top_k))

        return docs[:top_k], scores[:top_k]

    def search(self, query, top_k=10):

        print("Searching through {} documents...".format(self.N))

        kw = extract_keywords(query, stem=True)
        print(kw)
        tf_idf = np.empty((0, self.N))

        tf_idf = np.array([np.append(tf_idf, self.tf_idf[word]) for word in kw if word in self.BIR])
        tf_idf = np.sum(tf_idf, axis=0)

        postings = [self.BIR[t] for t in kw if t in self.BIR]

        retrieved_doc = reduce(np.union1d, postings).astype(int)

        pagerank_score = self.scores[retrieved_doc]
        retrieved_tf = tf_idf[retrieved_doc]

        final = np.multiply(pagerank_score, retrieved_tf)

        res = sorted(zip(retrieved_doc, final), key=lambda x: x[1], reverse=True)

        doc, scores = zip(*res)

        print("Found {} in {} documents!!".format(len(doc), self.N))
        print("Returning {}".format(top_k))

        return doc[:top_k], scores[:top_k]

    def _solve(self, root):

        if root:
            val = root.value
            if is_operand(val):
                return self.BIR[val]
            else:
                left = self._solve(root.left)
                right = self._solve(root.right)

                if val == "AND":
                    return np.intersect1d(left, right)
                elif val == "OR":
                    return np.union1d(left, right)
                else:
                    return np.setdiff1d(left, right)
