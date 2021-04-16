#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from environment_vars import USER, HOST, PASSWORD, DB
from my_imports import *
from cleaning_functions import *
import mysql.connector
from nltk import word_tokenize
import pandas as pd

# setting up connection to MySQL database with stored tweets
cnx = mysql.connector.connect(user=USER, password=PASSWORD,
                              host=HOST,
                              database=DB)

# setting up small example dataframe
df = create_dataframe("elephant_rhino",cnx)

# selecting only the tweet text
corpus = df["text"]

# cleaning the individual tweets (removing non-english characters, lemmatization, etc.)
cleanCorpus = corpus.apply(lambda x: clean_tweet(x,'english'))