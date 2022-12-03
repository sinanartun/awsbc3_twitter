from warnings import filterwarnings

import tweepy
import json
import os
import pandas as pd
import numpy as np

# To make sentiment analysis
from flair.models import TextClassifier
from flair.data import Sentence

import mysql.connector
from sqlalchemy import create_engine



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

api = tweepy.API(auth)
# public_tweets = api.user_timeline(screen_name="sinan_artun")

# users= input('Please Enter: ')

users = "BBCWorld"
public_tweets = []
all = []


def dbfonk(df):
    engine = create_engine(
        'mysql+mysqlconnector://username:pass@final.cluster-ciwzdfrp1kms.eu-central-1.rds.amazonaws.com:63306/twitter',
        echo=False)
    df.to_sql(name='twitter_analytics', con=engine, if_exists='append', index=False)


def sentiment_Flair(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "positive"
    elif "NEGATIVE" in str(score):
        return "negative"
    else:
        return "neutral"


sia = TextClassifier.load("en-sentiment")


def twapi(username):
    for i in range(0, 20):
        print(len(all))
        if len(all) != 0:

            for tweet in api.user_timeline(screen_name=username, max_id=all[-1]["tid"] - 1):
                if tweet:
                    row = {}
                    row['tweets'] = tweet.text
                    row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    row['tid'] = tweet.id
                    row['username'] = username
                    all.append(row)
                else:
                    continue;
        else:
            for tweet in api.user_timeline(screen_name=username):
                if tweet:
                    row = {}
                    row['tweets'] = tweet.text
                    row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    row['tid'] = tweet.id
                    row['username'] = username
                    all.append(row)
                else:
                    continue;
    df = pd.DataFrame(all)
    df['sentiment_flair'] = df['tweets'].apply(lambda x: sentiment_Flair(x))
    df["positive"] = np.where(df["sentiment_flair"] == 'positive', 1, 0)
    df["negative"] = np.where(df["sentiment_flair"] == 'negative', 1, 0)
    dbfonk(df)
    return df


# print(json.dumps(all))


"""
twt = []
time = []


alltweets = {}

userlist = ["SkyNews", "BBCWorld", "dwnews", "euronews", "nytimesworld"]

for tweet in public_tweets:
    row = {}
    row['tweets'] = tweet.text
    row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
    row['tid']= tweet.id
    all.append(row)



#user_tweets = pd.DataFrame({'tweets': twt, 'time_stamp': time})

#user_tweets[0:5]

# get date
#user_tweets["time_stamp"] = pd.to_datetime(user_tweets["time_stamp"])
#user_tweets['time_stamp'] = user_tweets['time_stamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
"""

# df['time_stamp'] = df['time_stamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))


# sentiment analysis


# print(df)

# user_tweets.to_csv('results.tsv', sep="\t")
# user_tweets.to_csv('results.csv')


# Database func


# data = pd.read_sql('SELECT * FROM sample_table', cnx)
