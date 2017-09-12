# diversity within the top N items
dir = open('data_source_folder','r').readline()
import pickle
import networkx as nx
path = pickle.load(open(dir+'l_distance','rb'))
g_path = pickle.load(open(dir+'g_distance','rb'))

import pandas as pd
c_dist = pd.read_pickle(dir+'c_dist.pickle')

def average_c_dist(m_list):
    return c_dist[c_dist['m1'].isin(m_list)&c_dist['m2'].isin(m_list)]['dist'].mean()

w = open('diversity','w')
N = 100
import operator
for m, v1 in path.items():
    v2 = g_path[m]
    l_d = average_c_dist(sorted(v1, key=v1.get)[:N])
    g_d = average_c_dist(sorted(v2, key=v2.get)[:N])
    w.write('%s,%s,%s\n'%(int(m), l_d, g_d))

