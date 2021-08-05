# -*- coding: utf-8 -*-

import yaml
import tweepy
import time
import psycopg2
from preprocessing_functions import *


try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    print('Error reading configuration file.')
    
# connecting to the POSTGRESQL server
cnx = psycopg2.connect(
    database = config['DATABASE'],
    host = config['HOST'],
    user = config['USER'],
    password = config['PASSWORD'])

cursor = cnx.cursor()   # POSTGRESQL cursor object

auth = tweepy.OAuthHandler(config['API_KEY'], config['SECRET_KEY'])
auth.set_access_token(config['ACCESS_TOKEN'], config['SECRET_TOKEN'])
api = tweepy.API(auth,wait_on_rate_limit=True)

create_tables(cnx)


class StreamListener(tweepy.StreamListener):
    
    def __init__(self, time_limit=15):
        self.start_time = time.time()
        self.limit = time_limit
        super(StreamListener, self).__init__()
    
    def on_status(self, status):    
        
        if status.truncated:
            status.text = status.extended_tweet['full_text']

        tweet_data = (status.id, status.text, status.retweet_count, status.created_at, status.user.id)
        user_data = (status.user.id, status.user.followers_count, status.user.location)
                
        if status.retweeted:
            return
        else:
            add_tweet(cnx,user_data,tweet_data)
        

def stream_tweets():
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener)
    stream.filter(track=config['ELEPHANT_KEYWORDS'], languages=['en'])

stream_tweets()

cursor.close()
cnx.close()