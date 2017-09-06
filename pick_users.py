import pandas as pd
import pickle

dir = open('data_source_folder','r').readline()
# get the reliable user sample

rating = pd.read_pickle(dir+'rating.pickle')
grouped = rating.groupby('userId').filter(lambda x: 2000 > len(x) > 500 and max(x['timestamp'])-min(x['timestamp'])>400000000)[['userId','movieId']]
pickle.dump(grouped, open(dir+'top_user.pickle', 'wb'))