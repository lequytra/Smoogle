import os.path
import pickle
import plotly.graph_objects as go
import networkx as nx
from Graph import Graph


curr_dir = os.getcwd()
data_path = os.path.join(curr_dir, 'Data')

G = pickle.load(open(os.path.join(data_path, 'graph.p'), "rb"))

web = nx.DiGraph()
for k in G.graph.keys():
    [web.add_edges_from([(parent,k)]) for parent in G.get(k)]

nx.draw(web, with_labels=True, node_size=1500, alpha=0.3, arrows=True)