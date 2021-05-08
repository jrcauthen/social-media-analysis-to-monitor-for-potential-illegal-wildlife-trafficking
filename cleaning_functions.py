#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
CLEANING_FUNCTION MODULE CONTAINS ALL FUNCTIONS USED TO CLEAN UP THE DATAFRAMES/TWEETS.
'''


import re
import nltk
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger',quiet=True)
from nltk.corpus import wordnet
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


def remove_invalid_characters(tweet: str,language: str) -> str:
    
    '''
    This function removes all punctuation, symbols, non-English characters,
    and hyperlinks from the passed tweet.
    '''
    
    # TODO: ADD ADDITIONAL LANGUAGE CAPABILITIES
    # TODO: WHY DOES UTF-8 RETURN HEX AND ASCII DOESN'T?
    # TODO: WHY DOES THE REGEX NOT FILTER OUT ELLIPSES?
    
    if language == "english":   
        encoding = "ascii"
    
    #tweet = tweet.encode(encoding, errors="ignore")  # filter out non ASCII/UTF-8 characters
    
    # filter out all non-alphanumeric characters
    regex = re.compile('[' + re.escape('!@#$%^&*()_+=-[]\'\\{}"|\.>/?,<;:~`’“”') + '0-9-_]')
    tweet = regex.sub('',tweet)
    tweet = tweet.replace('\u2026','')  # this removes ellipses from tweets
    
    return tweet


def lemmatize_tweet(tweet: str) -> str:
    
    ''' 
    This function takes the "stem" of a token in a tokenized tweet. The lines below
    give an idea of how this should look:
        
    "animals" --> "animal"
    "grazing" --> "graze"
    '''
    
    try:
        lemmatizer
    except NameError:
        lemmatizer = WordNetLemmatizer()
    
    tags = nltk.pos_tag(nltk.word_tokenize(tweet))  # extracting the nltk POS tags
    tags = list(map(lambda x: (x[0], convert_tag_2_wordnet(x[1])),tags))    # converting nltk tags to wordnet equivalents
    
    # if POS tag is NoneType, simply add the word to the list. Otherwise, lemmatize the word and add to the list
    lemmatizedTweet = ' '.join([word[0] if word[1] is None else 
                       lemmatizer.lemmatize(word[0],word[1]) 
                       for word in tags])
    
    return lemmatizedTweet    


    
def convert_tag_2_wordnet(tag: str) -> str:
    
    '''
    NLTK POS tags are not similar to wordnet POS tags. These must be mapped to
    the corresponding types.
    
    "J" : ADJECTIVE TYPE
    "N" : NOUN TYPE
    "V" : VERB TYPE
    "R" : ADVERB TYPE
    '''
    
    if tag[0] == 'J':
        return wordnet.ADJ
    if tag[0] == 'N':
        return wordnet.NOUN
    if tag[0] == 'V':
        return wordnet.VERB
    if tag[0] == 'R':
        return wordnet.ADV
    else:
        return None
    
    


def clean_tweet(tweet: str, language: str) -> str:
    
    '''
    This function encompasses all cleaning functions (invalid character removal,
    lemmatization, etc.).
    '''
    
    try:
        stopwords
    except NameError:
        stopwords = nltk.corpus.stopwords.words(language)
    
    tweet = re.sub('(?=http\S)[^\s]+','',tweet)     # remove hyperlinks
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet tag
    tweet = re.sub('(?=@\S)[^\s]+', '', tweet) # remove user names
    
    tweet = remove_invalid_characters(tweet, "english")
    tweet = tweet.lower().split()   # making tweet entirely lowercase
    
    # remove stopwords from the tweet
    tweet = [word for word in tweet if word not in stopwords]
    tweet = ' '.join(tweet)

    # lemmatize the tweet to reduce set of counted words
    lemmatizedTweet = lemmatize_tweet(tweet)
    
    return lemmatizedTweet