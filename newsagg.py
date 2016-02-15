# Name: News Aggregator (newsagg.py)
# Author: Dax Gerts
# Date: 12 February 2015

def main():
	import newspaper
	from newspaper import news_pool
	import re

	# Active list of news/media sources
	
	sources = ['http://cnn.com','http://foxnews.com',
	'http://npr.org','http://msnbc.com','http://cbs.com','www.ap.org',
	'http://economist.com','http://time.com','http://nytimes.com',
	'http://slate.com','http://espn.com','http://reuters.com','http://usatoday.com'
	'http://bbc.com','http://fivethirtyeight.com']

	papers = {} # Empty dictionary

	# Build diction, using url name for keys ex/ 'http://cnn.com' key will be 'cnn'
	for i in range(len(sources)):
		papers[re.sub(r'(^https?:\/\/|\.com$|\.org$)','',sources[i])] = newspaper.build(sources[i],memoize_articles=False)
	
	# Print number of articles added from "recent" list for logging purposes
	for i in papers:
		print(i,papers[i].size())

	# Download all articles via multi-threading
	news_pool.set(papers, threads_per_source=1) # Test various thread counts
	news_pool.join()

	# Parse all articles
	for i in papers:
		for j in range(papers[i].size()):
			#call to "download()" deprecated by news_pool.set & news_pool.join
			#papers[i].articles[j].download()
			papers[i].articles[j].parse()

	# Export articles to csv
	# Prototype format: col(1) = source, col(2) = title, col(3) = authors, col(4) = text
	writer = csv.writer(open('papers.csv','wb'))
	for i in papers:
		source = i
		for j in range(papers[i].size()):
			# Grab key features
			title = paper[i].articles[j].title
			authors = paper[i].articles[j].authors
			text = papers[i].articles[j].text
			# Identify keywords, while we're at it
			keywords = papers[i].articles[j].keywords
			writer.writerow([source,title,authors,text,keywords])

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()