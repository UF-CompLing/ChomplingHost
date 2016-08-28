from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse

# Create your views here.

def index(request):
	template = loader.get_template('Chompling.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))
