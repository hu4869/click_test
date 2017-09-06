__author__ = 'Yueqi'
import pandas as pd
import pickle
import networkx as nx

dir = open('data_source_folder','r').readline()
l_dist = pd.read_pickle(dir+'res.pickle')

# create graph
# remove duplicate movie and re-rank

bg = nx.DiGraph()
nodes = [int(v) for v in open('mids.txt')]

groups = l_dist.groupby('tid')
for tid, g_dist in groups:
    for m in nodes:
        df = g_dist[(g_dist['m1']== m) | (g_dist['m2']== m)].sort_values(by='corr', ascending=False).head(300)
        df.reset_index(drop=True, inplace=True)

        # keep the
        for i, t in df.iterrows():
            n1 = m
            n2 = t['m1']+t['m2'] - m
            if bg.has_edge(n1, n2) and bg[n1][n2]['weight']>i+1:
                bg[n1][n2]['weight'] = i+1
                bg[n1][n2]['tid'] = tid
            else:
                bg.add_edge(n1, n2, weight=i+1, tid=tid)

# pickle the graph
pickle.dump(bg, open(dir+'l_graph.pickle', 'wb'))