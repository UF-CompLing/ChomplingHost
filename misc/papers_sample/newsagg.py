# Name: News Aggregator (newsagg.py)
# Author: Dax Gerts
# Date: 12 February 2015

def main():
	import newspaper
	from newspaper import news_pool
	import re
	import csv
	import unicodedata

	# Active list of news/media sources
	
	sources = ['http://fivethirtyeight.com']

	#sources = ['http://cnn.com','http://foxnews.com',
	#'http://npr.org','http://msnbc.com','http://cbs.com',
	#'http://economist.com','http://time.com','http://nytimes.com',
	#'http://espn.com','http://reuters.com','http://usatoday.com',
	#'http://bbc.com','http://fivethirtyeight.com']

	papers = {} # Empty dictionary

	print("Building papers\n....\n...\n...")

	# Build diction, using url name for keys ex/ 'http://cnn.com' key will be 'cnn'
	for i in range(len(sources)):
		key = re.sub(r'(^https?:\/\/|\.com$|\.org$)','',sources[i])
		papers[key] = newspaper.build(sources[i],memoize_articles=False)
		# Print number of articles added from "recent" list for logging purposes
		print(key,papers[key].size())

	print("Downloading articles (this may take a while)\n...\n...\n...")

	# Download all articles via multi-threading
	news_pool.set([x[1] for x in papers.items()], threads_per_source=2) # Test various thread counts
	news_pool.join()

	print("Extracting text from articles \n...\n...\n...")

	# Parse all articles
	for i in papers:
		for j in range(papers[i].size()):
			#call to "download()" deprecated by news_pool.set & news_pool.join
			#papers[i].articles[j].download()
			papers[i].articles[j].parse()
			#extract keywords
			papers[i].articles[j].nlp()

	print("Writing new articles to dump file \n...\n...\n...")

	# Append articles to csv
	# Prototype format: col(1) = source, col(2) = title, col(3) = authors, col(4) = text
	with open('papers.csv','a') as outcsv:
		writer = csv.writer(outcsv)
		writer.writerow(["Source","Date","Title","Authors","Text","Keywords"])
		for i in papers:
			source = i
			for j in range(papers[i].size()):
				# Grab key features
				title = unicodedata.normalize('NFKD',papers[i].articles[j].title).encode('ascii','ignore')
				authors = [x.encode('UTF-8') for x in papers[i].articles[j].authors]
				text = unicodedata.normalize('NFKD',papers[i].articles[j].text).encode('ascii','ignore')
				date = papers[i].articles[j].publish_date
				#date = unicodedata.normalize('NFKD',papers[i].articles[j].publish_date).encode('ascii','ignore')
				# Identify keywords, while we're at it
				keywords = [x.encode('UTF-8') for x in papers[i].articles[j].keywords]
				writer.writerow([source,date,title,authors,text,keywords])

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()