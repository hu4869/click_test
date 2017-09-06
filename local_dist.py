__author__ = 'Yueqi'
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

dir = open('data_source_folder','r').readline()
rating = pd.read_pickle(dir+'rating.pickle')
##################################################################################################################################
# load topic model
# only in or not in a topic
# find movies in topic
df = pd.read_csv('weight.txt', sep='\t', header=None, names=["tid", "mid", "w"]).astype(int)
m_group = df[df['w'] > 10].sort_values(by='w', ascending=False).groupby('mid').head(10).groupby('tid')
# find users in topic
a = []
df = pd.read_csv('doc', sep='\t', header=None, skiprows=1)
for row in df.iterrows():
    row = row[1]
    for i in range(1, 11):
        if row[i*2+1] > 0.05:
            a.append([int(row[1]), int(row[i*2]), row[i*2+1]])
        else:
            break
df = pd.DataFrame(a)
df.columns = ["uid", "tid", "w"]
u_group = df.sort_values(by='w', ascending=False).groupby('uid').head(10).groupby('tid')
################################################################################################################################
# for each topic, get internal distance between movies
res = []
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import cosine
for tid in range(0,30):
    print(tid)
    mids = m_group.get_group(tid)['mid']
    uids = u_group.get_group(tid)['uid']
    t_rating = rating[rating['movieId'].isin(mids) & rating['userId'].isin(uids)]

    groups = t_rating.groupby('movieId')
    for m1, v1 in groups:
        print(m1)
        for m2, v2 in groups:
            if m1 < m2:
                # enough shared users and positive correlation
                shared = pd.merge(v1, v2, how='inner', on=['userId'])
                if len(shared) > 40:
                    r, pv = pearsonr(shared['rating_x'], shared['rating_y'])
                    if r > 0:
                        res.append({'tid': tid, 'm1': m1, 'm2': m2, 'corr': r, 'cos': cosine(shared['rating_x'], shared['rating_y'])})

pd.DataFrame(res).to_pickle(dir+'res.pickle')