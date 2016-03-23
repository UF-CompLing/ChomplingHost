def main():
	# Django Setup
	import os, sys
	sys.path.append("/home/django/Chompling/Chompling")
	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	import django
	django.setup()
	from news.models import Article as Article2
	import newspaper # article download utility
	from newspaper import news_pool, Config, Article, Source
	import re # regex
	import csv # csv file-formatting
	import unicodedata # string cleaning
	from datetime import datetime # time-checking for cache-updates
	import httplib
	print("Retrieving sources and update times\n...")

	# Read active list of news/media sources
	f = open("sourcelist","r")
	sources = f.read().splitlines()
	times = []

	for i in sources:
		paper = newspaper.build(i,memoize_articles=True)
		num_articles = paper.size()
		source = re.sub(r'(^https?:\/\/|\.com\n$|\.org\n$)','',i)
		print(source,num_articles)


		config = Config()
		config.fetch_images = False
		
		# Download all articles via multi-threading
		news_pool.set([paper], threads_per_source=2) # Test various thread counts
		news_pool.join()

		# Traverse articles in source			
		for j in range(paper.size()):

			# Parse articles and extract features
			print("Processing article " + str(i) +  " of " + str(num_articles) + " (" + str("{0:.2f}".format((j/float(num_articles)*100),2))
 + " %)")

			try:

				paper.articles[j].parse()
				paper.articles[j].nlp()

				# Grab key features
				title = unicodedata.normalize('NFKD',paper.articles[j].title).encode('ascii','ignore')
				if title is None:
					title = "NA"
				author = [x.encode('UTF-8') for x in paper.articles[j].authors]
				if author is None:
					author = "NA"
				text = unicodedata.normalize('NFKD',paper.articles[j].text).encode('ascii','ignore')
				if text is None:
					text = "NA"
				date = paper.articles[j].publish_date
				if date is None:
					date = datetime.now()
				keywords = [x.encode('UTF-8') for x in paper.articles[j].keywords]
				if keywords is None:
					keywords = "NA"
				article = Article2(article_source=source,article_title=title,article_author=author,article_text=text,article_date=date,article_keywords=keywords)
				article.save()
			except httplib.BadStatusLine:
				print "httplib.BadStatusLine, no dice"
				
				

if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	import logging
	logging.basicConfig()
	main()