__author__ = 'Yueqi'
import pandas as pd
# movie similarity basing on attributes
from sqlalchemy import create_engine
cnx = create_engine("mysql://root:yueyue@localhost/recom")

# create a full plink table
# consider popular profiles only
movies = pd.read_sql('SELECT mid, genres, keyword, crew, cast, studio FROM movie', cnx)
import json
def get_attrs(row):
    res = []
    for n in ['genres', 'keyword', 'crew', 'cast', 'studio']:
        res += [json.dumps(v) for v in json.loads(row[n])] if row[n] is not None else []
    return set(res)

grouped = pd.Series(movies.apply(lambda row: get_attrs(row), axis=1).values, index=movies['mid'])

res = []
for m1, p1 in grouped.iteritems():
    for m2, p2 in grouped.iteritems():
        if m1 > m2:
            tt = len(p1.intersection(p2))
            if tt > 1:
                res.append({'m1':m1, 'm2':m2, 'dist': tt*1.0/(len(p1)+len(p2)-tt)})

cnx = create_engine('mysql+mysqlconnector://root:yueyue@localhost:3306/recom2', echo=False)
pd.DataFrame(res).to_sql("mdist", cnx, index=False, if_exists='replace', chunksize=1000)