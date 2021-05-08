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

try:
    cleanCorpus in globals()
except:
    # setting up small example dataframe
    df = create_dataframe("elephant_rhino",cnx)
    
    # selecting only the tweet text
    corpus = df["text"]
    
    # cleaning the individual tweets (removing non-english characters, lemmatization, etc.)
    cleanCorpus = corpus.apply(lambda x: clean_tweet(x,'english'))

cleanCorpus.to_pickle('./pickledCleanCorpus_elephantRhino.pkl')

cleanCorpus = pd.read_pickle('pickledCleanCorpus_elephantRhino.pkl')

wordsAndCount = getWordsAndCount(cleanCorpus)

# taking the most common 1000 words as a list of tuples -> (word, frequency of occurence)
mostCommonWordsTuples = list(wordsAndCount.items())

mostCommonWords = pd.DataFrame(mostCommonWordsTuples,
                                columns = ['word','frequency'])[0:10]

# creating the bag of words
wordMatrix = formBagOfWords(cleanCorpus, mostCommonWords['word'])
    
# forming bar plot of word frequency
bar = sns.barplot(data=mostCommonWords, x='word', y='frequency', alpha=0.7)

cm = wordMatrix.T.dot(wordMatrix)
sums = wordMatrix.sum(axis=0)


x = cooccurrenceMatrix(wordMatrix, sums=sums)   

heatmap = sns.heatmap(x,cmap='GnBu')