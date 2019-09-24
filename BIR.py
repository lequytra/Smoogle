from collections import defaultdict, Counter
import numpy as np
import os
import pickle as p
from functools import reduce


class Doc:

    def __init__(self, idx, term_freq, most_common):
        self.doc_id = int(idx)
        self.term_freq = term_freq
        self.most_common = most_common

    def get_freq(self):
        return self.term_freq

    def get_most_common(self):
        return self.most_common

    def get_id(self):
        return self.doc_id


class BIR:
    def __init__(self, normalization_factor=2):
        self.dictionary = dict()
        self.alpha = normalization_factor
        self.N = 400

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
        self.N += 1
        if not doc or len(doc) == 0:
            return
        c = Counter(doc)
        # Get the highest frequency

        if not c:
            return

        most_freq = c.most_common(1)[0][1]

        for term, freq in c.items():
            # Create a document object
            document = Doc(idx, freq, most_freq)
            # If the term already exists in the dictionary
            if self.dictionary.get(term):
                f, postings = self.dictionary[term]

                postings.append(document)
                self.dictionary[term] = (f + 1, postings)

            else:
                f = 1
                postings = [document]
                # Add the term and its information to the dictionary
                self.dictionary[term] = (f, postings)



        return

    def intersect_by_terms(self, term1, term2):

        p1, p2 = self.get_ids_by_term(term1), self.get_ids_by_term(term2)

        return np.intersect1d(p1, p2, assume_unique=True).astype(int)

    def intersect(self, p1, p2):
        return np.intersect1d(p1, p2, assume_unique=True).astype(int)

    def reduce_intersect(self, terms):
        """
            Return the document intersections of
            a list of terms

            Param:
                - Terms: Array of terms/words
        """

        # Find the frequency for all terms, in ascending order
        terms, _ = self._get_freq(terms)
        del _
        # Get the postings of the term with the shortest frequency
        postings = [self.get_ids_by_term(t) for t in terms]

        return reduce(np.intersect1d, postings).astype(int)

    def union_by_terms(self, term1, term2):

        p1, p2 = self.get_ids_by_term(term1), self.get_ids_by_term(term2)

        return np.union1d(p1, p2).astype(int)

    def union(self, p1, p2):
        return np.union1d(p1, p2).astype(int)

    def reduce_union(self, terms):
        """
            Return the document intersections of
            a list of terms

            Param:
                - Terms: Array of terms/words
        """
        postings = [self.get_ids_by_term(t) for t in terms]

        return reduce(np.union1d, postings).astype(int)

    def diff_by_terms(self, term1, term2):

        p1, p2 = self.get_ids_by_term(term1), self.get_ids_by_term(term2)

        return np.setdiff1d(p1, p2, assume_unique=True).astype(int)

    def diff(self, p1, p2):
        return np.setdiff1d(p1, p2, assume_unique=True).astype(int)

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
            return np.array([int(doc.doc_id) for doc in self.dictionary[term][1]])
        else:
            return np.empty(shape=(0,))

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
                print("Term is contained in no documents")
                return 0
        else:
            print("Term is not in dictionary!")
            return -1

    def get_ids_by_term(self, term):

        return [doc.get_id() for doc in self.dictionary[term][1] if term in self.dictionary]

    def get_term(self, term):

        try:
            return [(doc.doc_id, doc.aug_freq) for doc in self.dictionary[term]]

        except KeyError:
            print("The term {} is not currently available in the dictionary.".format(term))
            return []

    def create_tf_idf(self):
        """
            A method to create a 2D array containing the tf-idx scores for all
            (term, document) pair.
        :return: a 2D numpy array
        """
        tf_table = {}

        for term in self.dictionary.keys():
            num_doc, postings = self.dictionary[term]
            all_doc = np.zeros((self.N,))
            if num_doc != 0:
                freq = np.array([doc.get_freq() for doc in postings])
                most_common = np.array([doc.get_most_common() for doc in postings])
                tf = np.add(1 / self.alpha, np.multiply((1 - 1 / self.alpha), np.divide(freq, most_common)))
                idf = np.log2(np.array([self.N / num_doc]))

                scores = np.multiply(tf, idf)
            else:
                scores = np.zeros((self.N,))

            all_doc[np.array([doc.doc_id for doc in postings], dtype=np.intp)] = scores

            tf_table[term] = all_doc

        return tf_table

    def create_and_save_tf_idf(self, filename=None, path=None):
        tf_table = self.create_tf_idf()

        if not filename:
            filename = 'tf_idf.p'

        if not path:
            path = os.path.join(os.getcwd(), 'Data', filename)
        else:
            path = os.path.join(path, 'Data', filename)

        try:
            with open(path, 'wb') as f:
                p.dump(tf_table, f)
            return True

        except FileNotFoundError:
            print("Cannot save file")
            return False

    def save(self, save_bir=True, filename=None, filename_bir=None, path=None):
        if not filename:
            filename = 'document_data.p'
        if not filename_bir:
            filename_bir = 'bir.p'

        if not path:
            path = os.path.join(os.getcwd(), 'Data')
        else:
            path = os.path.join(path, 'Data')

        if not os.path.exists(path):
            os.makedirs(path)

        path1 = os.path.join(path, filename)

        with open(path1, "wb") as f:
            p.dump(self, f)

        if save_bir:
            bir = {}
            for key, item in self.dictionary.items():
                bir[key] = self.get_posting(key)
            path2 = os.path.join(path, filename_bir)
            with open(path2, "wb") as f:
                p.dump((bir, self.N), f)

        return
