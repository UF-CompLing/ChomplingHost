# News Analyzer Class
# Author: Dax Gerts
# Start Date: 11 March 2016
# End Data:	
# Description: collection of tools for simplifying regularly used analysis tasks and procedures

import nltk, re
from Tkinter import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity as sub
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import word_tokenize

class NewsSelector(Frame):

	def say_hi(self):
		print "hi there, everyone"

	def create_widgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"] = "red"
		self.QUIT["command"] = self.quit

		self.QUIT.pack({"side":"left"})

		self.hi_there = Button(self)
		self.hi_there["text"] = "Hello",
		self.hi_there["command"] = self.say_hi

		self.hi_there.pack({"side":"left"})

	def __init__(self, master=None):
		Frame.__init(self, master)
		self.pack()
		self.create_widgets()

class NewsAnalyzer:
	def __init__(self,load=True):

		# Preload data from master file
		if load == True:
			print("Loading master data file\n...\n...\n...")
			self.load_data()
			print("Finished loading master data file")

		# Prepare default training data for sentiment analysis
		training_subjective = [(sentences,'subj') for sentences in sub.sents(categories='subj')[:500]]
		training_objective = [(sentences,'obj') for sentences in sub.sents(categories='obj')[:500]]
		self.sentiment_training_default = training_objective + training_subjective
		
		print("NewsAnalyzer created")

	#load formatted data into analyzer object
	#	format should be one of the following:
	#		1) train + test data (supervised)
	#			ex/ "train":.....,"test":.......
	#		2) training data (unsupervised)
	#			ex/ 

	#def utf_8_encoder(unicoded_csv_data):
	#	for line in unicode_csv_data:
	#		yield line.encode('utf-8')

	# Load data from source files and store in object

	def load_data(self,source="papers.csv"):
		
		# Prepare object storage for news analyzer
		self.text = [];self.source = [];self.date = [];self.title = [];self.authors = [];self.keywords = []

		# Extract data values from csv master file
		with open(source) as csvfile:

			reader = csv.DictReader(csvfile)
			#reader = csv.DictReader(utf_8_encoder(csvfile))
			for row in reader:	
				# Clean and separate text into sentence segments
				
				# Remove \n and \ characters and correct encoding (as safeguard measure)
				clean_text = re.sub(r'(\\)','',re.sub('(\n)','',unicode(row['Text'],'utf-8')))
				# Remove quotes
				clean_text = re.sub('"(.*?)"','',clean_text)
				#Tokenize strings
				tokenized_text = word_tokenize(clean_text)

				# Segment phrases and convert to unicode
				segments = []
				for i in range(len(tokenized_text)):
					segments.append(tokenized_text[i])		

				# Store data values line by line
				self.text.append((segments,"subj"))
				self.keywords.append(row['Keywords'])
				self.source.append(row['Source'])
				self.date.append(row['Date'])
				self.authors.append(row['Authors'])
				self.title.append(row['Title'])
	
	# Select data of interest from all

	def select_data(self):

		root = Tk()
		app = NewsSelector(master=root)
		app.mainloop()
		root.destroy()

	# Conduct sentiment analysis

	def sentiment_analysis(self,testing_data,training_data=None):
		if training_data is None:
			training_data = self.sentiment_training_default
		## Apply sentiment analysis to data to extract new "features"

		# Initialize sentiment analyzer object
		sentiment_analyzer = SentimentAnalyzer()

		# Mark all negative words in training data, using existing list of negative words
		all_negative_words = sentiment_analyzer.all_words([mark_negation(data) for data in training_data])

		unigram_features = sentiment_analyzer.unigram_word_feats(all_negative_words, min_freq=4)
		len(unigram_features)
		sentiment_analyzer.add_feat_extractor(extract_unigram_feats,unigrams=unigram_features)

		training_final = sentiment_analyzer.apply_features(training_data)
		testing_final = sentiment_analyzer.apply_features(testing_data)
		
		## Traing model and test

		model = NaiveBayesClassifier.train
		classifer = sentiment_analyzer.train(model, training_final)

		for key, value in sorted(sentiment_analyzer.evaluate(testing_final).items()):
		    print('{0}: {1}'.format(key,value))


	#def load_data(self,**data):
	#	for key, value in data.items():
	#		setattr(self, key, value)

	#def get_keys(self):
	#	print(self.__dict__.keys())

	# Sentiment

