__author__ = 'Yueqi'
# distance between movies in global space basing on ratings (cosine distance)
import numpy as np
import pandas as pd

# consider movies already in the database only.
from sqlalchemy import create_engine
dir = open('data_source_folder','r').readline()

rating = pd.read_pickle(dir+'rating.pickle')
mids = pd.read_csv('mids.txt', names=['movieId'])

res = []
f_cnt = 0
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import cosine

groups = rating.merge(mids, how='inner', on='movieId').groupby('movieId')

for m1, v1 in groups:
    print(m1)
    for m2, v2 in groups:
        if m1 < m2:
            # enough shared users and positive correlation
            # shared = pd.merge(v1, v2, how='inner', on=['userId'])
            shared = v1[['userId','rating']].merge(v2[['userId','rating']], how='inner', on='userId')[['rating_x','rating_y']]

            if len(shared) > 100:
                r, pv = pearsonr(shared['rating_x'], shared['rating_y'])
                if r > 0:
                    res.append({'m1': m1, 'm2': m2, 'corr': r, 'cos': cosine(shared['rating_x'], shared['rating_y'])})
                    if len(res) > 500000:
                        pd.DataFrame(res).to_pickle(dir+'g_res.pickle'+str(f_cnt))
                        f_cnt += 1
                        res = []

pd.DataFrame(res).to_pickle(dir+'g_res.pickle'+str(f_cnt))