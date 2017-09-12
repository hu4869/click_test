__author__ = 'Yueqi'
# the average length of the shortest path between items in global exploration.
import pandas as pd
import pickle
import networkx as nx
dir = open('data_source_folder','r').readline()
bg = pickle.load(open(dir+'g_graph.pickle', 'rb'))

# get all pair distance (length)
length = nx.all_pairs_dijkstra_path_length(bg)
pickle.dump(length, open(dir+'g_distance','wb'))