from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

class Article(models.Model):
	# Automatically generated id
	article_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.article_id
	# Link to Authors table
	article_author = models.CharField(max_length=50)
	def __unicode__(self):
		return self.article_author
	# Links to Keywords table
	article_keywords = models.TextField()
	def __unicode__(self):
		return self.article_keywords
	article_title = models.TextField()
	def __unicode__(self):
		return self.article_title
	article_text = models.TextField()
	def __unicode__(self):
		return self.article_text
	article_source = models.CharField(max_length=20)
	def __unicode__(self):
		return self.article_source
	article_date = models.DateField()
	def __unicode__(self):
		return self.article_date



