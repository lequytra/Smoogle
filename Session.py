from Conversion import Conversion, is_operand, Et
import numpy as np
import pickle as p
from text_processing_utils import extract_keywords


class Session:
    def __init__(self):
        self.BIR = None
        self.scores = None

    def load(self, path_bir, path_score):
        try:
            with open(path_bir) as f:
                self.BIR = p.loads(path_bir)
            with open(path_score) as f:
                self.scores = np.load(f)

        except FileNotFoundError:
            print("The input path is not valid.")

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
            return self.BIR.intersect()

        postfix = c.infix_to_postfix(query)
        root = c.constructTree(postfix)

        del c
        del postfix

        found = self._solve(root)

        found_scores = self.scores[found]

        pairs = [(f, s) for f, s in zip(found, found_scores)]

        pairs.sort(key=lambda x: x[1])

        return pairs

    def search(self, query):
        # TODO: Implement ranking documents on importance of the terms it contains

        scores, kw = extract_keywords(stem=True, return_score=True)

        return

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
