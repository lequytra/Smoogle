import pickle as p
from text_processing_utils import extract_keywords
from PageRank import PageRank
from BIR import BIR
import os


def main(content_path='Contents', graph_path='Data/graph.p'):
    # Create BIR
    bir = BIR(normalization_factor=2)
    for filename in os.listdir(content_path):
        idx = filename[:-4]  # Content file must be stored as doc_id.txt
        # Create
        with open("{}/{}".format(content_path, filename)) as f:
            kw = extract_keywords(f.read())
            bir.insert_document(doc=kw, idx=idx)
    # Calculate and save tf-idf table
    bir.create_and_save_tf_idf(filename='tf_idx', path=os.getcwd())
    # Save the BIR to a pickle file
    p.dumps(bir)

    # Upload the web graph
    with open(graph_path) as f:
        graph = p.load(f)

    # Build PageRank using the web graph
    pagerank = PageRank(graph, prev_path=None, damping_factor=0.32, epsilon=0.00000001, default_weight=None)
    # Iterate until converage
    pagerank.iterate(max_iter=100000)
    # Save the PageRank score
    pagerank.save_score(filename=None, path=os.getcwd())

    return True


main(content_path='Contents', graph_path='Data/graph.p')
