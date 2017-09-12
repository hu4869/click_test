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

# calculate number of operation to access the topic from a movie
# sort movie by weights
topics = pd.read_csv('weight.txt', sep='\t', header=None, names=["tid", "mid", "w"]).astype(int)
topics = topics[topics['w'] > 10]
topics['rank'] = topics.groupby('mid')['w'].rank()

groups = l_dist.groupby('tid')
from math import log
for tid, g_dist in groups:
    for m in l_dist[l_dist['tid'] == tid]['m1'].unique():
        m_t = topics[topics['tid'] == tid][topics['mid'] == m]
        if len(m_t) == 0:
            print('error!')
            continue

        t_dist2m = log(float(m_t['rank']),2)
        df = g_dist[(g_dist['m1'] == m) | (g_dist['m2']== m)].sort_values(by='corr', ascending=False).head(5)
        df.reset_index(drop=True, inplace=True)

        # keep the
        for i, t in df.iterrows():
            n1 = m
            n2 = t['m1']+t['m2'] - m
            if bg.has_edge(n1, n2) and bg[n1][n2]['weight'] > i+t_dist2m+1:
                bg[n1][n2]['weight'] = i+t_dist2m+1
            else:
                bg.add_edge(n1, n2, weight=i+t_dist2m+1)
    print (tid)

# pickle the graph
pickle.dump(bg, open(dir+'l_graph.pickle', 'wb'))
