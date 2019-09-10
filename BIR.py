from collections import defaultdict
import numpy as np 
from functools import reduce
import nltk

class BIR:
	def __init__(self):
		self.dictionary = defaultdict(tuple)

	def insert_document(self, doc, idx):
		"""
			A method to update the current Inverted Index table
			as a new document is inserted. 

			Params:
				- doc: A set of words contained in the document.
				- idx: The unique index assigned to the document. 
		"""
		doc = set(doc)
		for word in doc:
			word = word.lower()

			if self.dictionary.get(word):
				self.dictionary[word] = (self.dictionary[word][0] + 1, np.append(self.dictionary[word][1], idx))

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

		res.sort(key=lambda x:x[1])

		return res

