from Graph import Graph
from PageRank import PageRank
from Session import Session
import os
import base64
import pickle
import csv
import time

def test_graph_score():
    g = Graph()
    g.insert_edge(0, 1)
    g.insert_edge(0, 4)
    g.insert_edge(1, 2)
    g.insert_edge(1, 3)
    g.insert_edge(2, 0)
    g.insert_edge(3, 2)
    g.save_graph()
    p = PageRank(g)
    p.iterate(max_iter=None)
    p.save_score()

    return True


def test_session():
    s = Session()
    curr_dir = os.getcwd()
    path_bir = os.path.join(curr_dir, 'Data', 'bir.p')
    pscore_path = os.path.join(curr_dir, 'Data', 'PageRank_score.npy')
    tf_idf = os.path.join(curr_dir, 'Data', 'tf_idx.p')

    try:
        s.load(path_bir, pscore_path, tf_idf)
    except FileNotFoundError:
        print("Cannot find necessary files!!! Try running setup file??!")
        return False

    q1 = "Biologists AND long OR Grinnell"
    q2 = "biologists has long been Grinnell"
    now = time.time()
    res1 = s.advance_search(q1)
    now2 = time.time()
    res2 = s.search(q2)
    now3 = time.time()
    print("Results for advanced search: ")
    print(res1)
    print("Search takes {}".format(now2 - now))
    print("Results for intelligent search: ")
    print(res2)
    print("Search takes {}".format(now3 - now))
    return True

    return


test_session()
#
# your_pickle_obj = pickle.loads(open("/mnt/c/Users/stella/Documents/Github/Search-Engine/Data/Graph.p", 'rb').read())
# with open('output.csv', 'a', encoding='utf8') as csv_file:
#     wr = csv.writer(csv_file, delimiter='|')
#     pickle_bytes = pickle.dumps(your_pickle_obj)            # unsafe to write
#     b64_bytes = base64.b64encode(pickle_bytes)  # safe to write but still bytes
#     b64_str = b64_bytes.decode('utf8')          # safe and in utf8
#     wr.writerow(['col1', 'col2', b64_str])
