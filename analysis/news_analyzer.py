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

	def finish_selection(self):
		print "processing data subset"
		process_selection()
	#
	# STARTING SIMPLE, SOURCES ONLY, FRAMEWORK FOR REMAINDER
	#

	# Take user-inputted values and build subset (dump to csv)
	def process_selection():

		with open('papers.csv','r') as incsv, open('papers_subset.csv','w') as outcsv:

			# Use csv reader and list of sources to select rows of interest
			reader = csv.DictReader(incsv)
			sources = set(source)

			for row in reader:
				if row['Source'] in sources:
					outcsv.write(row) # Write row if in desired list of sources


	def create_widgets(self):
		self.vsb = Scrollbar(self,orient="vertical")
		self.text = Text(self, width=40, height=20, yscrollcommand=self.vsb.set)
		self.vsb.config(command=self.text.yview)
		self.vsb.pack(side="right",fill="y")
		self.text.pack(side="left",fill="both",expand=True)

		for i in self.source:
			cb = Checkbutton(self, text=str(i))
			self.text.window_create("end", window = cb)
			self.text.insert("end", "\n") # one checkbox per line

		self.finish_selection = Button(self)
		self.finish_selection["text"] = "Finish Selection",
		self.finish_selection["command"] = self.finish_selection

		self.finish_selection.pack(side = BOTTOM)

	def __init__(self,source,keywords,date,authors,master=None):
		Frame.__init__(self, master)
		self.source = set(source)
		self.keywords = keywords
		self.date = date
		self.authors = authors
		self.pack()
		self.create_widgets()

class NewsAnalyzer:
	def __init__(self,load=True,set_defaults=True):

		# Set global defaults
		self.data_source = "papers.csv"
		self.source = self.keywords = self.authors = self.date = self.text = self.title = []
		# Preload data from master file
		if load == True:
			self.load_data()

		# Prepare default training data for sentiment analysis
		if set_defaults == True:
			training_subjective = [(sentences,'subj') for sentences in sub.sents(categories='subj')[:500]]
			training_objective = [(sentences,'obj') for sentences in sub.sents(categories='obj')[:500]]
			self.training_data = training_objective + training_subjective
		
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
		
		print("Loading " + source + " data file\n...\n...\n...")
	
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
	
		print("Finished loading " + source + " data file")
	
	# Select data of interest from all

	def select_data(self):

		root = Tk()
		app = NewsSelector(master=root,source=self.source,keywords=self.keywords,date=self.date,authors=self.authors)
		app.mainloop()
		root.destroy()

		self.papers_source = "papers_subset.csv"

	# Conduct sentiment analysis

	def sentiment_analysis(self,testing_data,training_data=None):
		if training_data is None:
			training_data = self.training_data
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

