from Session import Session
import os
import sys

def main():
    se = Session()
    curr_dir = os.getcwd()
    path_bir = os.path.join(curr_dir, 'Data', 'bir.p')
    pscore_path = os.path.join(curr_dir, 'Data', 'PageRank_score.npy')
    tf_idf = os.path.join(curr_dir, 'Data', 'tf_idx.p')

    try:
        se.load(path_bir, pscore_path, tf_idf)
    except FileNotFoundError:
        print("Cannot find necessary files!!! Try running setup file??!")
        return False
    
    running = True
    print("Welcome to Smoogle Search: ")
    while running:
        print("Please enter options (s/a/q): ")
        print("s - search a - advanced search q - quit")
        arg = input()
        print(arg)
        if arg != False:
            if arg == 's' or arg == 'a':
                query = input("Please enter search query: ")
                if (arg == 's'):
                    se.search(query)
                else:
                    se.advance_search(query)
            elif arg == 'q':
                running = False
            else:
                print("This is wrong command!")
        else:
            return False

if __name__ == "__main__":
    main()