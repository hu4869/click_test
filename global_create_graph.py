import pandas as pd
dir = open('data_source_folder','r').readline()
g_dist = pd.read_pickle(dir+'g_res.pickle')
g_dist = g_dist.sort_values(by='jacc', ascending=False).groupby('m1').head(50)
group = g_dist.groupby('m1')

import networkx as nx
bg = nx.DiGraph()

for m1, g in group:
    a = g
    a = a.reset_index()
    for index, row in a.iterrows():
        bg.add_edge(m1, row['m2'], weight=index)

# pickle the graph
import pickle
pickle.dump(bg, open(dir+'g_graph.pickle', 'wb'))
