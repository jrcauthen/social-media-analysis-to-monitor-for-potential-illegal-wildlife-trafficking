

from preprocessing_functions import *
from nlp_functions import *
from nltk import word_tokenize
from btm import gibbs, fit_transform
import yaml
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import psycopg2
import pyLDAvis


# loading the configuration files
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

try:
    cleanCorpus in globals()
except:
    # setting up small example dataframe
    df = create_dataframe(cnx).tail(10)
    
    # selecting only the tweet text
    corpus = df["tweet_text"]
    
    # cleaning the individual tweets (removing non-english characters, lemmatization, etc.)
    cleanCorpus = corpus.apply(lambda x: clean_tweet(x,'english'))

cleanCorpus.to_pickle('./pickledCleanCorpus_elephant.pkl')

cleanCorpus = pd.read_pickle('pickledCleanCorpus_elephant.pkl')

wd_matrix, V = generate_word_document_matrix(cleanCorpus)

B = vec_to_biterms(wd_matrix)
#B = get_biterms(cleanCorpus)
#V = get_vocab_from_biterms(B)

#n_z, n_wz = gibbs(5,B,V,10)
topics, phi_wz = fit_transform(B,V,10,5,1.0,0.1,0.5)
pyLDAvis.enable_notebook()
vis = pyLDAvis.prepare(phi_wz.T, topics, np.count_nonzero(wd_matrix,axis=1),V,np.sum(wd_matrix,axis=0))
pyLDAvis.display(vis)
pyLDAvis.save_html(vis, './online_btm.html')

# wordsAndCount = get_words_and_count(cleanCorpus)

# # taking the most common 1000 words as a list of tuples -> (word, frequency of occurrence)
# mostCommonWordsTuples = list(wordsAndCount.items())

# mostCommonWords = pd.DataFrame(mostCommonWordsTuples,
#                                 columns = ['word','frequency'])[0:10]

# # creating the bag of words
# wordMatrix = form_bag_of_words(cleanCorpus, mostCommonWords['word'])
    
# forming bar plot of word frequency
#plot_word_frequency(mostCommonWords,('word','frequency'))

# cm = wordMatrix.T.dot(wordMatrix)
# sums = wordMatrix.sum(axis=0)


# cooccurrence_matrix = form_cooccurrence_matrix(wordMatrix, sums=sums)

#plot_word_cooccurrence_matrix(cooccurrence_matrix, mostCommonWords['word'])