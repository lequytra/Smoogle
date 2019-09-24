from Session import Session
import os


def run():
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
    running = True
    while running:
        pass
