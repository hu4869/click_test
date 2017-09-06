__author__ = 'Yueqi'
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# # load rating
# # consider movies already in the database only.
# cnx = create_engine("mysql://root:yueyue@localhost/recom")
# mids = pd.read_sql('select mid from movie',cnx).values.flatten().tolist()
# iter_csv = pd.read_csv('../ml-latest-small/ratings.csv',
#                         dtype={'userId': np.int32, 'movieId': np.int64, 'rating': np.float64, 'timestamp': np.int64},
#                         iterator=True, chunksize=1000)
# rating = pd.concat([chunk[chunk['movieId'].isin(mids)] for chunk in iter_csv])

# load from pickle
rating = pd.read_pickle('rating.pickle')
##################################################################################################################################
# load topic model
# only in or not in a topic
# find movies in topic
df = pd.read_csv('../weight.txt', sep='\t', header=None, names=["tid", "mid", "w"]).astype(int)
m_group = df[df['w'] > 10].sort_values(by='w', ascending=False).groupby('mid').head(10).groupby('tid')
# find users in topic
a = []
df = pd.read_csv('../doc', sep='\t', header=None, skiprows=1)
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
                # needs enough shared dataset for the
                if len(shared) > 100:
                    r, pv = pearsonr(shared['rating_x'], shared['rating_y'])
                    if r > 0:
                        res.append({'tid': tid, 'm1': m1, 'm2': m2, 'corr': r, 'cos': cosine(shared['rating_x'], shared['rating_y'])})

cnx = create_engine('mysql+mysqlconnector://root:yueyue@localhost:3306/recom2', echo=False)
pd.DataFrame(data=res).to_sql("ldist", cnx, index=False, if_exists='replace', chunksize=1000)
