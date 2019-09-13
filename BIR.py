from collections import defaultdict, Counter
import numpy as np
from functools import reduce
import nltk

class Doc:
	def __init__(self, id, term_freq, most_common, normalization_factor=0.5):
		self.doc_id = id
		self.aug_freq = normalization_factor + (1 - normalization_factor)*(term_freq/most_common)

class BIR:
	def __init__(self):
		self.dictionary = defaultdict(tuple)
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
				posting = [document]

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

	def get_term(self, term):

		try:
			return [(doc.doc_id, doc.aug_freq) for doc in self.dictionary[term]]

		except KeyError:
			print("The term {} is not currently available in the dictionary.".format(term))