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
	sources = ['cnn','foxnews','npr','msnbc','ap','economist','time','fivethirtyeight','nytimes','espn','onion']
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
	query_set = reduce(operator.or_, (Q(article_source__icontains=item) for item in sources2))
	results = Article.objects.filter(query_set)
	#results = results.filter({'article_source__icontains': sources2}) 

	# Clean data
	if trash != None:
		print("trash removed")
	if length != None:
		print("short articles removed")

	# Run analysis
	if classify != None:
		# run classifier
		print("classification analyzed")
	if polarity != None:
		# run polarity solver
		print("polarity analyzed")

	context = RequestContext(request)
	return render_to_response('news.html', {"results" : results}, context_instance=context)