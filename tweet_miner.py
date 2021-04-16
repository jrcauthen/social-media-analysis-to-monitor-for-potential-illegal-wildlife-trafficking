#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tweepy
from environment_vars import *
from my_imports import *
import mysql.connector
import wget

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

cnx = mysql.connector.connect(user=USER, password=PASSWORD,
                              host=HOST,
                              database=DB)

cursor = cnx.cursor()

# THESE VALUES MUST BE CHANGED ACCORDING THE RELEVANT SOUGHT AFTER INFORMATION

# TODO: MAYBE TURN THIS SCRIPT INTO A FUNCTION

imageDirectory = "images/elephantRhino_images"
keywordString = " OR ".join(elephantRhinoKeywords + generalKeywords) + " -filter:retweets"

#tweets = []     # initializing the list in which tweets will be stored
images = set()  # ensuring that there are no repeat images

for tweet in tweepy.Cursor(api.search, q = keywordString).items(400): 
    tweetJSON = tweet._json
    
    # checking for linked images or videos and saving them if present
    if 'media' in tweetJSON['entities']:
        for i in range(len(tweetJSON['entities']['media'])):
            if tweetJSON['entities']['media'][i]['type'] == 'photo':
                images.add(tweetJSON['entities']['media'][i]['media_url'])
                wget.download(tweetJSON['entities']['media'][i]['media_url'], imageDirectory)

    # very few tweets have coordinates embedded - they should be extracted if present
    if tweet.coordinates is None:
        coordinates = ''
    else:
        coordinates = str(tweet.coordinates['coordinates'])[1:-2]
    
    
    tweetData = (tweet.id_str, ", ".join(list(images)), tweet.user.followers_count,
                  tweet.user.location, tweet.text, tweet.created_at,
                  coordinates)
    
    images.clear()  # removing all image filenames from the current images list, the next tweet wil repopulate with new images
    
    # adding relevant extracted tweet data tweetData to the passed MySQL table
    cursor.execute(add_tweet('elephant_rhino'), tweetData)
    cnx.commit()
    
    #tweets.append(tweet._json)
 

cursor.close()
cnx.close()
 
    



