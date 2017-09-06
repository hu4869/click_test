__author__ = 'Yueqi'
# the average length of the shortest path between items in global exploration.
import pandas as pd
import pickle
import networkx as nx

g_dist = pd.concat([pd.read_pickle('res/g_res.pickle'+str(i)) for i in range(18)])

# filter nodes
nodes = [int(v) for v in open('mids.txt')]
g_dist = g_dist[(g_dist['m1'].isin(nodes)) | (g_dist['m2'].isin(nodes))]

bg = nx.DiGraph()

for m in nodes:
    df = g_dist[(g_dist['m1']== m) | (g_dist['m2']== m)].sort_values(by='corr', ascending=False).head(300)
    df.reset_index()
    for i, t in df.iterrows():
        bg.add_edge(m, t['m1']+t['m2'] - m, weight=i)

# pickle the graph
pickle.dump(bg, open('g_graph.pickle', 'wb'))
bg = pickle.load(open('g_graph.pickle', 'rb'))

# shortest path
# get the reliable user sample
rating = pd.read_pickle('rating.pickle')
grouped = rating.groupby('userId').filter(lambda x: 2000 > len(x) > 500 and max(x['timestamp'])-min(x['timestamp'])>400000000)[['userId','movieId']]

# read from pickle
pickle.dump(bg, open('user_sample.pickle', 'wb'))
grouped = pd.read_pickle('user_sample.pickle').groupby('userId')

# get the average distance
# distance buffer
buffer = {}
d = []
import numpy as np
for uid, df in grouped:
    dist = []
    bre = 0
    list = df['movieId'].values
    for m1 in list:
        for m2 in list:
            if m1 != m2:
                if (m1, m2) not in buffer.keys():
                    try:
                        tmp = nx.dijkstra_path_length(bg, m1, m2, weight='weight')
                        buffer[(m1, m2)] = tmp
                        print(m1, m2, tmp)
                    except nx.NetworkXNoPath:
                        bre += 1
                        print('break')
                if (m1, m2) in buffer:
                    dist.append(buffer[(m1, m2)])

    print({'uid': uid, 'aver':np.mean(dist), 'break': bre})
    d.append({'uid': uid, 'aver':np.mean(dist), 'break': bre})

pd.DataFrame(d).to_pickle('g_click_dist')