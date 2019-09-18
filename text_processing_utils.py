from rake_nltk import Rake
from nltk.stem import PorterStemmer
import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def extract_keywords(query, stem=True, return_score=False):
    r = Rake()
    r.extract_keywords_from_text(query)
    ls = r.get_ranked_phrases_with_scores()

    scores, kw = zip(*ls)

    scores = normalize(scores)

    if stem:
        ps = PorterStemmer()
        kw = [ps.stem(word) for word in kw]

    if return_score:
        return scores, kw
    else:
        return kw
