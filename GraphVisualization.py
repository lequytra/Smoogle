import os.path
import pickle
import plotly.graph_objects as go
import networkx as nx
from Graph import Graph


curr_dir = os.getcwd()
data_path = os.path.join(curr_dir, 'Data')

G = pickle.load(open(os.path.join(data_path, 'graph.p'), "rb"))

web = nx.DiGraph()
count =1

print(all(isinstance(n, int) for n in list(G.graph.keys())))
for k in list(G.graph.keys()):
    for parent in G.get(k):
        len(parent)

for k in G.graph.keys():
    #[web.add_edge(parent,k) for parent in G.get(k)]
    print(type(G.get(k)))
    print(G.get(k))
    for parent in G.get(k):
        print("this is start")
        i_parent = str(parent)
        i_child = str(k)
        print(str(type(parent)) + str(parent))
        print("k "+ str(type(k)) + str(k))
        web.add_edge(i_parent, i_child)
        break
    if count > 1:
        break
    else:
        pass
    count+=1

#print(web.nodes())
#print(web.edges())

nx.draw(web, with_labels=True, node_size=1500, alpha=0.3, arrows=True)

for k in list(G.graph.keys()):
    if isinstance(k, int) == False:
        k = int(k)

    
