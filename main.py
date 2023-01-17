from warnings import filterwarnings

import tweepy
import json
import os
import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ['API_Key']
consumer_secret = os.environ['API_Key_Secret']
access_token = os.environ['Access_Token']
access_token_secret = os.environ['Access_Token_Secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
all = []



def print_hi(name):
    username = 'elonmusk'
    for tweet in api.user_timeline(screen_name=username):
        if tweet:
            row = {}
            row['tweets'] = tweet.text
            row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            row['tid'] = tweet.id
            row['username'] = username
            all.append(row)
        else:
            continue

    print(json.dumps(all, indent=0, sort_keys=True, default=str))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
