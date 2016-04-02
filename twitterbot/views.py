from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

# Create your views here.
def index(request):
	template = loader.get_template('twitterbot.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def ajax(request):
	return "hey!"