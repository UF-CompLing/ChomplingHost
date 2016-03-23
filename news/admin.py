from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_display = ['article_id','article_author','article_keywords','article_title','article_text','article_source','article_date']
	list_editable = ['article_id','article_author','article_keywords','article_title','article_text','article_source','article_date']

admin.site.register(Article, ArticleAdmin)

