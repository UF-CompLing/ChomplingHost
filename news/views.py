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
from django.db.models import Max
from django.core.mail import EmailMessage
#import necessary models
from .models import Article
import datetime
import decimal

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
	price = request.GET.get('sort')
	
	try:
		query = str(query)
	except ValueError:
		query = None
		results = None

	if query:
	   	if price == None:
	   		results = Article.objects.order_by('article_title') # product name with str query in it
			results = results.filter(**{'article_title__icontains': str(query)}) #query, need to put in variable
			#results_price_sorted = None
			print("1")
		else:
			results = Product.objects.order_by('article_source') # product price
			results = results.filter(**{'article_source__icontains': str(query)}) 
			#results = None
			print("2")
	else:
		results = None
		results = None
	context = RequestContext(request)
	return render_to_response('news.html', {"results" : results}, context_instance=context)
