import pickle as p
from text_processing_utils import extract_keywords
from PageRank import PageRank
from BIR import BIR
import os
import time


def main(content_path='Contents', graph_path='Data/graph.p', bir_name=None):
    if not bir_name:
        # Create BIR
        bir = BIR(normalization_factor=2)

    else:
        with open("{}/{}".format('Data', bir_name), 'rb') as f:
            bir = p.load(f)
    n_file = 0
    for filename in os.listdir(content_path):
        if not filename.startswith('.'):
            idx = int(filename[:-4])  # Content file must be stored as doc_id.txt
            with open("{}/{}".format(content_path, filename), 'r') as f:
                if n_file % 100 == 0:
                    print("Have Parsed {} documents".format(n_file))
                kw = extract_keywords(f.read())
                bir.insert_document(doc=kw, idx=idx)
                n_file += 1
    # Calculate and save tf-idf table
    print("Create BIR and tf-idf for all documents...")
    bir.create_and_save_tf_idf(filename='tf_idx.p', path=os.getcwd())
    # Save the BIR to a pickle file
    print("Saving Inverted Index Table...")
    bir.save(path=os.getcwd())

    # Upload the web graph
    with open(graph_path, 'rb') as f:
        graph = p.load(f)

    print("Calculate PageRank ...")
    # Build PageRank using the web graph
    pagerank = PageRank(graph, prev_path=None, damping_factor=0.32, epsilon=0.0000001, default_weight=None)
    # Iterate until converge
    pagerank.iterate(max_iter=100000)

    # Save the PageRank score
    pagerank.save_score(filename=None, path=os.getcwd())
    print("Finished!!!")

    return True


now = time.time()
main(content_path='Contents', graph_path='Data/graph.p', bir_name=None)
print("Setup takes {} seconds to run".format(time.time() - now))
