__author__ = 'Yueqi'
# distance between movies in global space basing on ratings (cosine distance)
import pandas as pd
# consider movies already in the database only.
dir = open('data_source_folder','r').readline()

rating = pd.read_pickle(dir+'rating_good.pickle')
mids = pd.read_csv('mids.txt', names=['movieId'])

res = []
users = dict((m1, set(v1['userId']))for m1, v1 in rating.groupby('movieId'))

for m1, v1 in users.items():
    for m2, v2 in users.items():
        if m1 > m2:
            shared = len(v1.intersection(v2))
            if shared > 10:
                j = shared*1.0 / (len(v1)+len(v2)-shared )
                if j > 0.005:
                    res.append([m1, m2, j])

res = pd.DataFrame(res, columns=['m1','m2','jacc'])
res2 = res.copy()
res2 = res2.rename(columns={"m1": "m2", "m2": "m1"})
pd.concat([res, res2]).to_pickle(dir+'g_res.pickle')