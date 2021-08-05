# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 09:22:38 2021

@author: justi
"""

import pandas as pd
import seaborn as sns
import numpy as np
import re
import nltk
from itertools import combinations
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger',quiet=True)
from nltk.corpus import wordnet
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


def generate_word_document_matrix(corpus: pd.Series) -> np.array:
    
    try:
        CountVectorizer
    except: 
        from sklearn.feature_extraction.text import CountVectorizer
    
    #x = CountVectorizer(max_df = 0.95, min_df = 5)
    x = CountVectorizer()
    wd_matrix = x.fit_transform(corpus).toarray()
    vocab = x.get_feature_names()
    
    return wd_matrix, vocab

def vec_to_biterms(X):
    B_d = []
    for x in X:
        b_i = [b for b in combinations(np.nonzero(x)[0], 2)]
        B_d.append(b_i)
    return B_d

def remove_invalid_characters(string: str,language: str) -> str:
    
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
    tweet = regex.sub('',string)
    tweet = tweet.replace('\u2026','')  # this removes ellipses from tweets
    
    return tweet


def lemmatize(string: str) -> str:
    
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
    
    tags = nltk.pos_tag(nltk.word_tokenize(string))  # extracting the nltk POS tags
    tags = list(map(lambda x: (x[0], convert_tag_2_wordnet(x[1])),tags))    # converting nltk tags to wordnet equivalents
    
    # if POS tag is NoneType, simply add the word to the list. Otherwise, lemmatize the word and add to the list
    lemmatizedString = ' '.join([word[0] if word[1] is None else 
                       lemmatizer.lemmatize(word[0],word[1]) 
                       for word in tags])
    
    return lemmatizedString  


    
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
    
def remove_hyperlinks(string: str) -> str:
    return re.sub('(?=http\S)[^\s]+','',string)
    
def remove_retweet_tag(string: str) -> str:
    return re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', string)

def remove_username(string: str) -> str:
    return re.sub('(?=@\S)[^\s]+', '', string)

def make_lowercase(string: str) -> str:
    return string.lower().split()

def remove_stopwords(string: str, language: str) -> str:
    
    try:
        stopwords
    except NameError:
        stopwords = nltk.corpus.stopwords.words(language)
    
    tweet = [word for word in string if word not in stopwords]
    tweet = [word for word in tweet if len(word) > 1]
    return ' '.join(tweet)


def remove_emojis(string: str) -> str:
    
    #https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def clean_tweet(tweet: str, language: str) -> str:
    
    '''
    This function encompasses all cleaning functions (invalid character removal,
    lemmatization, etc.).
    '''
    
    tweet = remove_hyperlinks(tweet)
    tweet = remove_retweet_tag(tweet)
    tweet = remove_username(tweet)
    tweet = remove_invalid_characters(tweet, 'english')
    tweet = make_lowercase(tweet)
    tweet = remove_stopwords(tweet,'english')
    tweet = remove_emojis(tweet)
    cleanTweet = lemmatize(tweet)
    
    cleanTweet = ' '.join([word for word in cleanTweet.split(' ') if len(word) > 1])
    
    return cleanTweet

def get_biterms(corpus: pd.Series) -> list:
    
    biterms = []
    for document in corpus:
        document = document.split()
       # document_biterms = []
        if len(document) < 2: continue
        for i in range(len(document)):
            for j in range(i+1, len(document)):
                #biterms.append(' '.join([document[i], document[j]]))
                biterms.append([document[i],document[j]])
    return biterms

def get_vocab_from_biterms(biterms: list) -> set:
    #return set(' '.join(biterms).split(' '))
    v = []
    for biterm in biterms:
        v.extend(biterm)
    return set(v)

def get_words_and_count(data):
    
    '''
    Determines which words appear in the tweet database and how often
    the individual words appear in the tweet database
    '''
    wordsDict = {}
    for text in data:
        for word in text.split():
            if len(word) > 1:
                if word not in wordsDict:
                    wordsDict[word] = 1
                else:
                    wordsDict[word] += 1
        
    sortedWordsDict = {key: value for key, value in sorted(wordsDict.items(), key=lambda x: x[1], reverse=True)}
    return sortedWordsDict

def form_bag_of_words(data, words):
    
    '''
    Encodes the most frequent occuring words as a one-hot-encoded matrix. The
    matrix consists of one-hot-encoded vectors formed from the individual tweets.
    '''
    
    wordMatrix = np.empty((len(data),len(words)))
    for textNo, text in enumerate(data):
        text = text.split()
        wordVector = np.empty((1,len(words)))
        for i,word in enumerate(words):
            if word in text:
                wordVector[0,i] = 1
            else:
                wordVector[0,i] = 0
        wordMatrix[textNo,:] = wordVector
    return wordMatrix

def form_cooccurrence_matrix(wordMatrix, sums=1):
    
    '''
    Provides an overview of how often a word occurs in combination with 
    a seconds word.
    '''
    
    return (wordMatrix.T.dot(wordMatrix))/sums

def plot_word_cooccurrence_matrix(cooccurrence_matrix,labels):
    
    heatmap = sns.heatmap(cooccurrence_matrix, cmap='GnBu')
    heatmap.set_xticklabels(labels, rotation = 45)
    heatmap.set_yticklabels(labels, rotation = 45)
    
def plot_word_frequency(data,labels):
    
    sns.barplot(data=data, x=labels[0], y=labels[1], alpha=0.7)