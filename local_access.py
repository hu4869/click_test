__author__ = 'Yueqi'
import pandas as pd
import pickle
import networkx as nx

dir = open('data_source_folder','r').readline()
bg = pickle.load(open(dir + 'l_graph.pickle', 'rb'))

# read from pickle
grouped = pd.read_pickle(dir+'top_user.pickle').groupby('userId')

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

pd.DataFrame(d).to_pickle(dir+'g_click_dist')