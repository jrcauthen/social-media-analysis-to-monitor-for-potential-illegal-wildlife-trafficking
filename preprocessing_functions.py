# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 13:59:53 2021

@author: justi
"""

import pandas as pd
import numpy as np


def create_tables(dbConnection):
    
    cursor = dbConnection.cursor()   # POSTGRESQL cursor object
    
    sql = [# Table 1
        '''CREATE TABLE IF NOT EXISTS twitter_users(user_id BIGINT PRIMARY KEY,
                                                follower_count INT, user_location TEXT);''',
        # Table 2
        '''CREATE TABLE IF NOT EXISTS twitter_tweets(tweet_id BIGINT PRIMARY KEY,
                                     tweet_text TEXT,
                                     rt_count INT,
                                     tweet_datetime TIMESTAMP,
                                     user_id BIGINT,
                                     CONSTRAINT fk_users
                                         FOREIGN KEY(user_id) REFERENCES twitter_users(user_id));''']
    
    # execute sql commands - create tables in database
    for command in sql:
        cursor.execute(command)
        
    dbConnection.commit()



def add_tweet(dbConnection,user_data,tweet_data):
    
    ''' 
    possible animalType values are "bears", "birds", "cats", "pangolins",
    "turtles", "elephant", "rhino"
    
    This function inserts a tweet into the animalType PostgreSQL database.
    
    add_tweet('database_table'), data)
    
    '''
    cursor = dbConnection.cursor()
    
    sql = ["INSERT INTO twitter_users"
            "(user_id, follower_count, user_location)"
            "VALUES (%s, %s, %s)"
            "ON CONFLICT(user_id) DO NOTHING;",
            "INSERT INTO twitter_tweets"
            "(tweet_id, tweet_text, rt_count, tweet_datetime, user_id)"
            "VALUES (%s, %s, %s, %s, %s)"
            "ON CONFLICT(tweet_id) DO NOTHING;"]
    
    cursor.execute(sql[0],user_data)
    cursor.execute(sql[1],tweet_data)
    
    dbConnection.commit()

def create_dataframe(dbConnection):
    
    '''
    This function selects all data from the the designated table and stores
    the returned values into a pandas dataframe.
    '''
    # cursor = dbConnection.cursor()
    # cursor.execute("SELECT * FROM {}".format(twitter_tweet))
    # query_results = cursor.fetchall()
    # cursor.close()
    
    # df = pd.DataFrame(query_results)
    # return df
    try:
        df = pd.read_sql_query(("SELECT * FROM twitter_tweets"),dbConnection)
        dbConnection.close()
        return df
        
    except Exception as e:
        dbConnection.close()
        print(str(e))
        
def filter_relevant_tweets(dbConnection):
    
    ''' 
    Searches the database for tweets which actually contain information related
    to wildlife as opposed to simple commerce, and returns them.
    
    This function is necessary because the filter method for the tweepy streaming
    doesn't seem to work that well. I'm getting lots of irrelevant tweets still.
    '''
    
    cursor = dbConnection.cursor()
    
    interesting_words = ['!ivory', 'horn', 'tusk', 'carved', 'mammoth', 'antique',
            'trophy', 'bone', 'medicine', 'medicinal', 'authentic', 'decorative']

    interesting_words = ' | !'.join(interesting_words)

    sql = ("DELETE * FROM twitter_tweets WHERE to_tsvector('english',tweet_text), @@ to_tsquery('english', interesting_words)")
    
    cursor.execute(sql)
    dbConnection.commit()
    
    
    
    