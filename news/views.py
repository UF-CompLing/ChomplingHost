from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.db.models import Max, Q
from django.core.mail import EmailMessage
#import necessary models
from .models import Article
import datetime
import decimal
import operator
import nltk, re
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import word_tokenize

def index(request):
	article_list = Article.objects.order_by('article_id')
	title_sorted_article_list = Article.objects.order_by('article_title')
	template = loader.get_template('news.html')
	context = RequestContext(request, {
		'article_list': article_list,
		#'price_sorted_product_list': price_sorted_product_list,
		})
	return HttpResponse(template.render(context))

def search(request):
	query = request.GET.get('q')
	sort = request.GET.get('sort')

	try:
		query = str(query)
	except ValueError:
		query = None
		results = None

	if query:
	   	if sort == None:
	   		results = Article.objects.order_by('article_title') # product name with str query in it
			results = results.filter(**{'article_title__icontains': str(query)}) #query, need to put in variable
			#results.article_date = article_date.strftime("%d/%m/%y")
			#results_price_sorted = None
			print("1")
		else:
			results = Article.objects.order_by('article_date') # product price
			results = results.filter(**{'article_title__icontains': str(query)}) 
			#results.article_date = article_date.strftime("%d/%m/%y")
			#results = None
			print("2")
	else:
		results = None
	context = RequestContext(request)
	return render_to_response('news.html', {"results" : results}, context_instance=context)

def classifier(article_text):

	# Size of dataset(s)

	n = 500
	print(article_text)
	# Get "n" subjective and objective phrases from subjectivity corpus

	subjective = [(sentences,'subj') for sentences in subjectivity.sents(categories='subj')[:n]]
	objective = [(sentences,'obj') for sentences in subjectivity.sents(categories='obj')[:n]]

	training_subjective = subjective[:int(.8*n)]
	test_subjective = subjective[int(.8*n):n]
	training_objective = objective[:int(.8*n)]
	test_objective = objective[int(.8*n):n]

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

	output = ""
	for key, value in sorted(sentiment_analyzer.evaluate(test_final).items()):
	    output = output + str('{0}: {1}'.format(key,value)) + "<br>"

	return output

def analyze(request):
	query = request.GET.get('q')
	sort = request.GET.get('sort')
	try:
		query = str(query)
	except ValueError:
		query = None
		results = None
	
	# Cleaning Options
	trash = request.GET.get('trash')
	length = request.GET.get('length')
	# Source Options
	sources = ['cnn','fox','npr','msnbc','ap','economist','time','fivethirtyeight','nytimes','espn','onion']
	# Procedures Options
	classify = request.GET.get('classify')
	polarity = request.GET.get('polarity')

	# Build sources
	#results = Article.objects.order_by('article_title')
	sources2 = []
	for i in range(len(sources)):
		if request.GET.get(sources[i]) != None:
			sources2.append(sources[i])
			print("check one")
	if len(sources2) != 0:
		query_set = reduce(operator.or_, (Q(article_source__icontains=item) for item in sources2))
		results = Article.objects.filter(query_set)
		if query != None:
			results = results.filter(**{'article_title__icontains': str(query)}) 
	else:
		results = None
	# Clean data
	if trash != None:
		print("trash removed")
	if length != None:
		print("short articles removed")

	output = "No dice, you gotta pick some data"

	# Run analysis
	if classify != None:
		# run classifier
		output = classifier(article_text = results.values_list('article_text',flat=True))
		print("classification analyzed")
	if polarity != None:
		# run polarity solver
		print("polarity analyzed")

	context = RequestContext(request)
	return render_to_response('news.html', {"results" : results,"output" : output}, context_instance=context)