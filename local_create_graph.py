__author__ = 'Yueqi'
import pandas as pd

dir = open('data_source_folder','r').readline()
l_dist = pd.concat([pd.read_pickle(dir+'res.pickle'+str(i)) for i in range(30)])
l_dist = l_dist.sort_values(by='jacc', ascending=False).groupby(['m1','tid']).head(50)

# calculate number of operation to access the topic from a movie
# rank topic on each focal
topics = pd.read_csv('weight.txt', sep='\t', header=None, names=["tid", "m1", "w"]).astype(int)
topics = topics[topics['w'] > 10]
topics['t_rank'] = topics.groupby('m1')['w'].rank(ascending=False)-1
l_dist = pd.merge(l_dist, topics[topics['t_rank']<10], how='inner', on=['tid','m1'])
l_dist['dist'] = l_dist.groupby(['tid','m1'])['jacc'].rank(ascending=False) + l_dist['t_rank']

import networkx as nx
bg = nx.DiGraph()
nodes = [int(v) for v in open('mids.txt')]

for (m1, m2), dist in l_dist.groupby(['m1','m2']).min()['dist'].iteritems():
    bg.add_edge(m1, m2, weight=dist)

# pickle the graph
import pickle
pickle.dump(bg, open(dir+'l_graph.pickle', 'wb'))
