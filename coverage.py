# the number of item that can be reached within n steps
# store in map
dir = open('data_source_folder','r').readline()
import pickle
import networkx as nx
path = pickle.load(open(dir+'l_distance','rb'))
g_path = pickle.load(open(dir+'g_distance','rb'))

w = open('coverage','w')
# get # of m2 that can be reach in n steps
from collections import Counter

cnt = 0
for m, v1 in path.items():
    for r in range(1, 20):
        l_v = len([v for v in v1.values() if v<r])
        g_v = len([v for v in g_path[m].values() if v<r])
        w.write('%s,%s,%s,%s\n'%(int(m),r,l_v,g_v))