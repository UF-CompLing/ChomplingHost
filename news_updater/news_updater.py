# Name: News Aggregator (newsagg.py)
# Author: Dax Gerts
# Date: 22 February 2016

def main():
	import newspaper # article download utility
	from newspaper import news_pool
	import re # regex
	import csv # csv file-formatting
	import unicodedata # string cleaning
	from datetime import datetime # time-checking for cache-updates

	print("Retrieving sources and update times\n...")

	# Read active list of news/media sources
	f = open("sourcelist","r")
	sources = f.read().splitlines()
	times = []

	#
	# ONGOING: update time storage and retrieval
	#		-dependent on if caching is sufficient

	papers = {} # Empty dictionary

	print("Building papers\n....\n...\n...")

	# Build diction, using url name for keys ex/ 'http://cnn.com' key will be 'cnn'
	for i in range(len(sources)):
		key = re.sub(r'(^https?:\/\/|\.com\n$|\.org\n$)','',sources[i])
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
			# Parse articles and extract features
			papers[i].articles[j].parse()
			papers[i].articles[j].nlp()

	print("Writing new articles to dump file \n...\n...\n...")

	# Append articles to aggregate and individual csv's
	# Format: col(1) = source, col(2) = date, col(3) = title, col(4) = authors, col(5) = text, col(6) = keywords
	with open('papers.csv','a') as outcsv:

		# Setup aggregate csv writer
		writer = csv.writer(outcsv)
		writer.writerow(["Source","Date","Title","Authors","Text","Keywords"])

		# Traverse sources
		for i in papers:

			# Setup single_source csv writing
			source = i
			ind_outcsv = open(str(i+".csv"),'a')
			ind_writer = csv.writer(ind_outcsv)

			# Traverse articles in source			
			for j in range(papers[i].size()):

				# Grab key features
				title = unicodedata.normalize('NFKD',papers[i].articles[j].title).encode('ascii','ignore')
				authors = [x.encode('UTF-8') for x in papers[i].articles[j].authors]
				text = unicodedata.normalize('NFKD',papers[i].articles[j].text).encode('ascii','ignore')
				date = papers[i].articles[j].publish_date
				keywords = [x.encode('UTF-8') for x in papers[i].articles[j].keywords]
				
				# Add new row to both single-source and aggregate files
				ind_writer.writerow([source,date,title,authors,text,keywords])
				writer.writerow([source,date,title,authors,text,keywords])

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()