from Session import Session
import os
import sys
import csv

def main():
    se = Session()
    curr_dir = os.getcwd()
    path_bir = os.path.join(curr_dir, 'Data', 'bir.p')
    pscore_path = os.path.join(curr_dir, 'Data', 'PageRank_score.npy')
    tf_idf = os.path.join(curr_dir, 'Data', 'tf_idx.p')

    try:
        print ("Setting up Smoogle...")
        se.load(path_bir, pscore_path, tf_idf)
    except FileNotFoundError:
        print("Cannot find necessary files!!! Try running setup file??!")
        return False
    
    ciu = csv. reader(open(os.path.join(curr_dir, 'Data', 'c_id_url.csv')))
    crawl_id_url = {}
    for row in ciu:
        crawl_id_url.update({int(row[0]): row[1]})

    running = True
    print("Welcome to Smoogle Search: ")
    while running:
        print("Please enter options (s/a/q): ")
        print("s - search a - advanced search q - quit")
        arg = input()
        if arg != False:
            if arg == 's' or arg == 'a':
                query = input("Please enter search query: ")
                num = input("Please enter the number of web pages to show ")
                if (arg == 's'):
                    results = se.search(query, int(num))
                else:
                    results = se.advance_search(query, int(num))
                for result in results[0]:
                    print(crawl_id_url.get(result))
            elif arg == 'q':
                running = False
            else:
                print("This is wrong command!")
        else:
            return False

if __name__ == "__main__":
    main()

