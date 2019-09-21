from Graph import Graph
from PageRank import PageRank
from Session import Session
import os

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
    res1 = s.advance_search(q1)
    res2 = s.search(q2)
    print("Results for advanced search: ")
    print(res1)
    print("Results for intelligent search: ")
    print(res2)
    return True

    return


test_session()
