import pickle as p
from text_processing_utils import extract_keywords
from PageRank import PageRank
from BIR import BIR
import os


def main(content_path='Contents', graph_path='Data/graph.p', bir_name=None):
    if not bir_name:
        # Create BIR
        bir = BIR(normalization_factor=2)
    else:
        with open("{}/{}".format('Data', bir_name), 'rb') as f:
            bir = p.load(f)

    for filename in os.listdir(content_path):
        idx = filename[:-4]  # Content file must be stored as doc_id.txt
        if not filename.startswith('.'):
            with open("{}/{}".format(content_path, filename), 'r') as f:
                kw = extract_keywords(f.read())
                bir.insert_document(doc=kw, idx=idx)
    # Calculate and save tf-idf table
    bir.create_and_save_tf_idf(filename='tf_idx.p', path=os.getcwd())
    # Save the BIR to a pickle file
    bir.save(filename=bir_name, path=None)

    # Upload the web graph
    with open(graph_path, 'rb') as f:
        graph = p.load(f)

    # Build PageRank using the web graph
    pagerank = PageRank(graph, prev_path=None, damping_factor=0.32, epsilon=0.00000001, default_weight=None)
    # Iterate until converge
    pagerank.iterate(max_iter=100000)
    # Save the PageRank score
    pagerank.save_score(filename=None, path=os.getcwd())

    return True


main(content_path='Contents', graph_path='Data/graph.p', bir_name='bir.p')
