from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render

import json, csv, random
from tweetlist import getAllTweets, cleanTweets, makeMarkovChain
from brain import analyze, getRandomTweet, thinkOfASentence
from beak import tweet
from twython import Twython
import requests

secrets_file = open('twitterbot/secrets.json', 'r')
secrets = json.load(secrets_file)

CONSUMER_KEY = secrets["twitter"]["consumer_key"]
CONSUMER_SECRET = secrets["twitter"]["consumer_secret"]
ACCESS_KEY = secrets["twitter"]["access_key"]
ACCESS_SECRET = secrets["twitter"]["access_secret"]

# twython - for analysis
twython = Twython(app_key=CONSUMER_KEY,
            app_secret=CONSUMER_SECRET,
            oauth_token=ACCESS_KEY,
            oauth_token_secret=ACCESS_SECRET)

# Create your views here.
def twitterbot(request):
	
	# Retrieve values from webpage
	user_name = request.GET.get('user_name')
	twitter_handle = request.GET.get('twitter_handle')
	send_tweet = request.GET.get('send_tweet')

	# Set twitter_handle as string for logical operations
	try:
		twitter_handle = str(twitter_handle)
	except ValueError:
		twitter_handle = None
		results = None
	
	# Set "send tweet" flag
	if send_tweet == None:
		send_tweet = False
	else:
		send_tweet = True

	# If twitter handle exists, attempt to retrieve tweets via Tweepy API and generate sentence
	# If it does not exist, report error to webpage
	if twitter_handle:
		if twitter_handle[0] == "@" and len(twitter_handle) > 0:
			twitter_handle = twitter_handle[1:len(twitter_handle)]
		print(twitter_handle + "\n\n\n")
		results = twitterbot_main(twitter_handle=twitter_handle,user_name=user_name,send_tweet=send_tweet)
	else:
		results = "Please enter a twitter handle"
	context = RequestContext(request)

	return render_to_response('twitterbot.html', {"results" : results}, context_instance=context)

def ajax(request):
	return "hey!"


def twitterbot_main(twitter_handle,user_name,send_tweet):
	print 'starting sentence generation'

	# Initialize sentence placeholder
	sentence = ""
	
	# Failure flag for graceful failure
	failed = False

	#Gather tweets and dump in csv "twitter_handle" + "_tweets.csv"
	try:
		getAllTweets(twitter_handle)
	except:
		print("EXCEPTION: getAllTweets failed")
		failed = True

	# Attempt to clean tweets
	try:
		cleanTweets(twitter_handle)
	except:
		print("EXCEPTION: cleanTweets failed")
		failed = True

	# Build Markov Chain
	try:		
		makeMarkovChain(twitter_handle)	
	except:
		print("EXCEPTION: makeMarkovChain failed")
		failed = True
	
	# Think of a sentence
	try:
		sentence = thinkOfASentence(twitter_handle)
	except:
		print("EXCEPTION: thinkOfASentence failed")
		failed = True

	if failed == True:
		sentence = twitter_handle + " is not valid. Please enter valid Twitter handle"
	
	# Build visible output
	if user_name:
		sentence = str(user_name) + " looked up " + str(twitter_handle) + " and created: \n" + sentence
	else:
		sentence = "Chompling_Bot looked up " + str(twitter_handle) + " and created: \n" + sentence
	
	# Tweet if flag is checked	
	if send_tweet == True:
		print "would have tweeted this\n\n\n"
		#tweet(sentence[0:140]) # tweet it

	print 'done generating sentence'

	return sentence
