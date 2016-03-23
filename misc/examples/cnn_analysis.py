# Title: CNN analysis
# Author: Dax Gerts
# Date: 24 February 2016
# Description

## Modules

import nltk, re
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity as sub
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import word_tokenize

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.encode('utf-8')

def training_setup():
	## Build training set from nltk subjectivity/objectivity corpora
	training_subjective = [(sentences,'subj') for sentences in sub.sents(categories='subj')[:500]]
	training_objective = [(sentences,'obj') for sentences in sub.sents(categories='obj')[:500]]
	training = training_objective + training_subjective
	return training

def testing_setup():
	# Build test set from CNN csv dump file
	testing = [] #source = [],date = [],title =[],authors = [],keywords = []

	with open("cnn.csv") as csvfile:
		reader = csv.DictReader(utf_8_encoder(csvfile))
		for row in reader:	
			# Clean and separate text into sentence segments
			
			# Remove \n and \ characters
			clean_text = re.sub(r'(\\)','',re.sub('(\n)','',unicode(row['Text'],'utf-8')))
			# Remove quotes
			clean_text = re.sub('"(.*?)"','',clean_text)
			#Tokenize strings
			tokenized_text = word_tokenize(clean_text)

			# Segment phrases and convert to unicode
			segments = []
			for i in range(len(tokenized_text)):
				segments.append(tokenized_text[i])		

			testing.append((segments,"subj"))

			#keywords.append(row['Keywords'])
			#source.append(row['Source'])
			#date.append(row['Date'])
			#title.append(row['Authors'])
	return testing

def build_and_test_model(training,testing):
	## Apply sentiment analysis to data to extract new "features"

	# Initialize sentiment analyzer object
	sentiment_analyzer = SentimentAnalyzer()

	# Mark all negative words in training data, using existing list of negative words
	all_negative_words = sentiment_analyzer.all_words([mark_negation(data) for data in training])

	unigram_features = sentiment_analyzer.unigram_word_feats(all_negative_words, min_freq=4)
	len(unigram_features)
	sentiment_analyzer.add_feat_extractor(extract_unigram_feats,unigrams=unigram_features)

	training_final = sentiment_analyzer.apply_features(training)
	testing_final = sentiment_analyzer.apply_features(testing)
	
	## Traing model and test

	model = NaiveBayesClassifier.train
	classifer = sentiment_analyzer.train(model, training_final)

	for key, value in sorted(sentiment_analyzer.evaluate(testing_final).items()):
	    print('{0}: {1}'.format(key,value))

if __name__ == "__main__":
	training = training_setup()
	testing = testing_setup()
	build_and_test_model(training=training,testing=testing)