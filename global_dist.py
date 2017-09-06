__author__ = 'Yueqi'
# distance between movies in global space basing on ratings (cosine distance)
import pandas as pd

# consider movies already in the database only.
from sqlalchemy import create_engine
nodes = [int(v) for v in open('mids.txt')]

# load all movie rating from pickle
rating = pd.read_pickle('rating.pickle')

res = []
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import cosine

groups = rating.groupby('movieId')

# calculate pair distance of movies exists in the topic model.
for m1, v1 in groups:
    if m1 in nodes:
        print(m1)
        for m2, v2 in groups:
            if m1 < m2 and m2 in nodes:
                # enough shared users and positive correlation
                # shared = pd.merge(v1, v2, how='inner', on=['userId'])
                shared = v1[['userId','rating']].merge(v2[['userId','rating']], how='inner', on='userId')[['rating_x','rating_y']]

                if len(shared) > 40:
                    r, pv = pearsonr(shared['rating_x'], shared['rating_y'])
                    if r > 0:
                        res.append({'m1': m1, 'm2': m2, 'corr': r, 'cos': cosine(shared['rating_x'], shared['rating_y'])})
import mysql.connector
cnx = create_engine('mysql+mysqlconnector://root:yueyue@localhost:3306/recom2', echo=False)
pd.DataFrame(data=res).to_sql("gdist", cnx, index=False, if_exists='replace', chunksize=1000)

