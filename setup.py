import csv
import os, sys
sys.path.append("/home/django/Chompling/Chompling")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
from news.models import Article

rd = csv.reader(open('papers_master_clean.csv','r'), delimiter=',',quotechar='"')

for row in rd:
	if row[0] != 'SOURCE':
		article = Article()
		article.article_source = row[0]
		article.article_date = row[1]
		article.article_title = row[2]
		#article.article_author = row[3]
		#article.article_text = row[4]
		#article.article_keywords = row[5]