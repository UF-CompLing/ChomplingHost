# Title: Sentiment Analysis Example 1
# Author: Dax Gerts
# Date: 2 February 2016
# Description: introductory example to sentiment analysis with python-nltk, based heavily on example provided by at www.nltk.org/howto/sentiment.html

# Important components of NLTK libraries

from nltk.classify import NaiveBayesClassifier

# Corpus of phrases divided between subjective/objective

# "The Subjectivity Dataset contains 5000 subjective and 5000 objective processed sentences."
# More info here: "www.nltk.org/howto/corpus.html"

from nltk.corpus import subjectivity


from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

