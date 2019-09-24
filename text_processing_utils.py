from rake_nltk import Rake
from nltk.stem import PorterStemmer
import numpy as np
import nltk


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def extract_keywords(query, stem=True):
    r = Rake()
    r.extract_keywords_from_text(query)
    kw = r.get_ranked_phrases()
    word_ls = nltk.word_tokenize(query)

    total = set(kw + word_ls)

    if stem:
        ps = PorterStemmer()
        return list(map(ps.stem, total))

    else:
        return list(total)
