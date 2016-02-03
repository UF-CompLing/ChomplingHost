# Title: Sentiment Analysis Example 1
# Author: Dax Gerts
# Date: 2 February 2016
# Description: introductory example to sentiment analysis with python-nltk, based heavily on example provided by at www.nltk.org/howto/sentiment.html
#   Example uses the 'sentiment anlyzer' tool to prepare data for classification with Naive Bayes Classifier

## Modules

# 1. NaiveBayesClassifier (machine learning method)

# Naive Bayes Classifier is the machine learning model used in this example
# More info https://en.wikipedia.org/wiki/Naive_Bayes_classifier

from nltk.classify import NaiveBayesClassifier

# 2. Subjectivity (the data)

# Corpus of phrases divided between subjective/objective

# "The Subjectivity Dataset contains 5000 subjective and 5000 objective processed sentences."
# More info www.nltk.org/howto/corpus.html

from nltk.corpus import subjectivity

# 3. NLTK Sentiment Tools

# The NLTK's collection of sentiment analysis tools
# More info www.nltk.org

from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

## Build training and testing data sets

# Size of dataset(s)

n = 1000

# Get "n" subjective and objective phrases from subjectivity corpus

subjective = [(sentences,'subj') for sentences in subjectivity.sents(categories='subj')[:n]]
objective = [(sentences,'obj') for sentences in subjectivity.sents(categories='obj')[:n]]

# Here's what the first item in "subjective" looks like
# Note that it's stores as (phrase, label)

subjective[0]

# Create separate training and test data sets, this is pretty standard in any data mining/machine learning task
# The typical split is, as seen here (training = 80%, train = 20%)

training_subjective = subjective[:int(.8*n)]
test_subjective = subjective[int(.8*n):n]
training_objective = objective[:int(.8*n)]
test_objective = objective[int(.8*n):n]

# Now aggregate the training and test sets

training = training_subjective + training_objective
test = test_subjective + test_objective

## Apply sentiment analysis to data to extract new "features"

# Initialize sentiment analyzer object

sentiment_analyzer = SentimentAnalyzer()

# Mark all negative words in training data, using existing list of negative words

all_negative_words = sentiment_analyzer.all_words([mark_negation(data) for data in training])

unigram_features = sentiment_analyzer.unigram_word_feats(all_negative_words, min_freq=4)
len(unigram_features)
sentiment_analyzer.add_feat_extractor(extract_unigram_feats,unigrams=unigram_features)

training_final = sentiment_analyzer.apply_features(training)
test_final = sentiment_analyzer.apply_features(test)

## Traing model and test

model = NaiveBayesClassifier.train
classifer = sentiment_analyzer.train(model, training_final)

for key, value in sorted(sentiment_analyzer.evaluate(test_final).items()):
    print('{0}: {1}'.format(key,value))

