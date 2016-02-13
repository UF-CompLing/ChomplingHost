# Name: News Aggregator (newsagg.py)
# Author: Dax Gerts
# Date: 12 February 2015

def main():
	import newspaper
	import re

	# Active list of news/media sources
	sources = ['http://cnn.com','http://foxnews.com','http://npr.org','http://msnbc.com','http://cbs.com','www.ap.org']
	papers = {} # Empty dictionary

	# Build diction, using url name for keys ex/ 'http://cnn.com' key will be 'cnn'
	for i in range(len(sources)):
		papers[re.sub(r'(^https?:\/\/|\.com$|\.org$)','',sources[i])] = newspaper.build(sources[i],memoize_articles=False)
	
	# Print number of articles added from "recent" list
	for i in papers:
		print(i,papers[i].size())

	# Download and parse articles
	for i in papers:
		for j in range(papers[i].size()):
			papers[i].articles[j].download()
			papers[i].articles[j].parse()

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()