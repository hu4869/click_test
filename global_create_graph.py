import pandas as pd
import pickle
import networkx as nx

dir = open('data_source_folder','r').readline()
g_dist = pd.concat([pd.read_pickle(dir+'g_res.pickle'+str(i)) for i in range(18)])

bg = nx.DiGraph()
nodes = [int(v) for v in open('mids.txt')]

edges = pd.DataFrame()
for m in nodes:
    df = g_dist[(g_dist['m1']== m) | (g_dist['m2']== m)].sort_values(by='corr', ascending=False).head(100)
    df.reset_index(drop=True, inplace=True)
    for i, t in df.iterrows():
        bg.add_edge(m, t['m1']+t['m2'] - m, weight=i+1)

# pickle the graph
pickle.dump(bg, open(dir+'g_graph.pickle', 'wb'))
