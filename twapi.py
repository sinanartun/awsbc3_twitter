from warnings import filterwarnings

import tweepy
import json
import os
import pandas as pd
import numpy as np
import uvicorn

# To make sentiment analysis
from flair.models import TextClassifier
from flair.data import Sentence

import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


consumer_key = os.environ['API_Key']
consumer_secret = os.environ['API_Key_Secret']
access_token = os.environ['Access_Token']
access_token_secret = os.environ['Access_Token_Secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

api = tweepy.API(auth)
# public_tweets = api.user_timeline(screen_name="sinan_artun")

# users= input('Please Enter: ')

users = "elonmusk"
public_tweets = []
all = []


def dbfonk(df):
    engine = create_engine(
        'mysql+mysqlconnector://synan:haydegidelum@twitter.ccypzg4lmcfd.eu-north-1.rds.amazonaws.com:3306/twitter',
        echo=False)
    df.to_sql(name='tweets', con=engine, if_exists='append', index=False)


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
    all = []
    for i in range(0, 20):
        print(len(all))
        if len(all) != 0:
            for tweet in api.user_timeline(screen_name=username, max_id=all[-1]["tid"] - 1):
                if tweet:
                    row = {}
                    row['tweet'] = tweet.text
                    row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    row['tid'] = tweet.id
                    row['username'] = username
                    all.append(row)



        else:
            for tweet in api.user_timeline(screen_name=username):
                if tweet:
                    row = {}
                    row['tweet'] = tweet.text
                    row['time_stamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    row['tid'] = tweet.id
                    row['username'] = username
                    all.append(row)


    df = pd.DataFrame(all)
    df['sentiment_flair'] = df['tweet'].apply(lambda x: sentiment_Flair(x))
    df["positive"] = np.where(df["sentiment_flair"] == 'positive', 1, 0)
    df["negative"] = np.where(df["sentiment_flair"] == 'negative', 1, 0)
    dbfonk(df)

    return df




@app.get("/username/{username}")
def run(username):
    twapi(username)
    return {"username": username}

if __name__ == "__main__":
    uvicorn.run("twapi:app", host="0.0.0.0", port=8000, reload=True)
