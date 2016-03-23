# Name: News Aggregator (newsagg.py)
# Author: Dax Gerts
# Date: 22 February 2016
# Aggregation script, run regularly to collect and dump raw text of web articles to csv files

def main():
	import newspaper # article download utility
	from newspaper import news_pool, Config, Article, Source
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

	# Store total and current number of articles for progress metrics
	total_articles = 0; current_articles = 0

	# Build diction, using url name for keys ex/ 'http://cnn.com' key will be 'cnn'
	for i in range(len(sources)):
		key = re.sub(r'(^https?:\/\/|\.com\n$|\.org\n$)','',sources[i])
		papers[key] = newspaper.build(sources[i],memoize_articles=True)
		
		# Print number of articles added from "recent" list for logging purposes
		total_articles = total_articles + papers[key].size()
		print(key,papers[key].size())

	print("Downloading articles (this may take a while)\n...\n...\n...")

	config = Config()
	config.fetch_images = False
	
	# Download all articles via multi-threading
	news_pool.set([x[1] for x in papers.items()], threads_per_source=2) # Test various thread counts
	news_pool.join()

	print("Extracting text from articles and writing to dump files \n...\n...\n...")

	# Append articles to aggregate and individual csv's
	# Format: col(1) = source, col(2) = date, col(3) = title, col(4) = authors, col(5) = text, col(6) = keywords
	with open('papers.csv','a') as outcsv:

		# Setup aggregate csv writer
		writer = csv.writer(outcsv)
		#writer.writerow(["Source","Date","Title","Authors","Text","Keywords"])

		# Traverse sources
		for i in papers:

			# Setup single_source csv writing
			source = i
			ind_outcsv = open(str(i+".csv"),'a')
			ind_writer = csv.writer(ind_outcsv)

			# Traverse articles in source			
			for j in range(papers[i].size()):

				# Parse articles and extract features
				current_articles += 1
				print("Processing " + str(i) + " article " + str(current_articles) + " of " + str(total_articles) + " (" + str("{0:.2f}".format((current_articles/float(total_articles)*100),2))
 + " %)")

				try:
					papers[i].articles[j].parse()

					# Grab key features
					title = unicodedata.normalize('NFKD',papers[i].articles[j].title).encode('ascii','ignore')
					authors = [x.encode('UTF-8') for x in papers[i].articles[j].authors]
					text = unicodedata.normalize('NFKD',papers[i].articles[j].text).encode('ascii','ignore')
					date = papers[i].articles[j].publish_date
					keywords = [x.encode('UTF-8') for x in papers[i].articles[j].keywords]
					
					# Add new row to both single-source and aggregate files
					ind_writer.writerow([source,date,title,authors,text,keywords])
					writer.writerow([source,date,title,authors,text,keywords])
					papers[i].articles[j].nlp()

				except httplib.BadStatusLine:
					print "httplib.BadStatusLine, no dice"
				
				

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()