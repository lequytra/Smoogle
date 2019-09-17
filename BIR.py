from collections import defaultdict, Counter
import numpy as np
from functools import reduce


class Doc:

    def __init__(self, id, term_freq, most_common):
        self.doc_id = id
        self.term_freq = term_freq
        self.most_common = most_common

    def calc_aug_freq(self):
        return 1 / self.alpha + (1 - 1 / self.alpha) * (self.term_freq / self.most_common)

    def get_freq(self):
        return self.term_freq

    def get_most_common(self):
        return self.most_common


class BIR:
    def __init__(self, normalization_factor=2):
        self.dictionary = defaultdict(tuple)
        self.alpha = normalization_factor
        self.N = 0

    def insert_document(self, doc, idx):
        """
            A method to update the current Inverted Index table
            as a new document is inserted.

            Each term is associated with a posting list, containing the
            documents it is in.



            Params:
                - doc: A list of words contained in the document.
                - idx: The unique index assigned to the document.
        """
        c = Counter(doc)
        most_freq = c.most_common(1)[0][1]

        for term, freq in c.items():
            document = Doc(idx, freq, most_freq, normalization_factor=0.5)
            if self.dictionary.get(term):
                f, postings = self.dictionary[term]

                postings.append(document)
                f += 1

            else:
                f = 1
                postings = [document]

            self.dictionary[term] = (f, postings)

        return

    def intersect(self, p1, p2):
        return np.intersect1d(p1, p2, assume_unique=True)

    def intersect(self, terms):
        """
            Return the document intersections of
            a list of terms

            Param:
                - Terms: Array of terms/words
        """

        # Find the frequency for all terms, in ascending order
        terms = self._get_freq(terms)
        # Get the postings of the term with the shortest frequency
        _, result = self.dictionary[terms[0]]
        terms = terms[1:]

        while len(terms) != 0 and len(result) != 0:
            first_term = terms[0]
            result = self.intersect(result, self.dictionary[first_term])
            terms = terms[1:]

        return result

    def union(self, terms):
        """
            Return the document intersections of
            a list of terms

            Param:
                - Terms: Array of terms/words
        """

        return reduce(np.union1d, [self.dictionary[t][1] for t in terms])

    def diff(p1, p2):
        return np.setdiff1d(p1, p2, assume_unique=True)

    def _get_freq(self, terms):
        """
            Return a list of term-freq pair,
            sorted by frequency
        """
        res = []
        for t in terms:
            freq, _ = self.dictionary[t]
            res += [(terms, freq)]

        res.sort(key=lambda x: x[1])

        return res

    def get_posting(self, term):
        """
            Return a list of postings for the terms
        :param term: a string represent the term
        :return: postings
        """

        if term in self.dictionary:
            return [doc.doc_id for doc in self.dictionary[term][1]]
        else:
            return []

    def get_scores(self, term):
        """
            A method to calculate all tf-idf scores for all documents
            that contain the term
        :param term: the term to look for
        :return: np array : array of scores for all retrieved documents.
        """
        if term in self.dictionary:
            num_doc, postings = self.dictionary[term]
            if num_doc != 0:
                freq = np.array([doc.get_freq() for doc in postings])
                most_common = np.array([doc.get_most_common() for doc in postings])
                tf = np.add(1 / self.alpha, np.multiply((1 - 1 / self.alpha), np.divide(freq, most_common)))
                idf = np.log(self.N, num_doc)

                return np.multiply(tf, idf)

            else:
                print("Term contains no documents")
                return 0
        else:
            print("Term is not in dictionary!")
            return -1

    def get_term(self, term):

        try:
            return [(doc.doc_id, doc.aug_freq) for doc in self.dictionary[term]]

        except KeyError:
            print("The term {} is not currently available in the dictionary.".format(term))
            return []
