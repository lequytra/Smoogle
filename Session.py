from Conversion import Conversion, is_operand, Et
import numpy as np
import pickle as p
from text_processing_utils import extract_keywords
from nltk.stem import PorterStemmer

class Session:
    def __init__(self):
        self.BIR = None
        self.scores = None
        self.tf_idf = None

    def load(self, path_bir, pscore_path, tf_idf):
        try:
            with open(path_bir, "rb") as f:
                self.BIR = p.load(f)

            with open(pscore_path, "rb") as f:
                self.scores = np.load(f)

            with open(tf_idf, "rb") as f:
                self.tf_idf = p.load(f)
            return True

        except FileNotFoundError:
            print("The input path is not valid. Please check the input paths.")
            return False

    def advance_search(self, query):
        """
            Method takes in a query and evaluate it, retrieve relevant
            documents and rank it based on the PageRank scores.
        :param query:
        :return:
        """

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
        pairs = set(pairs)

        pairs = [i for i in pairs]

        pairs.sort(key=lambda x: x[1], reverse=True)

        docs, scores = zip(*pairs)

        return docs, scores

    def search(self, query):

        scores, kw = extract_keywords(query, stem=True, return_score=True)
        tf_idf = np.empty((0, self.BIR.N))
        tf_idf = np.array([np.append(tf_idf, self.tf_idf[word]) for word in kw])
        tf_idf = np.sum(tf_idf, axis=0)

        retrieved_doc = self.BIR.reduce_union(kw)

        pagerank_score = self.scores[retrieved_doc]
        retrieved_tf = tf_idf[retrieved_doc]

        final = np.multiply(pagerank_score, retrieved_tf)

        res = [i for i in zip(retrieved_doc, final)]
        res.sort(key=lambda x: x[1], reverse=True)
        doc, scores = zip(*res)

        return doc, scores

    def _solve(self, root):

        if root:
            val = root.value
            if is_operand(val):
                return self.BIR.get_posting(val)
            else:
                left = self._solve(root.left)
                right = self._solve(root.right)

                if val == "AND":
                    return self.BIR.intersect(left, right)
                elif val == "OR":
                    return self.BIR.union(left, right)
                else:
                    return self.BIR.diff(left, right)
