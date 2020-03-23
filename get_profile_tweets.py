import collections
import datetime as dt
from twitterscraper.query import query_tweets_from_user
import pandas as pd
from summary import summary
import json
import argparse

parser = argparse.ArgumentParser(description='Handle and json')
parser.add_argument('-han','--handle', type=str, help='twitter handle')
parser.add_argument('-j','--json',type=str, help='json filename with .json')
args = parser.parse_args()

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
    profile_dataframe = pd.read_json(filename, encoding='utf-8')

    lstt = []
    for i, val in enumerate(profile_dataframe['links']):
        if str(val) == '[]':
            lstt.append('[]')
        elif str(val[0][0:17]) == 'https://youtu.be/':
            pass
        else:
            summ = summary(profile_dataframe['links'][i][0])
            lstt.append(summ)
        profile_dataframe['summary'] = pd.DataFrame(lstt)

        is_summary = []
        for i, idx in enumerate(profile_dataframe['summary']):
            if len(str(idx)) > 3:
                is_summary.append(1)
            else:
                is_summary.append(0)

        profile_dataframe['is_summary'] = pd.DataFrame(is_summary)

    profile_dataframe.to_csv(filename[:-5] + ".csv")
    print('Loaded')

if __name__ == '__main__':
    get_profile_tweets(args.handle, args.json)
