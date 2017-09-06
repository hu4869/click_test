__author__ = 'Yueqi'
import pandas as pd
import pickle
import networkx as nx

# l_dist = pd.read_pickle('res/res.pickle')
#
# # create graph
# # remove duplicate movie and re-rank
#
# bg = nx.DiGraph()
# nodes = [int(v) for v in open('mids.txt')]
#
# groups = l_dist.groupby('tid')
# for tid, g_dist in groups:
#     for m in nodes:
#         df = g_dist[(g_dist['m1']== m) | (g_dist['m2']== m)].sort_values(by='corr', ascending=False).head(300)
#         df.reset_index()
#
#         # keep the
#         for i, t in df.iterrows():
#             n1 = m
#             n2 = t['m1']+t['m2'] - m
#             if bg.has_edge(n1, n2) and bg[n1][n2]['weight']>i+1:
#                 bg[n1][n2]['weight'] = i+1
#                 bg[n1][n2]['tid'] = tid
#             else:
#                 bg.add_edge(n1, n2, weight=i+1, tid=tid)
#
# # pickle the graph
# pickle.dump(bg, open('l_graph.pickle', 'wb'))
bg = pickle.load(open('l_graph.pickle', 'rb'))

# shortest path
# get the reliable user sample
# rating = pd.read_pickle('rating.pickle')
# grouped = rating.groupby('userId').filter(lambda x: 2000 > len(x) > 500 and max(x['timestamp'])-min(x['timestamp'])>400000000)[['userId','movieId']]
# pickle.dump(bg, open('l_graph.pickle', 'wb'))
# read from pickle
grouped = pd.read_pickle('top_user.pickle').groupby('userId')

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