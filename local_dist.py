__author__ = 'Yueqi'
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
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
df.columns = ["userId", "tid", "w"]
u_group = df.sort_values(by='w', ascending=False).groupby('userId').head(10).groupby('tid')
################################################################################################################################
# for each topic, get internal distance between movies
# user's weight in topic will be considered.
dir = open('data_source_folder','r').readline()
rating = pd.read_pickle(dir+'rating_good.pickle')

for tid in range(0,30):
    res = []
    print(tid)
    mids = m_group.get_group(tid)['mid']
    groups = rating[rating['movieId'].isin(mids)].merge(u_group.get_group(tid), how='inner', on=['userId']).groupby('movieId')
    m_sum = dict((m1, sum(v1['w'])) for m1, v1 in groups)
    m_user = dict((m1, v1[['w','userId']]) for m1, v1 in groups)
    # groups = t_rating
    for m1, v1 in m_user.items():
        # print(tid, m1, len(res))
        for m2, v2 in m_user.items():
            if m1 > m2:
                # enough shared users and positive correlation
                shared = sum(pd.merge(v1, v2, how='inner', on=['userId','w'])['w'])
                j = shared*1.0 / (m_sum[m1]+m_sum[m2]-shared)
                if j > 0.005:
                    res.append({'tid': tid, 'm1': m1, 'm2': m2, 'jacc': j})
                    res.append({'tid': tid, 'm1': m2, 'm2': m1, 'jacc': j})
    pd.DataFrame(res).to_pickle(dir+'res.pickle'+str(tid))