import collections
import datetime as dt
from twitterscraper.query import query_tweets_from_user
import pandas as pd

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, collections.Iterable):
            return list(obj)
        elif isinstance(obj, dt.datetime):
            return obj.isoformat()
        elif hasattr(obj, '__getitem__') and hasattr(obj, 'keys'):
            return dict(obj)
        elif hasattr(obj, '__dict__'):
            return {member: getattr(obj, member)
                    for member in dir(obj)
                    if not member.startswith('_') and
                    not hasattr(getattr(obj, member), '__call__')}

        return json.JSONEncoder.default(self, obj)
    
def get_profile_tweets(handle, filename):
    profile = query_tweets_from_user(handle, limit=10)
    print('Loading...')
    with open(filename, "w", encoding="utf-8") as output:
        json.dump(profile, output, cls=JSONEncoder)
    profile_dataframe = pd.read_json('my.json', encoding='utf-8')
    profile_dataframe.to_csv('profile_tweets.csv')
    print('Loaded')    
