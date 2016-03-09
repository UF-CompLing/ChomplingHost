# Title: CNN analysis
# Author: Dax Gerts
# Date: 24 February 2016
# Descriptio

## Modules

import nltk, re
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import word_tokenize

## Build training set from nltk subjectivity/objectivity corpora
training_subjective = [(sentences,'subj') for sentences in subjectivity.sents(categories='subj')[:5000]]
training_objective = [(sentences,'obj') for sentences in subjectivity.sents(categories='obj')[:5000]]
training = training_objective + training_subjective

# Build test set from CNN csv dump file
test = [] #source = [],date = [],title =[],authors = [],keywords = []

with open("cnn.csv") as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:	
		# Clean and separate text into sentence segments
		
		# Remove \n and \ characters
		clean_text = re.sub(r'(\\)','',re.sub('(\n)','',row['Text']))
		# Remove quotes
		clean_text = re.sub('"(.*?)"','',clean_text)
		#Tokenize strings
		tokenized_text = word_tokenize(clean_text)

		# Segment phrases and convert to unicode
		segments = []
		for i in range(len(tokenized_text)):
			segments.append(tokenized_text[i].encode("ascii"))		

		test.append((segments,'na'))

		# Other columns not used here
		#keywords.append(row['Keywords'])
		#source.append(row['Source'])
		#date.append(row['Date'])
		#title.append(row['Authors'])

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


